-- Supabase SQL schema for WhatsApp Product Review Collector
create table if not exists public.reviews (
    id uuid primary key default gen_random_uuid(),
    contact_number text not null,
    user_name text not null,
    product_name text not null,
    product_review text not null,
    created_at timestamptz not null default timezone('utc', now())
);

create index if not exists reviews_contact_number_idx on public.reviews (contact_number);
create index if not exists reviews_created_at_idx on public.reviews (created_at desc);

