import os
from os import path

from django.test import TestCase
# TODO: To be removed when we drop python 2.7 support
# Mock is a standard library from python3.3-pre onwards
# from unittest.mock import patch
from mock import patch
from openwisp_utils.qa import check_commit_message, check_migration_name

MIGRATIONS_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'migrations')


class TestQa(TestCase):
    _test_migration_file = '%s/0002_auto_20181001_0421.py' % MIGRATIONS_DIR

    def setUp(self):
        # Create a fake migration file with default name
        open(self._test_migration_file, 'w').close()

    def test_qa_call_check_migration_name_pass(self):
        options = [
            'checkmigrations', '--migrations-to-ignore', '2',
            '--migration-path', MIGRATIONS_DIR
        ]
        with patch('argparse._sys.argv', options):
            check_migration_name()

    def test_qa_call_check_migration_name_failure(self):
        options = [
            [
                'checkmigrations', '--migrations-to-ignore', '1',
                '--migration-path', MIGRATIONS_DIR
            ],
            ['checkmigrations', '--migration-path', MIGRATIONS_DIR],
            ['checkmigrations']
        ]
        for option in options:
            with patch('argparse._sys.argv', option):
                try:
                    check_migration_name()
                except (SystemExit, Exception):
                    pass
                else:
                    self.fail('SystemExit or Exception not raised')

    def test_qa_call_check_commit_message_pass(self):
        options = [
            [
                'commitcheck',
                '--message',
                "[qa] Minor clean up operations"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Updated more file and fix problem #20\n\n"
                "Added more files Fixes #20"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Improved Y #2\n\n"
                "Related to #2"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Finished task #2\n\n"
                "Closes #2\nRelated to #1"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Finished task #2\n\n"
                "Related to #2\nCloses #1"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Finished task #2\n\n"
                "Related to #2\nRelated to #1"
            ]
        ]
        for option in options:
            with patch('argparse._sys.argv', option):
                check_commit_message()

    def test_qa_call_check_commit_message_failure(self):
        options = [
            ['commitcheck'],
            [
                'commitcheck',
                '--message',
                'Hello World',
            ],
            [
                'commitcheck',
                '--message',
                '[qa] hello World',
            ],
            [
                'commitcheck',
                '--message',
                '[qa] Hello World.',
            ],
            [
                'commitcheck',
                '--message',
                '[qa] Hello World.\nFixes #20',
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Updated more file and fix problem #20"
                "\n\nAdded more files #20"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Finished task #2\n\n"
                "Failure #2\nRelated to #1"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Finished task\n\n"
                "Failure #2\nRelated to #1"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Updated more file and fix problem\n\n"
                "Added more files Fixes #20"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Improved Y\n\n"
                "Related to #2"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Improved Y #2\n\n"
                "Updated files"
            ],
            [
                'commitcheck',
                '--message',
                "[qa] Improved Y #20\n\n"
                "Related to #32 Fixes #30 Fix #40"
            ],
        ]
        for option in options:
            with patch('argparse._sys.argv', option):
                try:
                    check_commit_message()
                except (SystemExit, Exception):
                    pass
                else:
                    self.fail('SystemExit or Exception not raised')

    def tearDown(self):
        os.unlink(self._test_migration_file)
