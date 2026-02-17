# test-for-codex

一个用于演示「本地仓库一键创建并发布到 GitHub」流程的小型脚本项目。

## 项目目标

本仓库提供一个 Bash 脚本 `create_github_repo.sh`，用于自动完成以下步骤：

1. 调用 GitHub API 创建仓库。
2. 将本地仓库 `origin` 指向新建仓库。
3. 将当前分支推送到远端并设置上游分支。

适用于需要快速初始化远端仓库并发布当前代码的场景。

---

## 目录结构

```text
.
├── create_github_repo.sh   # 核心脚本：创建 GitHub 仓库并推送当前分支
├── README.md               # 项目说明文档（中文）
├── LICENSE
└── paper_crawler.rar       # 示例压缩文件（与脚本逻辑无耦合）
```

---

## 环境要求

运行脚本前，请确认具备以下依赖：

- `bash`（建议 4.x+）
- `git`
- `curl`
- `jq`

可用以下命令检查：

```bash
bash --version
git --version
curl --version
jq --version
```

---

## 快速开始

### 1) 创建 GitHub Token

在 GitHub 中创建 Personal Access Token（classic 或 fine-grained 均可），并确保具备创建仓库与推送代码的权限。

> 最常见做法：classic token 勾选 `repo` 权限。

### 2) 配置环境变量

```bash
export GITHUB_TOKEN='ghp_xxx你的token'
```

可简单验证是否已设置：

```bash
test -n "$GITHUB_TOKEN" && echo "GITHUB_TOKEN 已设置"
```

### 3) 执行脚本

创建公开仓库：

```bash
./create_github_repo.sh 你的新仓库名 public
```

创建私有仓库：

```bash
./create_github_repo.sh 你的新仓库名 private
```

附带描述信息：

```bash
./create_github_repo.sh 你的新仓库名 private "这是一个自动创建的测试仓库"
```

---

## 脚本用法

```bash
./create_github_repo.sh <repo-name> [public|private] [description]
```

- `repo-name`：必填，新仓库名称。
- `public|private`：可选，默认 `public`。
- `description`：可选，仓库描述。

查看帮助：

```bash
./create_github_repo.sh --help
```

---

## 脚本行为说明

脚本执行成功后会：

1. 在你的 GitHub 账号下创建新仓库；
2. 自动创建或更新本地 `origin` 远端地址；
3. 执行 `git push -u origin <当前分支>`；
4. 输出新仓库访问地址和克隆地址。

---

## 常见问题

### 1) 提示 `GITHUB_TOKEN is not set`

请确认你在同一终端会话中执行了：

```bash
export GITHUB_TOKEN='你的token'
```

### 2) 提示仓库创建失败（如名称已存在）

请更换仓库名后重试，或检查 token 权限是否足够。

### 3) 推送失败

可能原因包括：

- 当前目录不是 Git 仓库；
- 当前分支不存在或无法识别；
- 认证权限不足。

可先执行：

```bash
git status
git branch --show-current
```

---

## 安全建议

- 不要将 `GITHUB_TOKEN` 明文写入仓库。
- 不要将 token 提交到 Git 历史。
- 建议使用最小权限原则，定期轮换 token。

---

## 许可证

本项目基于 `LICENSE` 文件中声明的许可证发布。
