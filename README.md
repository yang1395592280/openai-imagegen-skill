# OpenAI ImageGen Skill

Codex skill for image generation and image editing through an OpenAI-compatible Images API. It is designed for custom gateways, proxies, and self-managed endpoints.

## Customer Guide

For detailed macOS and Windows setup instructions, see [CUSTOMER_GUIDE.md](CUSTOMER_GUIDE.md).

## Install

### From a cloned repository

```bash
git clone https://github.com/yang1395592280/openai-imagegen-skill.git
cd openai-imagegen-skill
./install.sh
```

Install to a custom Codex skills directory:

```bash
./install.sh --dest "$HOME/.codex/skills/openai-imagegen"
```

Replace an existing installation:

```bash
./install.sh --force
```

### With npm from GitHub

```bash
npm install -g github:yang1395592280/openai-imagegen-skill
openai-imagegen-skill
```

Restart Codex after installing the skill.

## Runtime Configuration

Set these variables in the environment used to run Codex:

```bash
export IMAGEGEN_API_KEY="your-image-api-key"
export IMAGEGEN_BASE_URL="https://your-openai-compatible-host/v1"
export IMAGEGEN_MODEL="gpt-image-2"
```

Optional defaults:

```bash
export IMAGEGEN_SIZE="1024x1024"
export IMAGEGEN_OUTPUT_DIR="$HOME/Pictures/codex-images"
```

Do not commit real API keys or customer endpoints to this repository.

## Usage

In Codex, ask:

```text
Use openai-imagegen to generate a 1024x1024 product poster for a ceramic coffee mug.
```

For image editing, provide an absolute local image path:

```text
Use openai-imagegen to edit /absolute/path/input.png and replace the background with a bright studio scene.
```

The skill saves generated images locally and reports the output path.
