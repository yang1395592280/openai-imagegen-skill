# OpenAI ImageGen Skill 客户安装使用指南

本文档面向需要在 Codex 中使用自有 OpenAI-compatible 生图接口的客户。安装完成后，客户可以在 Codex 里调用 `openai-imagegen` 生成图片或编辑图片。

## 一、准备信息

请先准备好三项信息：

```text
IMAGEGEN_API_KEY   生图分组的 API Key
IMAGEGEN_BASE_URL  生图接口地址，必须是 /v1 结尾
IMAGEGEN_MODEL     生图模型名或网关模型别名
```

示例：

```text
IMAGEGEN_API_KEY   <your-image-api-key>
IMAGEGEN_BASE_URL  https://api.example.com/v1
IMAGEGEN_MODEL     gpt-image-2
```

注意：

- 不要把真实 API Key 发到群聊、截图、工单或 GitHub 仓库里。
- `IMAGEGEN_BASE_URL` 应该填到 `/v1`，不要填到 `/images/generations`。
- 如果服务端使用模型映射，请确保 `IMAGEGEN_MODEL` 能被生图分组识别。

## 二、macOS 安装步骤

### 1. 安装基础工具

打开「终端」执行：

```bash
git --version
python3 --version
node --version
```

如果 `git` 不存在，macOS 通常会提示安装 Command Line Tools，按提示安装即可。

如果 `node` 不存在，请安装 Node.js：

```bash
brew install node
```

如果没有 Homebrew，可以从 Node.js 官网下载安装包：

```text
https://nodejs.org/
```

### 2. 下载 skill 仓库

```bash
cd ~
git clone https://github.com/yang1395592280/openai-imagegen-skill.git
cd openai-imagegen-skill
```

### 3. 安装到 Codex

```bash
./install.sh
```

安装成功后会输出类似路径：

```text
/Users/yourname/.codex/skills/openai-imagegen
```

如果之前安装过，需要覆盖：

```bash
./install.sh --force
```

### 4. 配置环境变量

推荐写入 `~/.zshrc`，这样以后打开终端都会自动生效：

```bash
cat >> ~/.zshrc <<'EOF'

# OpenAI ImageGen Skill
export IMAGEGEN_API_KEY="<你的生图分组Key>"
export IMAGEGEN_BASE_URL="https://你的生图接口域名/v1"
export IMAGEGEN_MODEL="gpt-image-2"
export IMAGEGEN_OUTPUT_DIR="$HOME/Pictures/codex-images"
EOF
```

让配置立即生效：

```bash
source ~/.zshrc
```

检查变量是否存在，不要打印完整 Key：

```bash
test -n "$IMAGEGEN_API_KEY" && echo "IMAGEGEN_API_KEY is set"
echo "$IMAGEGEN_BASE_URL"
echo "$IMAGEGEN_MODEL"
```

### 5. 重启 Codex

关闭并重新打开 Codex。重新打开后，Codex 才能读取新安装的 skill 和新的环境变量。

### 6. 在 Codex 中测试

在 Codex 中输入：

```text
使用 openai-imagegen 生成一张 1024x1024 的图片：一只白色陶瓷咖啡杯放在木质桌面上，产品摄影风格
```

如果成功，Codex 会返回本地图片路径。

## 三、Windows 安装步骤

### 1. 安装基础工具

请先安装：

- Git for Windows: `https://git-scm.com/download/win`
- Node.js: `https://nodejs.org/`
- Python 3: `https://www.python.org/downloads/windows/`

安装 Python 时请勾选：

```text
Add python.exe to PATH
```

安装完成后，打开 PowerShell，执行：

```powershell
git --version
node --version
python --version
```

如果 `python --version` 不可用，尝试：

```powershell
py --version
```

### 2. 下载 skill 仓库

打开 PowerShell：

```powershell
cd $HOME
git clone https://github.com/yang1395592280/openai-imagegen-skill.git
cd openai-imagegen-skill
```

### 3. 安装到 Codex

Windows 上推荐直接运行 Node 安装器：

```powershell
node .\bin\install.js
```

安装成功后会输出类似路径：

```text
C:\Users\yourname\.codex\skills\openai-imagegen
```

如果之前安装过，需要覆盖：

```powershell
node .\bin\install.js --force
```

### 4. 配置环境变量

#### 方式 A：仅当前 PowerShell 窗口生效

适合临时测试：

```powershell
$env:IMAGEGEN_API_KEY = "<你的生图分组Key>"
$env:IMAGEGEN_BASE_URL = "https://你的生图接口域名/v1"
$env:IMAGEGEN_MODEL = "gpt-image-2"
$env:IMAGEGEN_OUTPUT_DIR = "$HOME\Pictures\codex-images"
```

#### 方式 B：永久保存到当前用户环境变量

推荐正式使用：

```powershell
[Environment]::SetEnvironmentVariable("IMAGEGEN_API_KEY", "<你的生图分组Key>", "User")
[Environment]::SetEnvironmentVariable("IMAGEGEN_BASE_URL", "https://你的生图接口域名/v1", "User")
[Environment]::SetEnvironmentVariable("IMAGEGEN_MODEL", "gpt-image-2", "User")
[Environment]::SetEnvironmentVariable("IMAGEGEN_OUTPUT_DIR", "$HOME\Pictures\codex-images", "User")
```

永久环境变量需要重新打开 PowerShell 和 Codex 才会生效。

