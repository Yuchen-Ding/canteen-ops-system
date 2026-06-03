import {
  BadgeDollarSign,
  BarChart3,
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

const navigationItems = [
  { label: '运营看板', icon: Gauge, active: true },
  { label: '餐厅管理', icon: Building2 },
  { label: '档口管理', icon: Store },
  { label: '菜品管理', icon: Utensils },
  { label: '套餐管理', icon: Package },
  { label: '员工管理', icon: UsersRound },
  { label: '访客管理', icon: UserRound },
  { label: 'POS 设备', icon: TabletSmartphone },
  { label: '订单管理', icon: ClipboardList },
  { label: '支付流水', icon: BadgeDollarSign },
  { label: '退款管理', icon: RefreshCcw },
  { label: '补贴规则', icon: ShieldCheck },
  { label: '报表中心', icon: BarChart3 },
  { label: '设备监控', icon: Monitor },
  { label: 'AI 运营总结', icon: Bot },
  { label: '系统设置', icon: Settings },
];

export function Sidebar() {
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
            <button className={`nav-item ${item.active ? 'active' : ''}`} key={item.label} type="button">
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
