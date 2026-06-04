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

create table if not exists canteen_ops.canteens (
    id bigserial primary key,
    canteen_code varchar(50) not null unique,
    name varchar(120) not null,
    city varchar(80) not null,
    location varchar(255) not null,
    status varchar(30) not null default 'ACTIVE',
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.stalls (
    id bigserial primary key,
    stall_code varchar(50) not null unique,
    canteen_id bigint not null references canteen_ops.canteens(id),
    name varchar(120) not null,
    category varchar(80) not null,
    floor varchar(50),
    status varchar(30) not null default 'ACTIVE',
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.dishes (
    id bigserial primary key,
    dish_code varchar(50) not null unique,
    stall_id bigint not null references canteen_ops.stalls(id),
    name varchar(120) not null,
    category varchar(80) not null,
    unit_price numeric(10, 2) not null,
    is_available boolean not null default true,
    status varchar(30) not null default 'ACTIVE',
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.meal_packages (
    id bigserial primary key,
    package_code varchar(50) not null unique,
    stall_id bigint not null references canteen_ops.stalls(id),
    name varchar(120) not null,
    package_price numeric(10, 2) not null,
    status varchar(30) not null default 'ACTIVE',
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.meal_package_items (
    id bigserial primary key,
    package_id bigint not null references canteen_ops.meal_packages(id),
    dish_id bigint not null references canteen_ops.dishes(id),
    quantity integer not null default 1,
    created_at timestamptz not null default now(),
    unique (package_id, dish_id)
);

create table if not exists canteen_ops.employees (
    id bigserial primary key,
    employee_no varchar(50) not null unique,
    name varchar(120) not null,
    department varchar(120) not null,
    employee_type varchar(30) not null,
    card_no varchar(80) unique,
    phone varchar(40),
    status varchar(30) not null default 'ACTIVE',
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.visitors (
    id bigserial primary key,
    visitor_no varchar(50) not null unique,
    name varchar(120) not null,
    phone varchar(40),
    company varchar(120),
    status varchar(30) not null default 'ACTIVE',
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.devices (
    id bigserial primary key,
    device_code varchar(50) not null unique,
    device_name varchar(120) not null,
    canteen_id bigint not null references canteen_ops.canteens(id),
    stall_id bigint references canteen_ops.stalls(id),
    device_type varchar(30) not null,
    ip_address varchar(60),
    location varchar(255),
    status varchar(30) not null default 'OFFLINE',
    last_heartbeat_time timestamptz,
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_stalls_canteen_id on canteen_ops.stalls(canteen_id);
create index if not exists idx_dishes_stall_id on canteen_ops.dishes(stall_id);
create index if not exists idx_meal_packages_stall_id on canteen_ops.meal_packages(stall_id);
create index if not exists idx_meal_package_items_package_id on canteen_ops.meal_package_items(package_id);
create index if not exists idx_meal_package_items_dish_id on canteen_ops.meal_package_items(dish_id);
create index if not exists idx_devices_canteen_id on canteen_ops.devices(canteen_id);
create index if not exists idx_devices_stall_id on canteen_ops.devices(stall_id);

insert into canteen_ops.migration_history (version, description)
values ('0002', 'stage 1 master data schema')
on conflict (version) do nothing;
