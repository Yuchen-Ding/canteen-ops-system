import { Activity, Database, GitBranch, ServerCog } from 'lucide-react';

const statusCards = [
  {
    title: '工程骨架',
    value: '已建立',
    description: 'FastAPI、React、PostgreSQL、Docker Compose 基线已规划。',
    icon: GitBranch,
  },
  {
    title: '健康检查',
    value: '/health',
    description: '后端提供服务、数据库和系统信息检查接口。',
    icon: Activity,
  },
  {
    title: '数据库',
    value: 'PostgreSQL',
    description: '阶段 0 仅创建系统版本表，不创建完整业务数据。',
    icon: Database,
  },
  {
    title: '部署目标',
    value: 'QA 云服务器',
    description: '适配 Ubuntu 22.04 / 24.04 与 Docker Compose。',
    icon: ServerCog,
  },
];

const roadmapItems = [
  '阶段 1：餐厅、档口、菜品、员工、访客、POS 设备主数据',
  '阶段 2：员工刷卡、访客扫码、订单与支付状态闭环',
  '阶段 3：退款、补贴计算、日报与月度结算',
  '阶段 4：设备监控、异常交易检测与监控指标',
  '阶段 5：AI 日报和月报总结，默认 mock provider',
];

export function Dashboard() {
  return (
    <section className="dashboard">
      <div className="section-heading">
        <h2>运营看板</h2>
        <p>当前版本用于验证工程结构、部署基线、健康检查和后续业务扩展位置。</p>
      </div>

      <div className="status-grid">
        {statusCards.map((card) => {
          const Icon = card.icon;
          return (
            <article className="status-card" key={card.title}>
              <div className="card-icon">
                <Icon size={22} />
              </div>
              <div>
                <h3>{card.title}</h3>
                <strong>{card.value}</strong>
                <p>{card.description}</p>
              </div>
            </article>
          );
        })}
      </div>

      <div className="content-band">
        <div>
          <h3>阶段 0 范围</h3>
          <p>
            本阶段只交付可上传 GitHub、可在云服务器 QA 环境部署的基础工程，不接入真实支付、刷卡硬件、HR、门禁或财务系统。
          </p>
        </div>
        <ul>
          {roadmapItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
