create table if not exists public.favorites (
  user_id uuid not null references auth.users(id) on delete cascade,
  project_key text not null,
  created_at timestamptz not null default now(),
  primary key (user_id, project_key)
);

alter table public.favorites enable row level security;

drop policy if exists "Users can view their own favorites" on public.favorites;
create policy "Users can view their own favorites"
  on public.favorites for select
  to authenticated
  using ((select auth.uid()) = user_id);

drop policy if exists "Users can add their own favorites" on public.favorites;
create policy "Users can add their own favorites"
  on public.favorites for insert
  to authenticated
  with check ((select auth.uid()) = user_id);

drop policy if exists "Users can delete their own favorites" on public.favorites;
create policy "Users can delete their own favorites"
  on public.favorites for delete
  to authenticated
  using ((select auth.uid()) = user_id);
