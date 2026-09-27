#!/usr/bin/env python3
"""Restrict this feature hook to the current branch and its matching remote ref."""
import subprocess
import sys
import check


def validate_updates(lines, branch, head):
    errors = []
    for line in lines:
        fields = line.split()
        if len(fields) != 4:
            errors.append('Invalid pre-push ref record')
            continue
        local_ref, local_sha, remote_ref, _ = fields
        expected = 'refs/heads/' + branch
        if local_ref != expected or local_sha != head or remote_ref != expected:
            errors.append('Push only the current feature to its matching remote branch; other refs/deletions need a separate reviewed operation')
    return errors


def main():
    try:
        branch = check.git(check.ROOT, 'branch', '--show-current').decode().strip()
        head = check.git(check.ROOT, 'rev-parse', 'HEAD').decode().strip()
        errors = validate_updates(sys.stdin.read().splitlines(), branch, head)
        if errors:
            for error in errors:
                print('FAIL:', error)
            return 1
        return check.main(['--mode', 'branch'])
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL:', error)
        return 1


if __name__ == '__main__':
    sys.exit(main())
