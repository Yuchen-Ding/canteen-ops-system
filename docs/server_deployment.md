# 云服务器 QA 部署文档

## 1. 云服务器建议配置

QA 环境建议配置：

- CPU：2 核或以上
- 内存：4 GB 或以上
- 系统盘：40 GB 或以上
- 操作系统：Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS
- 云厂商：阿里云或华为云均可

## 2. Ubuntu 基础准备

```bash
sudo apt update
sudo apt upgrade -y
```

## 3. 安装 Git

```bash
sudo apt install -y git
git --version
```

## 4. 安装 Docker 和 Docker Compose

```bash
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker compose version
```

如需非 root 用户运行 Docker：

```bash
sudo usermod -aG docker $USER
```

重新登录服务器后生效。

## 5. 从 GitHub clone 项目

```bash
git clone git@github.com:<your-org-or-user>/<your-repo>.git
cd <your-repo>
```

## 6. 配置 env/.env.qa

```bash
cp env/.env.qa.example env/.env.qa
vim env/.env.qa
```

必须修改：

- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `FRONTEND_API_BASE_URL`
- `CORS_ORIGINS_RAW`

示例：

```text
FRONTEND_API_BASE_URL=http://<QA_SERVER_IP>:8100
CORS_ORIGINS_RAW=http://<QA_SERVER_IP>:3100
```

## 7. 启动 QA 环境

```bash
chmod +x scripts/*.sh
scripts/start-qa.sh
```

## 8. 查看容器状态

```bash
docker compose --env-file env/.env.qa -f docker-compose.qa.yml ps
```

## 9. 查看后端日志

```bash
docker logs -f canteen_backend_qa
```

## 10. 执行 smoke test

```bash
BASE_URL=http://<QA_SERVER_IP>:8100 scripts/smoke-test.sh
```

## 11. 停止服务

```bash
docker compose --env-file env/.env.qa -f docker-compose.qa.yml down
```

不要使用会影响服务器其他项目的全局清理命令。

## 12. 数据库备份和恢复

备份 QA 数据库：

```bash
scripts/backup-db.sh qa
```

恢复 QA 数据库：

```bash
scripts/restore-db.sh qa backups/<backup-file>.sql
```

脚本只操作本项目 PostgreSQL 容器 `canteen_postgres_qa`。

## 13. 安全组开放端口建议

QA 阶段建议只开放：

- `22`：SSH，仅允许可信 IP。
- `3100`：前端访问。
- `8100`：后端 API 访问。

## 14. PostgreSQL 安全要求

不要开放 PostgreSQL 到公网。QA Compose 文件没有映射 `5432` 到宿主机，数据库只在 Docker network 内部访问。

## 15. Docker 清理禁令

不要执行以下命令：

```bash
docker system prune
docker volume prune
docker rm -f $(docker ps -aq)
docker volume rm $(docker volume ls -q)
```

这些命令可能影响服务器上其他 Docker 项目。
