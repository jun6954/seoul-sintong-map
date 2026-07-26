import unittest
from pathlib import Path


SQL = (
    Path(__file__).resolve().parents[1]
    / "supabase/migrations/20260726_create_favorites.sql"
).read_text()


class FavoritesMigrationTests(unittest.TestCase):
    def test_shared_favorites_are_not_exposed_through_the_database_api(self):
        self.assertIn("create table if not exists public.shared_favorites", SQL)
        self.assertIn("primary key (project_key)", SQL)
        self.assertIn("alter table public.shared_favorites enable row level security", SQL)
        self.assertIn("revoke all on public.shared_favorites from anon, authenticated", SQL)
