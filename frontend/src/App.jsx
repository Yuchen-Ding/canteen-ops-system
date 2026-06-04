import { useMemo, useState } from 'react';
import { LayoutDashboard } from 'lucide-react';

import { navigationItems, Sidebar } from './components/Sidebar.jsx';
import { Dashboard } from './pages/Dashboard.jsx';
import { MasterDataPage } from './pages/MasterDataPage.jsx';
import { masterDataPages } from './pages/masterDataConfig.js';
import { OrdersPage } from './pages/OrdersPage.jsx';
import { PaymentsPage } from './pages/PaymentsPage.jsx';
import { PosPaymentPage } from './pages/PosPaymentPage.jsx';

export function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const activeNav = useMemo(
    () => navigationItems.find((item) => item.key === activePage) || navigationItems[0],
    [activePage],
  );

  const renderPage = () => {
    if (activePage === 'dashboard') {
      return <Dashboard />;
    }
    if (masterDataPages[activePage]) {
      return <MasterDataPage config={masterDataPages[activePage]} />;
    }
    if (activePage === 'employeeCardPayment') {
      return <PosPaymentPage mode="employee" />;
    }
    if (activePage === 'visitorQrPayment') {
      return <PosPaymentPage mode="visitor" />;
    }
    if (activePage === 'orders') {
      return <OrdersPage />;
    }
    if (activePage === 'payments') {
      return <PaymentsPage />;
    }
    return <Dashboard />;
  };

  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">阶段 1 主数据管理</p>
            <h1>{activePage === 'dashboard' ? '企业餐厅运营管理系统' : activeNav.label}</h1>
          </div>
          <div className="environment-pill">
            <LayoutDashboard size={18} />
            <span>阶段 1</span>
          </div>
        </header>
        {renderPage()}
      </main>
    </div>
  );
}
