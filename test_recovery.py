import unittest
from dataclasses import replace
from recovery import SCENARIOS, evaluate

class TestRecovery(unittest.TestCase):
    def test_success(self):
        self.assertEqual(evaluate(SCENARIOS['Successful pickup'])[0], 'CONTINUE_TO_PRESS')
    def test_retry(self):
        self.assertEqual(evaluate(SCENARIOS['Failed pickup — approved retry'])[0], 'SIMULATED_RETRY_ELIGIBLE')
    def test_block(self):
        self.assertEqual(evaluate(SCENARIOS['Failed pickup — unsafe/unknown'])[0], 'BLOCK_AND_INSPECT')
    def test_retry_limit(self):
        self.assertEqual(evaluate(SCENARIOS['Failed pickup — retry limit reached'])[0], 'BLOCK_AND_INSPECT')
    def test_wrong_tool_blocks(self):
        s = replace(SCENARIOS['Successful pickup'], tool_ok=False)
        self.assertEqual(evaluate(s)[0], 'BLOCK_AND_INSPECT')
    def test_missing_approval_blocks(self):
        s = replace(SCENARIOS['Failed pickup — approved retry'], operator_approved=False)
        self.assertEqual(evaluate(s)[0], 'BLOCK_AND_INSPECT')

if __name__ == '__main__':
    unittest.main()
