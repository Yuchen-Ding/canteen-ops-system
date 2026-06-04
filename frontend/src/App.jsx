import { useMemo, useState } from 'react';
import { LayoutDashboard } from 'lucide-react';

import { navigationItems, Sidebar } from './components/Sidebar.jsx';
import { Dashboard } from './pages/Dashboard.jsx';
import { MasterDataPage } from './pages/MasterDataPage.jsx';
import { masterDataPages } from './pages/masterDataConfig.js';

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
