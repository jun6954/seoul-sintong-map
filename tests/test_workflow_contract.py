import unittest
from pathlib import Path


WORKFLOW = (
    Path(__file__).resolve().parents[1] / ".github/workflows/sync-data.yml"
).read_text()


class WorkflowContractTests(unittest.TestCase):
    def test_data_sync_schedule_remains_enabled_while_telegram_is_opt_in(self):
        self.assertIn('cron: "15 20 * * *"', WORKFLOW)
        self.assertIn("python scripts/fetch_general_projects.py --with-geometry", WORKFLOW)
        self.assertIn("vars.TELEGRAM_NOTIFICATIONS_ENABLED == 'true'", WORKFLOW)
        self.assertIn("TELEGRAM_BOT_TOKEN", WORKFLOW)
