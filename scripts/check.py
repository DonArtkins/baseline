#!/usr/bin/env python3
"""Validate actual candidate snapshots; a workflow gate is not a security audit."""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
# No fixed system list. The template ships only infra/ and qa/ kits plus root;
# target projects use free-form areas. Legacy names are accepted for old branches.
LEGACY_SYSTEMS = ('backend', 'web', 'mobile', 'infra', 'qa', 'ai', 'mcp')
SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'coverage', 'dist', 'build', 'bin', 'obj'}
SECRETS = [
    ('private key', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    ('GitHub token', r'\bgh[pousr]_[A-Za-z0-9]{30,}\b'),
    ('AWS access key', r'\bAKIA[A-Z0-9]{16}\b'),
    ('provider key', r'\b[rs]k_(?:live|test)_[A-Za-z0-9]{16,}\b'),
    ('JWT-shaped value', r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b'),
]


def git(root, *args, required=True):
    r = subprocess.run(['git', *args], cwd=root, capture_output=True)
    if required and r.returncode:
        raise ValueError('Git command failed: ' + ' '.join(args[:3]) + '. Check history and refs.')
    return r.stdout if r.returncode == 0 else None


def snapshot(root, mode):
    if mode == 'template':
        files = {}
        for p in root.rglob('*'):
            rel = p.relative_to(root)
            if any(x in SKIP for x in rel.parts) or rel.parts[:2] in (('.husky', '_'), ('.baseline', 'local'), ('.coderabbit', 'raw')):
                continue
            if p.is_symlink():
                raise ValueError(f'Symlink requires a reviewed checker extension: {rel}')
            if p.is_file():
                files[rel.as_posix()] = p.read_bytes()
        return files
    staged = mode == 'staged'
    rows = git(root, *(['ls-files', '--stage', '-z'] if staged else ['ls-tree', '-rz', 'HEAD'])).split(b'\0')
    paths = []
    for row in filter(None, rows):
        meta, path = row.split(b'\t', 1)
        fields = meta.split()
        if fields[0] in (b'120000', b'160000') or (staged and fields[2] != b'0'):
            raise ValueError('Resolve conflicts/symlinks/submodules before validation.')
        paths.append(path.decode())
    return {p: git(root, 'show', (':' if staged else 'HEAD:') + p) for p in paths}


def discover_prefixes(files):
    prefixes = ['']
    for p in files:
        if p.endswith('/AGENTS.md'):
            prefix = p[: -len('AGENTS.md')]
            if prefix not in prefixes:
                prefixes.append(prefix)
    return sorted(set(prefixes))


def decoded(files):
    texts = {}
    for p, b in files.items():
        if b'\0' not in b:
            try:
                texts[p] = b.decode('utf-8')
            except UnicodeDecodeError:
                pass
    return texts


def load_json(texts, path, errors):
    try:
        value = json.loads(texts[path])
        if not isinstance(value, dict):
            raise ValueError('expected object')
        return value
    except (KeyError, ValueError):
        errors.append(path + ': missing or invalid JSON object')
        return {}


def check_structure(files):
    errors, texts = [], decoded(files)
    for p in ['AGENTS.md', 'START-HERE.md', 'package.json', 'research/project-brief.md', 'docs/planning/APPROVALS.md', 'docs/planning/CONTRACT-SYNC.md']:
        if p not in files:
            errors.append('Missing required file: ' + p)
    # .baseline/ is per-target-project state, created by scripts/configure.py.
    # The template master itself has no .baseline/ — that is expected.
    has_baseline = '.baseline/project.json' in texts
    if has_baseline:
        cfg = load_json(texts, '.baseline/project.json', errors)
        change = load_json(texts, '.baseline/change.json', errors)
    else:
        cfg, change = {'phase': 'template', 'name': 'baseline', 'areas': []}, {}
    if cfg.get('phase') not in ('template', 'planning', 'implementation'):
        errors.append('Unknown project phase')
    # Free-form areas: accept "areas" (new) or "systems" (legacy). Any slug allowed.
    areas = cfg.get('areas', cfg.get('systems', []))
    if has_baseline and not isinstance(areas, list):
        errors.append('areas must be a list of free-form area names')
        areas = []
    if has_baseline:
        if not all(isinstance(x, str) and x for x in areas):
            errors.append('areas must be unique non-empty strings')
            areas = []
        elif len(areas) != len(set(areas)):
            errors.append('areas must be unique non-empty strings')
            areas = []
    if has_baseline and not re.fullmatch(r'[a-z0-9][a-z0-9-]*', str(cfg.get('name', ''))):
        errors.append('Project name must be a lowercase slug')
    if has_baseline:
        for k in ('default_branch', 'remote'):
            if k in cfg and (not isinstance(cfg.get(k), str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*', cfg[k])):
                errors.append('Invalid ' + k)
    if cfg.get('phase') == 'implementation':
        ref = cfg.get('planning_approval')
        if not isinstance(ref, str) or ref.split('#')[0] not in files:
            errors.append('Implementation requires an existing planning_approval reference')
        command_map = cfg.get('commands', {})
        for s in areas:
            local = command_map.get(s, {}) if isinstance(command_map, dict) else {}
            for k in ('checks', 'security'):
                commands = local.get(k) if isinstance(local, dict) else None
                if commands is not None and (not isinstance(commands, list) or not commands):
                    errors.append(f'{s}: configure nonempty argument arrays for {k}')
    if has_baseline and cfg.get('phase') != 'implementation' and any(production_owner(p) for p in files):
        errors.append('Production source exists outside implementation phase')
    for p, data in files.items():
        if any(x in ('node_modules', 'App_Data', 'TestResults') for x in PurePosixPath(p).parts):
            errors.append(p + ': runtime artifact must not be versioned')
        name = PurePosixPath(p).name
        if name.startswith('.env') and name != '.env.example':
            errors.append(p + ': environment values must not be committed')
        if len(data) > 20 * 1024 * 1024:
            errors.append(p + ': exceeds 20 MiB; use reviewed artifact storage')
    for p, content in texts.items():
        for label, pattern in SECRETS:
            for m in re.finditer(pattern, content):
                line = content.count('\n', 0, m.start()) + 1
                errors.append(f'{p}:{line}: {label}; matched value redacted')
        if not p.endswith('.md'):
            continue
        without_code = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', content, flags=re.M | re.S)
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', without_code):
            target = target.strip().split(' "')[0].strip('<>')
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = target.split('#')[0]
            dest = posixpath.normpath(posixpath.join(posixpath.dirname(p), target))
            if target.startswith('/') or dest.startswith('../'):
                errors.append(f'{p}: nonportable local link {target}')
            elif dest not in files and not any(f.startswith(dest.rstrip('/') + '/') for f in files):
                errors.append(f'{p}: broken local link {target}')
        if p.endswith('/SKILL.md'):
            front = re.match(r'^---\n(.*?)\n---\n', content, re.S)
            if not front or not re.search(r'^name: [a-z0-9-]+$', front[1], re.M) or not re.search(r'^description: .+', front[1], re.M):
                errors.append(p + ': skill needs name and description frontmatter')
    prefixes = discover_prefixes(files)
    for prefix in prefixes:
        folder = prefix + 'project-kit/feature-specs/'
        specs = [p for p in files if p.startswith(folder) and re.fullmatch(r'\d{2,3}-[^/]+\.md', p[len(folder):])]
        ids = [p[len(folder):].split('-')[0] for p in specs]
        if len(ids) != len(set(ids)):
            errors.append(folder + ': duplicate feature IDs')
        for p in specs:
            for h in ['Outcome', 'Dependencies', 'Setup and initialization', 'Files owned and separation of concerns', 'Docker and deployment', 'Acceptance criteria']:
                if '## ' + h not in texts.get(p, ''):
                    errors.append(f'{p}: missing {h}')
        tracker = prefix + 'project-kit/context/progress-tracker.md'
        body = texts.get(tracker, '')
        section = body.split('## 0. Execution chain', 1)[-1].split('## 1.', 1)[0]
        blocks = re.findall(r'```text\n(.*?)\n```', section, re.S)
        token = r'\d{2,3}(?: [✅🟡📋⛔])?'
        if len(blocks) != 2 or any(not re.fullmatch(rf'{token}(?: → {token})*|Done', b) for b in blocks):
            errors.append(tracker + ': Full and Next must be two ID-only text fences')
        else:
            full, nxt = (re.findall(r'\d{2,3}', b) for b in blocks)
            if sorted(full) != sorted(ids) or len(full) != len(set(full)):
                errors.append(tracker + ': Full chain must contain each local spec exactly once')
            if any(x not in full for x in nxt) or len(nxt) != len(set(nxt)):
                errors.append(tracker + ': Next contains unknown or duplicate IDs')
            if sorted(re.findall(r'^\| (\d{2,3}) \|', body, re.M)) != sorted(ids):
                errors.append(tracker + ': status board must contain each local spec exactly once')
    return errors, cfg, change


def production_owner(path):
    parts = PurePosixPath(path).parts
    if len(parts) < 2:
        return None
    # Template-owned planning locations are never production.
    if parts[1] in ('project-kit', '.agents', 'AGENTS.md', 'README.md'):
        return None
    if parts[0] in ('docs', 'research', 'templates', 'scripts', 'bugs', 'inspo', '.agents', '.github', '.husky', '.coderabbit'):
        return None
    # infra/ and qa/ production paths are owned; any other top-level folder in a
    # target project is treated as the user's own area (free-form, not template-owned).
    if parts[0] in ('infra', 'qa'):
        return parts[0]
    return None


def check_scope(files, cfg, change, changed, branch, bootstrap=False):
    errors = []
    if not change:
        return []  # template master has no .baseline/change.json; scope checks apply to target branches
    system, spec = change.get('system'), change.get('spec')
    valid_systems = {'root', *LEGACY_SYSTEMS}
    # Also accept free-form areas from config and discovered kit prefixes.
    for a in (cfg.get('areas') or cfg.get('systems') or []):
        if isinstance(a, str) and a:
            valid_systems.add(a)
    for p in files:
        if p.endswith('/AGENTS.md') and len(PurePosixPath(p).parts) == 2:
            valid_systems.add(PurePosixPath(p).parts[0])
    if system not in valid_systems or not isinstance(spec, str) or not re.fullmatch(r'\d{2,3}', spec):
        return ['change.json must identify one area and two/three-digit spec ID']
    prefix = '' if system == 'root' else system + '/'
    tracker = prefix + 'project-kit/context/progress-tracker.md'
    owning_specs = [p for p in files if p.startswith(prefix + 'project-kit/feature-specs/' + spec + '-') and p.endswith('.md')]
    if len(owning_specs) != 1:
        errors.append('Change scope must identify exactly one existing owning spec')
    if not bootstrap and not re.fullmatch(rf'(feature|fix|docs)/{system}/{spec}-[a-z0-9-]+', branch):
        errors.append(f'Branch must be feature|fix|docs/{system}/{spec}-<slug>, matching change.json')
    if changed and tracker not in changed:
        errors.append('Update owning tracker in this candidate change: ' + tracker)
    owners = {production_owner(p) for p in changed} - {None}
    if owners:
        if cfg.get('phase') != 'implementation':
            errors.append('Production changes require implementation phase and approved planning')
        if owners != {system} and system != 'root':
            errors.append('Production change crosses owning area boundary')
        if not any(p in changed for p in owning_specs):
            errors.append('Production change requires the owning spec to be updated')
    for flag in ('contract_changed', 'schema_changed', 'ui_changed'):
        if not isinstance(change.get(flag), bool):
            errors.append(flag + ' must be an explicit boolean')
    fields = ('required_docs', 'contract_docs', 'consumer_docs', 'approval_refs')
    for f in fields:
        if not isinstance(change.get(f), list) or not all(isinstance(x, str) and x for x in change[f]):
            errors.append(f + ' must be a list of paths')
    if any(not isinstance(change.get(f), list) or not all(isinstance(x, str) for x in change[f]) for f in fields):
        return errors
    required = change['required_docs'][:]
    if change.get('contract_changed'):
        if not change['contract_docs']:
            errors.append('Contract change requires canonical contract_docs')
        if not change['consumer_docs'] and not str(change.get('no_consumers_reason', '')).strip():
            errors.append('Contract change needs consumer_docs or an explicit no-consumers reason')
        required += change['contract_docs'] + change['consumer_docs']
    for ref in required:
        p = ref.split('#')[0]
        if p not in files or p not in changed:
            errors.append('Required synchronized document missing or unchanged: ' + p)
    if (owners or change.get('schema_changed') or change.get('ui_changed')) and not change['approval_refs']:
        errors.append('Implementation/schema/UI change requires actual approval references')
    for ref in change['approval_refs']:
        if ref.split('#')[0] not in files:
            errors.append('Missing approval record: ' + ref)
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('template', 'staged', 'branch'), default='template')
    parser.add_argument('--base')
    args = parser.parse_args(argv)
    try:
        files = snapshot(ROOT, args.mode)
        errors, cfg, change = check_structure(files)
        changed = set()
        if args.mode != 'template' and not errors:
            bootstrap = git(ROOT, 'rev-parse', '--verify', 'HEAD', required=False) is None
            if args.mode == 'branch' and bootstrap:
                raise ValueError('Branch validation needs a committed snapshot')
            branch = os.environ.get('BASELINE_BRANCH') or git(ROOT, 'branch', '--show-current').decode().strip()
            if args.mode == 'staged':
                changed = set(filter(None, git(ROOT, 'diff', '--cached', '--name-only', '--no-renames', '-z').decode().split('\0')))
            else:
                if git(ROOT, 'status', '--porcelain').strip():
                    errors.append('Branch checks require a clean tree so runtime checks match HEAD')
                base_ref = args.base or cfg['remote'] + '/' + cfg['default_branch']
                initial_push = (not args.base and branch == cfg['default_branch']
                                and cfg['phase'] in ('template', 'planning')
                                and git(ROOT, 'rev-list', '--count', 'HEAD').strip() == b'1'
                                and git(ROOT, 'rev-parse', '--verify', base_ref, required=False) is None)
                if initial_push:
                    bootstrap, changed, commits, refs = True, set(files), set(), []
                else:
                    base = git(ROOT, 'merge-base', 'HEAD', base_ref).decode().strip()
                    changed = set(filter(None, git(ROOT, 'diff', '--name-only', '--no-renames', '-z', base, 'HEAD').decode().split('\0')))
                    commits = set(git(ROOT, 'rev-list', base + '..HEAD').decode().splitlines())
                    refs = git(ROOT, 'for-each-ref', '--format=%(refname:short)', 'refs/remotes').decode().splitlines()
                for ref in refs:
                    if ref in (cfg['remote'] + '/' + branch, base_ref, cfg['remote'] + '/' + cfg['default_branch']) or ref.endswith('/HEAD'):
                        continue
                    others = set(git(ROOT, 'rev-list', base_ref + '..' + ref).decode().splitlines())
                    if commits & others:
                        errors.append('Unmerged commit overlap with ' + ref + '; check branch provenance')
            errors += check_scope(files, cfg, change, changed, branch, bootstrap)
            if bootstrap and cfg.get('phase') == 'implementation':
                errors.append('Bootstrap exception is planning/template only')
        if errors:
            for e in errors:
                print('FAIL:', e)
            return 1
        if args.mode == 'branch' and cfg.get('phase') == 'implementation':
            for owner in sorted({production_owner(p) for p in changed} - {None}):
                for kind in ('checks', 'security'):
                    for command in cfg['commands'][owner][kind]:
                        print(f'RUN {owner} {kind}: {command[0]}', flush=True)
                        subprocess.run(command, cwd=ROOT / owner, check=True)
        print(f'PASS: {args.mode} workflow checks ({len(files)} files). Product acceptance and human approvals need separate evidence.')
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL:', str(error))
        return 1


if __name__ == '__main__':
    sys.exit(main())
