insert into canteen_ops.canteens (canteen_code, name, city, location, status, remark)
values
    ('CT-HF-001', '合肥餐厅', '合肥', '合肥研发中心 A 座 1 层', 'ACTIVE', '服务合肥园区员工和访客'),
    ('CT-BJ-001', '北京餐厅', '北京', '北京总部 B 座 B1 层', 'ACTIVE', '总部综合餐厅'),
    ('CT-TJ-001', '天津餐厅', '天津', '天津制造基地生活区 1 层', 'ACTIVE', '制造基地员工餐厅')
on conflict (canteen_code) do nothing;

insert into canteen_ops.stalls (stall_code, canteen_id, name, category, floor, status, remark)
values
    ('ST-HF-NOODLE', (select id from canteen_ops.canteens where canteen_code = 'CT-HF-001'), '面食档口', 'NOODLE', '1F', 'ACTIVE', '早餐和午餐面食供应'),
    ('ST-HF-FAST', (select id from canteen_ops.canteens where canteen_code = 'CT-HF-001'), '快餐档口', 'FAST_FOOD', '1F', 'ACTIVE', '工作日午餐快餐供应'),
    ('ST-BJ-COFFEE', (select id from canteen_ops.canteens where canteen_code = 'CT-BJ-001'), '咖啡档口', 'COFFEE', 'B1', 'ACTIVE', '咖啡和轻食供应'),
    ('ST-BJ-FAST', (select id from canteen_ops.canteens where canteen_code = 'CT-BJ-001'), '快餐档口', 'FAST_FOOD', 'B1', 'ACTIVE', '总部午餐档口'),
    ('ST-TJ-NOODLE', (select id from canteen_ops.canteens where canteen_code = 'CT-TJ-001'), '面食档口', 'NOODLE', '1F', 'ACTIVE', '制造基地面食档口'),
    ('ST-TJ-STORE', (select id from canteen_ops.canteens where canteen_code = 'CT-TJ-001'), '便利店档口', 'CONVENIENCE', '1F', 'ACTIVE', '包装食品和饮品供应')
on conflict (stall_code) do nothing;

