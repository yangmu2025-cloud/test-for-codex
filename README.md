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
