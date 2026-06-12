import { useState } from 'react';

import { AiAssistantWidget } from './components/AiAssistantWidget.jsx';
import { Sidebar } from './components/Sidebar.jsx';
import { CanteenMonitoringPage } from './pages/CanteenMonitoringPage.jsx';
import { Dashboard } from './pages/Dashboard.jsx';
import { MasterDataPage } from './pages/MasterDataPage.jsx';
import { masterDataPages } from './pages/masterDataConfig.js';
import { OrdersPage } from './pages/OrdersPage.jsx';
import { PaymentsPage } from './pages/PaymentsPage.jsx';
import { PosPaymentPage } from './pages/PosPaymentPage.jsx';
import { RefundsPage } from './pages/RefundsPage.jsx';
import { ReportsPage } from './pages/ReportsPage.jsx';

export function App() {
  const [activePage, setActivePage] = useState('dashboard');

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
    if (activePage === 'refunds') {
      return <RefundsPage />;
    }
    if (activePage === 'reports') {
      return <ReportsPage />;
    }
    if (activePage === 'canteenMonitoring') {
      return <CanteenMonitoringPage />;
    }
    return <Dashboard />;
  };

  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <main className="main-content">{renderPage()}</main>
      <AiAssistantWidget />
    </div>
  );
}