insert into canteen_ops.dishes (dish_code, stall_id, name, category, unit_price, is_available, status, remark)
values
    ('DS-HF-NOODLE-001', (select id from canteen_ops.stalls where stall_code = 'ST-HF-NOODLE'), '牛肉面', 'NOODLE', 18.00, true, 'ACTIVE', '午餐高频菜品'),
    ('DS-HF-NOODLE-002', (select id from canteen_ops.stalls where stall_code = 'ST-HF-NOODLE'), '番茄鸡蛋面', 'NOODLE', 14.00, true, 'ACTIVE', '清淡面食'),
    ('DS-HF-NOODLE-003', (select id from canteen_ops.stalls where stall_code = 'ST-HF-NOODLE'), '葱油拌面', 'NOODLE', 12.00, true, 'ACTIVE', '快速出餐'),
    ('DS-HF-FAST-001', (select id from canteen_ops.stalls where stall_code = 'ST-HF-FAST'), '红烧鸡腿饭', 'RICE', 20.00, true, 'ACTIVE', '标准员工套餐'),
    ('DS-HF-FAST-002', (select id from canteen_ops.stalls where stall_code = 'ST-HF-FAST'), '鱼香肉丝饭', 'RICE', 18.00, true, 'ACTIVE', '川味快餐'),
    ('DS-HF-FAST-003', (select id from canteen_ops.stalls where stall_code = 'ST-HF-FAST'), '时蔬豆腐饭', 'RICE', 15.00, true, 'ACTIVE', '素食选项'),
    ('DS-BJ-COFFEE-001', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-COFFEE'), '美式咖啡', 'DRINK', 12.00, true, 'ACTIVE', '办公区常规饮品'),
    ('DS-BJ-COFFEE-002', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-COFFEE'), '拿铁咖啡', 'DRINK', 18.00, true, 'ACTIVE', '咖啡档口热销'),
    ('DS-BJ-COFFEE-003', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-COFFEE'), '火腿三明治', 'LIGHT_MEAL', 16.00, true, 'ACTIVE', '早餐轻食'),
    ('DS-BJ-FAST-001', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-FAST'), '黑椒牛柳饭', 'RICE', 24.00, true, 'ACTIVE', '总部午餐菜品'),
    ('DS-BJ-FAST-002', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-FAST'), '宫保鸡丁饭', 'RICE', 20.00, true, 'ACTIVE', '经典快餐'),
    ('DS-BJ-FAST-003', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-FAST'), '番茄牛腩饭', 'RICE', 23.00, true, 'ACTIVE', '热菜盖饭'),
    ('DS-TJ-NOODLE-001', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-NOODLE'), '炸酱面', 'NOODLE', 13.00, true, 'ACTIVE', '北方风味'),
    ('DS-TJ-NOODLE-002', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-NOODLE'), '羊肉烩面', 'NOODLE', 22.00, true, 'ACTIVE', '高蛋白午餐'),
    ('DS-TJ-NOODLE-003', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-NOODLE'), '鸡汤馄饨', 'NOODLE', 12.00, true, 'ACTIVE', '早餐和夜班供应'),
    ('DS-TJ-STORE-001', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-STORE'), '矿泉水', 'DRINK', 3.00, true, 'ACTIVE', '常温饮品'),
    ('DS-TJ-STORE-002', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-STORE'), '酸奶', 'DRINK', 6.00, true, 'ACTIVE', '冷藏饮品'),
    ('DS-TJ-STORE-003', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-STORE'), '全麦面包', 'PACKAGED_FOOD', 8.00, true, 'ACTIVE', '包装食品')
on conflict (dish_code) do nothing;

insert into canteen_ops.meal_packages (package_code, stall_id, name, package_price, status, remark)
values
    ('PK-HF-FAST-001', (select id from canteen_ops.stalls where stall_code = 'ST-HF-FAST'), '合肥工作午餐套餐', 26.00, 'ACTIVE', '主食搭配饮品的员工午餐套餐'),
    ('PK-BJ-COFFEE-001', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-COFFEE'), '北京早餐咖啡套餐', 26.00, 'ACTIVE', '咖啡搭配轻食'),
    ('PK-BJ-FAST-001', (select id from canteen_ops.stalls where stall_code = 'ST-BJ-FAST'), '总部商务午餐套餐', 32.00, 'ACTIVE', '适合访客接待的午餐套餐'),
    ('PK-TJ-STORE-001', (select id from canteen_ops.stalls where stall_code = 'ST-TJ-STORE'), '夜班补给套餐', 12.00, 'ACTIVE', '制造基地夜班包装食品组合')
on conflict (package_code) do nothing;

insert into canteen_ops.meal_package_items (package_id, dish_id, quantity)
values
    ((select id from canteen_ops.meal_packages where package_code = 'PK-HF-FAST-001'), (select id from canteen_ops.dishes where dish_code = 'DS-HF-FAST-001'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-HF-FAST-001'), (select id from canteen_ops.dishes where dish_code = 'DS-HF-FAST-003'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-BJ-COFFEE-001'), (select id from canteen_ops.dishes where dish_code = 'DS-BJ-COFFEE-002'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-BJ-COFFEE-001'), (select id from canteen_ops.dishes where dish_code = 'DS-BJ-COFFEE-003'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-BJ-FAST-001'), (select id from canteen_ops.dishes where dish_code = 'DS-BJ-FAST-001'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-BJ-FAST-001'), (select id from canteen_ops.dishes where dish_code = 'DS-BJ-FAST-003'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-TJ-STORE-001'), (select id from canteen_ops.dishes where dish_code = 'DS-TJ-STORE-002'), 1),
    ((select id from canteen_ops.meal_packages where package_code = 'PK-TJ-STORE-001'), (select id from canteen_ops.dishes where dish_code = 'DS-TJ-STORE-003'), 1)
on conflict (package_id, dish_id) do nothing;

insert into canteen_ops.employees (employee_no, name, department, employee_type, card_no, phone, status, remark)
values
    ('EMP-0001', '张伟', '研发中心', 'FULL_TIME', 'CARD-100001', '13800001001', 'ACTIVE', '合肥研发员工'),
    ('EMP-0002', '李娜', '产品部', 'FULL_TIME', 'CARD-100002', '13800001002', 'ACTIVE', '总部产品经理'),
    ('EMP-0003', '王磊', '制造部', 'OUTSOURCED', 'CARD-100003', '13800001003', 'ACTIVE', '天津制造基地外包员工'),
    ('EMP-0004', '赵敏', '行政部', 'MANAGEMENT', 'CARD-100004', '13800001004', 'ACTIVE', '行政管理人员'),
    ('EMP-0005', '陈晨', '财务部', 'FULL_TIME', 'CARD-100005', '13800001005', 'ACTIVE', '财务结算对接人'),
    ('EMP-0006', '刘洋', 'IT 运维部', 'CONTRACTOR', 'CARD-100006', '13800001006', 'ACTIVE', '运维合同员工'),
    ('EMP-0007', '孙悦', '人力资源部', 'FULL_TIME', 'CARD-100007', '13800001007', 'ACTIVE', '员工信息维护'),
    ('EMP-0008', '周强', '安全部', 'OUTSOURCED', 'CARD-100008', '13800001008', 'ACTIVE', '园区安保人员'),
    ('EMP-0009', '吴迪', '供应链部', 'CONTRACTOR', 'CARD-100009', '13800001009', 'ACTIVE', '供应链合同员工'),
    ('EMP-0010', '郑可', '研发中心', 'INTERN', 'CARD-100010', '13800001010', 'ACTIVE', '实习生')
on conflict (employee_no) do nothing;

insert into canteen_ops.visitors (visitor_no, name, phone, company, status, remark)
values
    ('VIS-0001', '高明', '13900002001', '华东供应商有限公司', 'ACTIVE', '合肥供应商访客'),
    ('VIS-0002', '林雪', '13900002002', '北京咨询服务有限公司', 'ACTIVE', '总部项目访客'),
    ('VIS-0003', '何峰', '13900002003', '天津设备维保有限公司', 'ACTIVE', '天津基地维保访客')
on conflict (visitor_no) do nothing;

insert into canteen_ops.devices (device_code, device_name, canteen_id, stall_id, device_type, ip_address, location, status, last_heartbeat_time, remark)
values
    ('DEV-HF-001', '合肥面食 POS 01', (select id from canteen_ops.canteens where canteen_code = 'CT-HF-001'), (select id from canteen_ops.stalls where stall_code = 'ST-HF-NOODLE'), 'POS', '10.10.1.21', '合肥餐厅 1F 面食档口', 'ONLINE', now(), '主收银设备'),
    ('DEV-HF-002', '合肥快餐自助机 01', (select id from canteen_ops.canteens where canteen_code = 'CT-HF-001'), (select id from canteen_ops.stalls where stall_code = 'ST-HF-FAST'), 'SELF_SERVICE', '10.10.1.31', '合肥餐厅 1F 快餐档口', 'ONLINE', now(), '自助结算设备'),
    ('DEV-BJ-001', '北京咖啡移动终端 01', (select id from canteen_ops.canteens where canteen_code = 'CT-BJ-001'), (select id from canteen_ops.stalls where stall_code = 'ST-BJ-COFFEE'), 'MOBILE_TERMINAL', '10.20.1.41', '北京餐厅 B1 咖啡档口', 'OFFLINE', null, '移动点单终端'),
    ('DEV-BJ-002', '北京快餐 POS 01', (select id from canteen_ops.canteens where canteen_code = 'CT-BJ-001'), (select id from canteen_ops.stalls where stall_code = 'ST-BJ-FAST'), 'POS', '10.20.1.51', '北京餐厅 B1 快餐档口', 'MAINTENANCE', null, '维护中'),
    ('DEV-TJ-001', '天津便利店 POS 01', (select id from canteen_ops.canteens where canteen_code = 'CT-TJ-001'), (select id from canteen_ops.stalls where stall_code = 'ST-TJ-STORE'), 'POS', '10.30.1.61', '天津餐厅 1F 便利店档口', 'ONLINE', now(), '便利店收银设备')
on conflict (device_code) do nothing;
