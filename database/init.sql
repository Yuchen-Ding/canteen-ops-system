create schema if not exists canteen_ops;

create table if not exists canteen_ops.migration_history (
    id bigserial primary key,
    version varchar(50) not null unique,
    description varchar(255) not null,
    applied_at timestamptz not null default now()
);

create table if not exists canteen_ops.system_info (
    id bigserial primary key,
    system_name varchar(120) not null,
    app_version varchar(50) not null,
    app_env varchar(30) not null,
    ai_provider varchar(50) not null default 'mock',
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

insert into canteen_ops.migration_history (version, description)
values ('0001', 'stage 0 baseline schema')
on conflict (version) do nothing;

insert into canteen_ops.system_info (system_name, app_version, app_env, ai_provider)
select 'Enterprise Canteen Operations System', '0.1.0', 'bootstrap', 'mock'
where not exists (select 1 from canteen_ops.system_info);
