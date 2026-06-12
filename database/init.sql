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

create table if not exists canteen_ops.orders (
    id bigserial primary key,
    order_no varchar(60) not null unique,
    canteen_id bigint not null references canteen_ops.canteens(id),
    stall_id bigint not null references canteen_ops.stalls(id),
    device_id bigint not null references canteen_ops.devices(id),
    customer_type varchar(30) not null,
    employee_id bigint references canteen_ops.employees(id),
    visitor_id bigint references canteen_ops.visitors(id),
    visitor_name_snapshot varchar(120),
    meal_type varchar(30) not null,
    original_amount numeric(12, 2) not null,
    discount_amount numeric(12, 2) not null default 0,
    subsidy_amount numeric(12, 2) not null default 0,
    payable_amount numeric(12, 2) not null,
    payment_status varchar(30) not null default 'PENDING',
    order_status varchar(30) not null default 'CREATED',
    transaction_time timestamptz not null default now(),
    operator varchar(120),
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint chk_orders_customer_ref check (
        (customer_type = 'EMPLOYEE' and employee_id is not null and visitor_id is null)
        or
        (customer_type = 'VISITOR' and employee_id is null)
    ),
    constraint chk_orders_amount check (payable_amount = original_amount - discount_amount - subsidy_amount)
);

create table if not exists canteen_ops.order_items (
    id bigserial primary key,
    order_id bigint not null references canteen_ops.orders(id),
    dish_id bigint references canteen_ops.dishes(id),
    item_type varchar(30) not null,
    item_name_snapshot varchar(120) not null,
    quantity integer not null,
    unit_price numeric(12, 2) not null,
    amount numeric(12, 2) not null,
    created_at timestamptz not null default now(),
    constraint chk_order_items_quantity check (quantity > 0),
    constraint chk_order_items_amount check (amount = quantity * unit_price)
);

create table if not exists canteen_ops.payments (
    id bigserial primary key,
    payment_no varchar(60) not null unique,
    order_id bigint not null unique references canteen_ops.orders(id),
    payment_method varchar(30) not null,
    payment_amount numeric(12, 2) not null,
    payment_status varchar(30) not null default 'PENDING',
    paid_at timestamptz,
    failure_reason varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_orders_canteen_id on canteen_ops.orders(canteen_id);
create index if not exists idx_orders_stall_id on canteen_ops.orders(stall_id);
create index if not exists idx_orders_device_id on canteen_ops.orders(device_id);
create index if not exists idx_orders_employee_id on canteen_ops.orders(employee_id);
create index if not exists idx_orders_visitor_id on canteen_ops.orders(visitor_id);
create index if not exists idx_orders_transaction_time on canteen_ops.orders(transaction_time);
create index if not exists idx_order_items_order_id on canteen_ops.order_items(order_id);
create index if not exists idx_order_items_dish_id on canteen_ops.order_items(dish_id);
create index if not exists idx_payments_order_id on canteen_ops.payments(order_id);
create index if not exists idx_payments_paid_at on canteen_ops.payments(paid_at);

insert into canteen_ops.migration_history (version, description)
values ('0003', 'stage 2 transaction baseline schema')
on conflict (version) do nothing;

create table if not exists canteen_ops.refunds (
    id bigserial primary key,
    refund_no varchar(60) not null unique,
    order_id bigint not null unique references canteen_ops.orders(id),
    payment_id bigint not null unique references canteen_ops.payments(id),
    refund_amount numeric(12, 2) not null,
    refund_reason varchar(500) not null,
    refund_status varchar(30) not null default 'PENDING',
    requested_by varchar(120) not null,
    refunded_at timestamptz,
    failure_reason varchar(500),
    remark varchar(500),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint chk_refunds_amount check (refund_amount > 0)
);

create index if not exists idx_refunds_status on canteen_ops.refunds(refund_status);
create index if not exists idx_refunds_created_at on canteen_ops.refunds(created_at);
create index if not exists idx_refunds_refunded_at on canteen_ops.refunds(refunded_at);

insert into canteen_ops.migration_history (version, description)
values ('0004', 'stage 3 refund and reporting baseline')
on conflict (version) do nothing;

create table if not exists canteen_ops.ai_chat_sessions (
    id bigserial primary key,
    session_no varchar(60) not null unique,
    title varchar(200) not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists canteen_ops.ai_chat_messages (
    id bigserial primary key,
    session_id bigint not null references canteen_ops.ai_chat_sessions(id),
    role varchar(30) not null,
    content text not null,
    created_at timestamptz not null default now()
);

create index if not exists idx_ai_chat_messages_session_id
    on canteen_ops.ai_chat_messages(session_id);
create index if not exists idx_ai_chat_messages_created_at
    on canteen_ops.ai_chat_messages(created_at);

insert into canteen_ops.migration_history (version, description)
values ('0005', 'stage 4 monitoring reporting and ai assistant baseline')
on conflict (version) do nothing;
