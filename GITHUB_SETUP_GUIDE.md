# GitHub Actions 在线打包 APK 指南

本指南将帮助你使用 GitHub Actions 自动构建 Android APK，无需在本地安装复杂的开发环境。

## 📋 准备工作

### 1. 确保你有以下内容：
- ✅ GitHub 账户（已有）
- ✅ 本项目代码（已在你的电脑上）
- ✅ 稳定的网络连接

### 2. 检查项目文件：
确保你的项目包含以下关键文件：
- `buildozer.spec` - Android 构建配置
- `main.py` - 应用主程序
- `requirements.txt` - Python 依赖
- `.gitignore` - Git 忽略规则（已配置忽略 `.buildozer/` 和 `bin/`）

## 🚀 第一步：创建 GitHub 仓库

### 方法A：网页创建（推荐）
1. 访问 https://github.com 并登录
2. 点击右上角 "+" 图标 → "New repository"
3. 填写仓库信息：
   - **Repository name**: `LotteryMobileApp`（或其他名称）
   - **Description**: 可选，如 "彩票记录与分析工具"
   - **Public** 或 **Private**（建议 Public）
4. **重要**：不要勾选以下选项：
   - [ ] Add a README file
   - [ ] Add .gitignore
   - [ ] Choose a license
   （因为项目已有这些文件）
5. 点击 "Create repository"

### 方法B：使用 GitHub CLI（高级）
```bash
gh repo create LotteryMobileApp --public --push --source=. --remote=origin
```

## 📤 第二步：上传项目到 GitHub

### A. 打开命令行
1. 按 `Win + R` 键
2. 输入 `cmd` 按回车
3. 进入项目目录：
   ```cmd
   cd C:\Users\86152\LotteryMobileApp
   ```

### B. 初始化 Git 仓库
```bash
git init
```

### C. 添加所有文件
```bash
git add .
```
*注意：这会添加除 `.gitignore` 中指定的文件外的所有文件*

### D. 创建第一次提交
```bash
git commit -m "Initial commit: Lottery tracking mobile app"
```

### E. 连接到 GitHub 仓库
将 `YOUR_USERNAME` 替换为你的 GitHub 用户名：
```bash
git remote add origin https://github.com/YOUR_USERNAME/LotteryMobileApp.git
```

### F. 推送代码到 GitHub
```bash
git branch -M main
git push -u origin main
```

### G. 输入 GitHub 凭证
第一次推送时会要求输入用户名和密码：
- **用户名**：你的 GitHub 用户名
- **密码**：使用 **Personal Access Token**（不是 GitHub 密码）
  1. 访问：https://github.com/settings/tokens
  2. 点击 "Generate new token"
  3. 选择 "repo" 权限
  4. 生成并复制 token
  5. 粘贴 token 作为密码

## ⚙️ 第三步：GitHub Actions 工作流

### 已自动配置
项目已包含 GitHub Actions 工作流文件：
- `.github/workflows/build-android.yml`

这个工作流会自动：
1. 在代码推送时触发构建
2. 使用 Ubuntu Linux 环境
3. 自动下载 Android SDK/NDK
4. 使用清华镜像加速下载（中国用户）
5. 构建 Android APK 调试版
6. 上传 APK 作为可下载文件

### 如果需要手动触发：
1. 进入 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 选择 "Build Android APK" 工作流
4. 点击 "Run workflow"

## 🏗️ 第四步：监控构建过程

### 查看构建进度：
1. 进入仓库 → "Actions" 标签
2. 点击正在运行的工作流
3. 查看实时日志

### 第一次构建时间：
- **预计时间**：30-60 分钟
- **原因**：需要下载 Android SDK/NDK（约 2-5GB）
- **后续构建**：5-15 分钟（使用了缓存）

### 常见状态：
- ⏳ **Queued**：排队中
- 🏗️ **In Progress**：构建中
- ✅ **Completed**：完成
- ❌ **Failed**：失败

## 📱 第五步：下载 APK 文件

### 构建成功后：
1. 进入工作流运行页面
2. 滚动到 "Artifacts" 部分
3. 点击 `lottery-app-apk` 下载
4. 解压 zip 文件获取 APK

### APK 文件信息：
- **文件名**：`lottery.tool-1.0.0-debug.apk`
- **位置**：`bin/` 文件夹内
- **大小**：约 20-50 MB

### 安装到手机：
1. 将 APK 文件复制到手机
2. 在文件管理器中找到 APK
3. 点击安装（需允许"未知来源应用"）
4. 打开应用测试功能

## 🔧 故障排除

### 问题1：构建失败（Android SDK 下载超时）
**解决方案**：
- 工作流已配置清华镜像源
- 等待一段时间后重试
- 检查 GitHub Actions 运行日志

### 问题2：Git 推送失败
**解决方案**：
```bash
# 检查远程仓库配置
git remote -v

# 如果配置错误，重新设置
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/LotteryMobileApp.git

# 强制推送（谨慎使用）
git push -f origin main
```

### 问题3：APK 无法安装
**解决方案**：
1. 确保 Android 版本 5.0+（API 21+）
2. 开启"未知来源应用"权限
3. 尝试其他 Android 设备

### 问题4：工作流未触发
**解决方案**：
1. 确保代码已推送到 `main` 或 `master` 分支
2. 检查 `.github/workflows/build-android.yml` 文件是否存在
3. 手动触发工作流：
   - Actions → Build Android APK → Run workflow

## 📝 工作流配置说明

### 关键配置：
- **运行环境**：Ubuntu 22.04
- **Python 版本**：3.9（兼容 Kivy 2.3.0）
- **Android SDK**：API 31（目标），API 21（最低）
- **缓存**：Android SDK/NDK 缓存加速构建
- **镜像源**：清华镜像（中国用户）

### 构建步骤：
1. 安装系统依赖（Java、Python、编译工具）
2. 安装 Buildozer
3. 下载/缓存 Android SDK
4. 构建 APK
5. 上传 APK 文件

## 🔄 后续开发流程

### 日常开发：
1. 修改代码
2. 提交更改：
   ```bash
   git add .
   git commit -m "描述修改内容"
   git push origin main
   ```
3. GitHub Actions 自动构建新 APK
4. 下载新版本测试

### 版本更新：
修改 `buildozer.spec` 中的版本号：
```ini
version = 1.0.1
```

## 📞 技术支持

### 查看详细日志：
```bash
# 在工作流运行页面查看完整日志
```

### 常见错误：
- **Network timeout**：网络超时，等待后重试
- **Disk space**：GitHub Actions 磁盘空间不足
- **License acceptance**：Android SDK 许可证问题（已自动处理）

### 获取帮助：
1. 查看工作流运行日志
2. 检查本指南的故障排除部分
3. 提供错误截图寻求帮助

## 🎉 完成！

成功设置后，你将拥有：
- ✅ 自动化的 APK 构建管道
- ✅ 无需本地复杂环境
- ✅ 云端的 Android SDK 管理
- ✅ 可下载的 APK 文件
- ✅ 每次代码推送自动构建

**现在开始你的云端构建之旅吧！**