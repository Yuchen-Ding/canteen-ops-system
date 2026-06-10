import {
  BadgeDollarSign,
  CalendarDays,
  CalendarRange,
  Bot,
  Building2,
  ClipboardList,
  CreditCard,
  Gauge,
  Monitor,
  Package,
  Receipt,
  RefreshCcw,
  Settings,
  ShieldCheck,
  Store,
  TabletSmartphone,
  UserRound,
  UsersRound,
  Utensils,
} from 'lucide-react';

export const navigationItems = [
  { key: 'dashboard', label: '运营看板', icon: Gauge },
  { key: 'canteens', label: '餐厅管理', icon: Building2 },
  { key: 'stalls', label: '档口管理', icon: Store },
  { key: 'dishes', label: '菜品管理', icon: Utensils },
  { key: 'mealPackages', label: '套餐管理', icon: Package },
  { key: 'employees', label: '员工管理', icon: UsersRound },
  { key: 'visitors', label: '访客管理', icon: UserRound },
  { key: 'devices', label: 'POS 设备', icon: TabletSmartphone },
  { key: 'employeeCardPayment', label: '员工刷卡消费', icon: CreditCard },
  { key: 'visitorQrPayment', label: '访客扫码消费', icon: Receipt },
  { key: 'orders', label: '订单管理', icon: ClipboardList },
  { key: 'payments', label: '支付流水', icon: BadgeDollarSign },
  { key: 'refunds', label: '退款管理', icon: RefreshCcw },
  { key: 'subsidyRules', label: '补贴规则', icon: ShieldCheck, disabled: true },
  { key: 'dailyReport', label: '运营日报', icon: CalendarDays },
  { key: 'monthlyReport', label: '运营月报', icon: CalendarRange },
  { key: 'deviceMonitoring', label: '设备监控', icon: Monitor, disabled: true },
  { key: 'aiSummary', label: 'AI 运营总结', icon: Bot, disabled: true },
  { key: 'settings', label: '系统设置', icon: Settings, disabled: true },
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
      <nav className="nav-list" aria-label="主导航">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              className={`nav-item ${activePage === item.key ? 'active' : ''}`}
              disabled={item.disabled}
              key={item.key}
              title={item.disabled ? '后续阶段实现' : item.label}
              type="button"
              onClick={() => onNavigate(item.key)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