检查变量是否存在，不要打印完整 Key：

```powershell
if ($env:IMAGEGEN_API_KEY) { "IMAGEGEN_API_KEY is set" }
$env:IMAGEGEN_BASE_URL
$env:IMAGEGEN_MODEL
```

### 5. 重启 Codex

关闭并重新打开 Codex。重新打开后，Codex 才能读取新安装的 skill 和新的环境变量。

### 6. 在 Codex 中测试

在 Codex 中输入：

```text
使用 openai-imagegen 生成一张 1024x1024 的图片：一只白色陶瓷咖啡杯放在木质桌面上，产品摄影风格
```

如果成功，Codex 会返回本地图片路径。

## 四、直接测试脚本

如果 Codex 中调用失败，可以先在终端直接测试脚本。

### macOS

```bash
python3 ~/.codex/skills/openai-imagegen/scripts/generate_image.py \
  --prompt "A simple red apple on a white table" \
  --output /tmp/openai-imagegen-test.png
```

### Windows PowerShell

```powershell
python "$HOME\.codex\skills\openai-imagegen\scripts\generate_image.py" `
  --prompt "A simple red apple on a white table" `
  --output "$HOME\Pictures\openai-imagegen-test.png"
```

成功时会输出类似：

```json
{
  "mode": "generation",
  "model": "gpt-image-2",
  "output": "/path/to/openai-imagegen-test.png",
  "url": null,
  "has_b64_json": true,
  "revised_prompt": null
}
```

## 五、图片编辑用法

### macOS 示例

```bash
python3 ~/.codex/skills/openai-imagegen/scripts/generate_image.py \
  --input-image /absolute/path/input.png \
  --prompt "保留主体，把背景换成明亮的摄影棚" \
  --output /tmp/openai-imagegen-edit.png
```

### Windows PowerShell 示例

```powershell
python "$HOME\.codex\skills\openai-imagegen\scripts\generate_image.py" `
  --input-image "C:\Users\yourname\Pictures\input.png" `
  --prompt "保留主体，把背景换成明亮的摄影棚" `
  --output "$HOME\Pictures\openai-imagegen-edit.png"
```

## 六、更新 skill

### macOS

```bash
cd ~/openai-imagegen-skill
git pull
./install.sh --force
```

### Windows PowerShell

```powershell
cd $HOME\openai-imagegen-skill
git pull
node .\bin\install.js --force
```

更新后请重启 Codex。

## 七、卸载 skill

### macOS

```bash
rm -rf ~/.codex/skills/openai-imagegen
```

### Windows PowerShell

```powershell
Remove-Item -Recurse -Force "$HOME\.codex\skills\openai-imagegen"
```

卸载后请重启 Codex。

## 八、常见问题

### 1. Codex 里没有触发 openai-imagegen

处理方式：

1. 确认已经安装到 `~/.codex/skills/openai-imagegen`。
2. 确认安装后已经重启 Codex。
3. 在提示词中明确写：`使用 openai-imagegen ...`。

### 2. 提示 IMAGEGEN_API_KEY is required

说明 Codex 启动时没有读到环境变量。

处理方式：

- macOS：确认变量写入 `~/.zshrc` 后重新打开 Codex。
- Windows：确认使用 `SetEnvironmentVariable` 后重新打开 Codex。

### 3. 提示 IMAGEGEN_BASE_URL is required

说明没有配置接口地址。

正确格式：

```text
https://你的生图接口域名/v1
```

不要写成：

```text
https://你的生图接口域名/v1/images/generations
```

### 4. 提示 model not found 或模型不可用

说明 `IMAGEGEN_MODEL` 没有被你的生图接口识别。

处理方式：

- 把 `IMAGEGEN_MODEL` 改成服务端支持的模型名。
- 或者在网关后台把 `gpt-image-2` 映射到真实可用的生图模型。

### 5. 返回 HTTP 401

通常是 Key 错误、Key 过期、Key 没有生图分组权限。

处理方式：

1. 重新生成生图分组 Key。
2. 确认 Key 没有多余空格。
3. 确认该 Key 可以访问图片接口。

### 6. 返回 HTTP 404

通常是 `IMAGEGEN_BASE_URL` 错误。

处理方式：

1. 确认地址以 `/v1` 结尾。
2. 确认服务端支持 `/v1/images/generations`。
3. 确认域名可以从本机访问。

### 7. 返回 HTTP 429

说明触发限流或额度不足。

处理方式：

- 稍后重试。
- 降低并发或 `n` 数量。
- 检查服务端额度。

### 8. 图片编辑没有按原图修改

接口返回成功不代表图生图效果一定符合预期。请检查输出图片是否保留了原图主体。

处理方式：

- 换更明确的提示词。
- 使用更清晰的输入图片。
- 确认服务端的 `/images/edits` 真实支持图生图。

## 九、给客户的最短使用说明

安装：

```bash
git clone https://github.com/yang1395592280/openai-imagegen-skill.git
cd openai-imagegen-skill
./install.sh
```

配置：

```bash
export IMAGEGEN_API_KEY="<你的生图分组Key>"
export IMAGEGEN_BASE_URL="https://你的生图接口域名/v1"
export IMAGEGEN_MODEL="gpt-image-2"
```

在 Codex 里说：

```text
使用 openai-imagegen 生成一张产品海报图：一杯冰美式咖啡，干净白色背景，商业摄影风格
```
