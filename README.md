# test-for-codex
Personal test project for codex connect

## 将完成代码发布到新的 GitHub 仓库

我已在仓库根目录新增脚本 `create_github_repo.sh`，用于：

1. 调用 GitHub API 创建新仓库
2. 自动把本地仓库 `origin` 指向新仓库
3. 自动推送当前分支

### 使用步骤

1. 准备 GitHub Personal Access Token（至少包含 `repo` 权限）
2. 导出环境变量：

```bash
export GITHUB_TOKEN=你的token
```

3. 执行脚本（公开仓库）：

```bash
./create_github_repo.sh 你的新仓库名 public
```

4. 或执行脚本（私有仓库）：

```bash
./create_github_repo.sh 你的新仓库名 private
```

脚本执行成功后会输出新仓库地址，并完成当前分支推送。

## 如何添加 GITHUB_TOKEN

### 1) 在 GitHub 创建 Token

1. 登录 GitHub
2. 打开 `Settings` → `Developer settings` → `Personal access tokens` → `Tokens (classic)`
3. 点击 **Generate new token (classic)**
4. 勾选权限：`repo`（创建和推送私有/公开仓库建议使用）
5. 生成后复制 token（只会显示一次）

> 也可以使用 Fine-grained token，但请确保对目标仓库具备可创建/写入权限。

### 2) 临时添加到当前终端会话（推荐先测试）

```bash
export GITHUB_TOKEN='ghp_xxx你的token'
```

验证是否生效：

```bash
echo "$GITHUB_TOKEN" | head -c 10
```

### 3) 永久生效（Linux/macOS）

把下面一行写入 `~/.bashrc` 或 `~/.zshrc`：

```bash
export GITHUB_TOKEN='ghp_xxx你的token'
```

然后执行：

```bash
source ~/.bashrc
# 或 source ~/.zshrc
```

### 4) Windows PowerShell（当前会话）

```powershell
$env:GITHUB_TOKEN="ghp_xxx你的token"
```

### 5) 配置后执行脚本

```bash
./create_github_repo.sh 你的新仓库名 public
```

如果仍提示 `GITHUB_TOKEN is not set`，请确认：

- 你在**同一个终端会话**里执行了 `export`
- 变量名拼写必须是 `GITHUB_TOKEN`
- token 没有多余空格或换行
