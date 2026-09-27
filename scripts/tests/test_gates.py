"""Behavioral checks for real failure modes in the workflow gate."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('baseline_check', ROOT / 'scripts/check.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = gate.snapshot(ROOT, 'template')

    def modified(self, path, content):
        files = self.files.copy()
        files[path] = content.encode()
        return files

    def test_template_has_no_broken_contract_structure(self):
        self.assertEqual(gate.check_structure(self.files)[0], [])

    def test_missing_local_link_is_rejected(self):
        errors, _, _ = gate.check_structure(self.modified('README.md', '[Missing](missing.md)'))
        self.assertTrue(any('broken local link' in e for e in errors))

    def test_outside_repository_link_is_rejected(self):
        errors, _, _ = gate.check_structure(self.modified('README.md', '[Private](/home/someone/private.md)'))
        self.assertTrue(any('nonportable' in e for e in errors))

    def test_duplicate_feature_is_rejected(self):
        files = self.files.copy()
        files['qa/project-kit/feature-specs/01-duplicate.md'] = files['qa/project-kit/feature-specs/01-planning-foundation.md']
        self.assertTrue(any('duplicate feature' in e for e in gate.check_structure(files)[0]))

    def test_chain_cannot_hide_an_unregistered_feature(self):
        path = 'qa/project-kit/context/progress-tracker.md'
        body = self.files[path].decode().replace('01\n```', '01 → 99\n```', 1)
        self.assertTrue(any('each local spec' in e for e in gate.check_structure(self.modified(path, body))[0]))

    def test_research_secret_is_detected_without_echoing_it(self):
        secret = 'ghp_' + 'A' * 36
        errors = gate.check_structure(self.modified('research/leak.md', secret))[0]
        self.assertTrue(any('GitHub token' in e for e in errors))
        self.assertNotIn(secret, '\n'.join(errors))

    def test_environment_file_is_rejected(self):
        errors = gate.check_structure(self.modified('qa/.env.production', 'VALUE=anything'))[0]
        self.assertTrue(any('environment values' in e for e in errors))

    def test_implementation_requires_real_gate_configuration(self):
        files = self.files.copy()
        cfg = {'name': 'demo', 'phase': 'implementation', 'areas': ['infra'],
               'default_branch': 'main', 'remote': 'origin'}
        files['.baseline/project.json'] = json.dumps(cfg).encode()
        files['.baseline/change.json'] = json.dumps({'system': 'root', 'spec': '01'}).encode()
        errors = gate.check_structure(files)[0]
        self.assertTrue(any('planning_approval' in e for e in errors))

    def test_production_cannot_hide_inside_a_planning_snapshot(self):
        files = self.files.copy()
        files['.baseline/project.json'] = json.dumps({'name': 'demo', 'phase': 'planning', 'areas': []}).encode()
        files['.baseline/change.json'] = json.dumps({'system': 'root', 'spec': '01'}).encode()
        files['infra/src/app.ts'] = b'export const app = 1;'
        errors = gate.check_structure(files)[0]
        self.assertTrue(any('outside implementation phase' in e for e in errors))

    def test_malformed_area_configuration_fails_cleanly(self):
        files = self.files.copy()
        files['.baseline/project.json'] = json.dumps({'name': 'demo', 'phase': 'planning', 'areas': [{'bad': True}]}).encode()
        files['.baseline/change.json'] = json.dumps({'system': 'root', 'spec': '01'}).encode()
        self.assertTrue(gate.check_structure(files)[0])


class ScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = gate.snapshot(ROOT, 'template')

    def scope(self, changed, **updates):
        files = self.files.copy()
        cfg = {'name': 'demo', 'phase': 'planning', 'areas': [], 'default_branch': 'main', 'remote': 'origin'}
        change = {'system': 'root', 'spec': '01', 'contract_changed': False,
                  'schema_changed': False, 'ui_changed': False, 'required_docs': [],
                  'contract_docs': [], 'consumer_docs': [], 'approval_refs': []}
        change.update(updates)
        return gate.check_scope(files, cfg, change, set(changed), 'feature/root/01-planning')

    def test_tracker_must_travel_with_the_change(self):
        self.assertTrue(any('tracker' in e for e in self.scope(['README.md'])))

    def test_contract_consumers_must_be_updated(self):
        errors = self.scope(['project-kit/context/progress-tracker.md'], contract_changed=True,
                            contract_docs=['docs/contracts/README.md'], consumer_docs=['qa/project-kit/context/integration-contracts.md'])
        self.assertEqual(sum('missing or unchanged' in e for e in errors), 2)

    def test_contract_without_consumers_needs_reason(self):
        errors = self.scope(['project-kit/context/progress-tracker.md', 'docs/contracts/README.md'],
                            contract_changed=True, contract_docs=['docs/contracts/README.md'])
        self.assertTrue(any('no-consumers' in e for e in errors))

    def test_unapproved_production_is_rejected(self):
        errors = self.scope(['infra/src/app.ts', 'project-kit/context/progress-tracker.md'])
        self.assertTrue(any('implementation phase' in e for e in errors))

    def test_schema_change_requires_approval(self):
        self.assertTrue(any('approval references' in e for e in self.scope(['project-kit/context/progress-tracker.md'], schema_changed=True)))

    def test_a_documented_planning_change_passes(self):
        self.assertEqual(self.scope(['README.md', 'project-kit/context/progress-tracker.md']), [])


class GitSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='baseline-gate-test-')
        self.root = Path(self.temp.name)
        for name, data in gate.snapshot(ROOT, 'template').items():
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        # Per-target state (absent in template master) so scope/branch checks apply.
        bdir = self.root / '.baseline'
        bdir.mkdir(parents=True, exist_ok=True)
        (bdir / 'project.json').write_text(json.dumps({'name': 'demo', 'phase': 'planning', 'areas': [], 'default_branch': 'main', 'remote': 'origin'}))
        (bdir / 'change.json').write_text(json.dumps({'system': 'root', 'spec': '01', 'contract_changed': False, 'schema_changed': False, 'ui_changed': False, 'required_docs': [], 'contract_docs': [], 'consumer_docs': [], 'approval_refs': []}))
        self.run_git('init', '-b', 'main')
        self.run_git('config', 'user.name', 'Template Test')
        self.run_git('config', 'user.email', 'template-test@example.invalid')
        self.run_git('config', 'commit.gpgsign', 'false')
        self.run_git('add', '.')

    def tearDown(self):
        self.temp.cleanup()

    def run_git(self, *args):
        return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null', *args], cwd=self.root, stderr=subprocess.DEVNULL).decode().strip()

    def run_gate(self, *args):
        old_root = gate.ROOT
        old_env = os.environ.pop('BASELINE_BRANCH', None)
        gate.ROOT = self.root
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                code = gate.main(list(args))
            return code, output.getvalue()
        finally:
            gate.ROOT = old_root
            if old_env is not None:
                os.environ['BASELINE_BRANCH'] = old_env

    def commit_base(self):
        self.run_git('commit', '-m', 'Initial planning scaffold')
        self.run_git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        self.run_git('switch', '-c', 'feature/root/01-planning')

    def change_tracker(self):
        p = self.root / 'project-kit/context/progress-tracker.md'
        p.write_text(p.read_text().replace('No implementation is authorized.', 'Planning review is in progress.'))
        self.run_git('add', str(p.relative_to(self.root)))

    def test_bootstrap_snapshot_passes(self):
        code, output = self.run_gate('--mode', 'staged')
        self.assertEqual(code, 0, output)

    def test_initial_planning_push_is_allowed_without_remote_history(self):
        self.run_git('commit', '-m', 'Initial planning scaffold')
        code, output = self.run_gate('--mode', 'branch')
        self.assertEqual(code, 0, output)

    def test_configured_runtime_failure_blocks_push(self):
        self.commit_base()
        self.run_git('switch', '-c', 'feature/infra/01-foundation')
        config_path = self.root / '.baseline/project.json'
        cfg = json.loads(config_path.read_text())
        cfg.update(phase='implementation', areas=['infra'], planning_approval='docs/planning/APPROVALS.md')
        cfg.setdefault('commands', {})['infra'] = {'checks': [[sys.executable, '-c', 'raise SystemExit(7)']],
                                  'security': [[sys.executable, '-c', 'raise SystemExit(0)']]}
        config_path.write_text(json.dumps(cfg))
        change_path = self.root / '.baseline/change.json'
        change = json.loads(change_path.read_text())
        change.update(system='infra', spec='01', approval_refs=['docs/planning/APPROVALS.md'])
        change_path.write_text(json.dumps(change))
        for name in ['infra/project-kit/context/progress-tracker.md', 'infra/project-kit/feature-specs/01-planning-foundation.md']:
            p = self.root / name
            p.write_text(p.read_text() + '\nRuntime verification fixture.\n')
        source = self.root / 'infra/src/app.txt'
        source.parent.mkdir(exist_ok=True)
        source.write_text('Synthetic production fixture')
        self.run_git('add', '.')
        self.run_git('commit', '-m', 'Runtime fixture')
        code, output = self.run_gate('--mode', 'branch')
        self.assertEqual(code, 1)
        self.assertIn('RUN infra checks', output)
        self.assertIn('exit status 7', output)

    def test_unstaged_fix_cannot_hide_a_staged_secret(self):
        self.commit_base()
        secret = 'ghp_' + 'B' * 36
        p = self.root / 'research/secret.md'
        p.write_text(secret)
        self.run_git('add', 'research/secret.md')
        p.write_text('Clean working copy, but index still contains the secret.')
        self.change_tracker()
        code, output = self.run_gate('--mode', 'staged')
        self.assertEqual(code, 1)
        self.assertIn('GitHub token', output)
        self.assertNotIn(secret, output)

    def test_missing_tracker_commit_fails(self):
        self.commit_base()
        p = self.root / 'README.md'
        p.write_text(p.read_text() + '\nA planning clarification.\n')
        self.run_git('add', 'README.md')
        code, output = self.run_gate('--mode', 'staged')
        self.assertEqual(code, 1)
        self.assertIn('tracker', output)

    def test_committed_branch_passes_then_dirty_tree_fails(self):
        self.commit_base()
        self.change_tracker()
        self.run_git('commit', '-m', 'Record planning review')
        code, output = self.run_gate('--mode', 'branch')
        self.assertEqual(code, 0, output)
        (self.root / 'README.md').write_text('Uncommitted change')
        code, output = self.run_gate('--mode', 'branch')
        self.assertEqual(code, 1)
        self.assertIn('clean tree', output)

    def test_unmerged_remote_branch_overlap_is_rejected(self):
        self.commit_base()
        self.change_tracker()
        self.run_git('commit', '-m', 'Record planning review')
        self.run_git('update-ref', 'refs/remotes/origin/feature/root/02-other', 'HEAD')
        code, output = self.run_gate('--mode', 'branch')
        self.assertEqual(code, 1)
        self.assertIn('Unmerged commit overlap', output)

    def test_wrong_branch_cannot_claim_the_feature(self):
        self.commit_base()
        self.run_git('switch', '-c', 'feature/root/02-wrong')
        self.change_tracker()
        code, output = self.run_gate('--mode', 'staged')
        self.assertEqual(code, 1)
        self.assertIn('matching change.json', output)


if __name__ == '__main__':
    unittest.main()
