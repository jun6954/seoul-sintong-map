import unittest
from pathlib import Path


SQL = (
    Path(__file__).resolve().parents[1]
    / "supabase/migrations/20260726_create_favorites.sql"
).read_text()


class FavoritesMigrationTests(unittest.TestCase):
    def test_favorites_table_is_user_scoped_and_protected_by_rls(self):
        self.assertIn("create table if not exists public.favorites", SQL)
        self.assertIn("primary key (user_id, project_key)", SQL)
        self.assertIn("alter table public.favorites enable row level security", SQL)
        self.assertEqual(SQL.count("(select auth.uid()) = user_id"), 3)
        self.assertIn("for select", SQL)
        self.assertIn("for insert", SQL)
        self.assertIn("for delete", SQL)
