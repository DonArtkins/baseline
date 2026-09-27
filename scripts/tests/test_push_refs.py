import importlib.util
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('baseline_push', SCRIPTS / 'pre_push.py')
push = importlib.util.module_from_spec(spec)
spec.loader.exec_module(push)


class PushRefTests(unittest.TestCase):
    def test_matching_branch_is_allowed(self):
        branch = 'feature/web/01-screen'
        row = f'refs/heads/{branch} abc refs/heads/{branch} def'
        self.assertEqual(push.validate_updates([row], branch, 'abc'), [])

    def test_feature_cannot_be_pushed_to_main_by_refspec(self):
        branch = 'feature/web/01-screen'
        row = f'refs/heads/{branch} abc refs/heads/main def'
        self.assertTrue(push.validate_updates([row], branch, 'abc'))

    def test_other_commit_cannot_escape_head_validation(self):
        branch = 'feature/web/01-screen'
        row = f'refs/heads/{branch} other refs/heads/{branch} def'
        self.assertTrue(push.validate_updates([row], branch, 'abc'))

    def test_deletion_is_not_a_feature_push(self):
        self.assertTrue(push.validate_updates(['(delete) 000 refs/heads/old abc'], 'feature/web/01-screen', 'abc'))
