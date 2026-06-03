# 部署策略

## 开发与部署模式

本项目采用“本地 Codex 开发 + GitHub 版本管理 + 云服务器 QA 部署”的模式。

- Mac 本地：用于开发、代码检查、Git 提交和最小 smoke test。
- GitHub：用于版本管理和基础 CI。
- QA 云服务器：作为主要运行环境，使用 Docker Compose 部署。
- PRD：阶段 0 仅保留结构占位，不建议直接对公网暴露服务。

## Compose 文件

- `docker-compose.local.yml`：本地最小验证。
- `docker-compose.qa.yml`：云服务器 QA 部署。
- `docker-compose.prd.yml`：生产结构占位。

## 端口策略

项目避免使用常见冲突端口：`80`、`443`、`3000`、`5001`、`5432`、`6379`。

阶段 0 使用：

- Frontend: `3100`
- Backend: `8100`
- Local PostgreSQL: `55432`

QA 和 PRD 不暴露 PostgreSQL 到公网。

## 安全约束

- 不提交真实密钥。
- 不在脚本中执行 `docker system prune`、`docker volume prune` 或删除所有容器、所有 volume 的命令。
- QA 数据库只允许 Docker network 内部访问。
