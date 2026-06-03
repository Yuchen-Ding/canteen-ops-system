import { LayoutDashboard } from 'lucide-react';

import { Sidebar } from './components/Sidebar.jsx';
import { Dashboard } from './pages/Dashboard.jsx';

export function App() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">QA 部署基线</p>
            <h1>企业餐厅运营管理系统</h1>
          </div>
          <div className="environment-pill">
            <LayoutDashboard size={18} />
            <span>阶段 0</span>
          </div>
        </header>
        <Dashboard />
      </main>
    </div>
  );
}
