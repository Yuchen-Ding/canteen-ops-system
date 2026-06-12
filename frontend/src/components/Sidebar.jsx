import {
  BadgeDollarSign,
  BarChart3,
  Building2,
  ClipboardList,
  CreditCard,
  Gauge,
  Monitor,
  Package,
  Receipt,
  RefreshCcw,
  Store,
  TabletSmartphone,
  UserRound,
  UsersRound,
  Utensils,
} from 'lucide-react';

export const navigationGroups = [
  {
    label: '运营分析',
    items: [
      { key: 'dashboard', label: '运营看板', icon: Gauge },
      { key: 'canteenMonitoring', label: '食堂基础监控', icon: Monitor },
      { key: 'reports', label: '报表中心', icon: BarChart3 },
    ],
  },
  {
    label: '主数据',
    items: [
      { key: 'canteens', label: '餐厅管理', icon: Building2 },
      { key: 'stalls', label: '档口管理', icon: Store },
      { key: 'dishes', label: '菜品管理', icon: Utensils },
      { key: 'mealPackages', label: '套餐管理', icon: Package },
      { key: 'employees', label: '员工管理', icon: UsersRound },
      { key: 'visitors', label: '访客管理', icon: UserRound },
      { key: 'devices', label: 'POS 设备', icon: TabletSmartphone },
    ],
  },
  {
    label: '交易管理',
    items: [
      { key: 'employeeCardPayment', label: '员工刷卡消费', icon: CreditCard },
      { key: 'visitorQrPayment', label: '访客扫码消费', icon: Receipt },
      { key: 'orders', label: '订单管理', icon: ClipboardList },
      { key: 'payments', label: '支付流水', icon: BadgeDollarSign },
      { key: 'refunds', label: '退款管理', icon: RefreshCcw },
    ],
  },
];

export function Sidebar({ activePage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <CreditCard size={24} />
        <div>
          <strong>餐厅运营</strong>
          <span>Canteen Ops</span>
        </div>
      </div>
      <nav className="nav-groups" aria-label="主导航">
        {navigationGroups.map((group) => (
          <section className="nav-group" key={group.label}>
            <p className="nav-group-title">{group.label}</p>
            <div className="nav-list">
              {group.items.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    className={`nav-item ${activePage === item.key ? 'active' : ''}`}
                    key={item.key}
                    title={item.label}
                    type="button"
                    onClick={() => onNavigate(item.key)}
                  >
                    <Icon size={18} />
                    <span>{item.label}</span>
                  </button>
                );
              })}
            </div>
          </section>
        ))}
      </nav>
    </aside>
  );
}
