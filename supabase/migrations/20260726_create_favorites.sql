create table if not exists public.shared_favorites (
  project_key text not null,
  created_at timestamptz not null default now(),
  primary key (project_key)
);

alter table public.shared_favorites enable row level security;
revoke all on public.shared_favorites from anon, authenticated;
