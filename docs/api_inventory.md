# API 清单

阶段 0 仅提供系统级接口，业务 API 从阶段 1 开始增加。

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/health` | 返回服务状态、版本、环境和时间戳 |
| GET | `/health/db` | 检查 PostgreSQL 连接状态 |
| GET | `/metrics` | 返回基础 mock metrics |
| GET | `/api/v1/system/info` | 返回系统名称、版本、环境和 AI provider |

## 命名约束

- API 路径统一使用英文。
- 枚举值统一使用英文。
- 数据库字段统一使用英文。
- 前端展示文本使用中文。
