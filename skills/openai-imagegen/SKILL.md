---
name: openai-imagegen
description: Generate and edit images through a user-configured OpenAI-compatible Images API. Use when the task asks Codex to create images, generate pictures, produce visual assets, perform text-to-image, image-to-image, or image edits with a custom base URL, proxy, gateway, or self-managed API key.
---

# OpenAI ImageGen

## Defaults

- Read the API key from `IMAGEGEN_API_KEY`.
- Read the API base URL from `IMAGEGEN_BASE_URL`; it must point to the OpenAI-compatible `/v1` base URL.
- Read the model from `IMAGEGEN_MODEL`; default to `gpt-image-2` only when the variable is unset.
- Never print, echo, commit, or save API keys.
- Prefer local output files so Codex can display results with `![alt](/absolute/path.png)`.
- Use `IMAGEGEN_OUTPUT_DIR` for default output location when set.

## Workflow

1. Confirm `IMAGEGEN_API_KEY` and `IMAGEGEN_BASE_URL` are available without printing their values.
2. Use `scripts/generate_image.py` for text-to-image requests.
3. Pass `--input-image` for image-to-image or edit requests.
4. Save the output image to a local file. If the user does not request a path, let the wrapper choose one.
5. Treat HTTP success plus `data[0].b64_json` or `data[0].url` as transport success.
6. For edits, inspect the output against the source image when visual fidelity matters.
7. Show generated local outputs with Markdown image syntax and an absolute path.

## Commands

Text-to-image:

```bash
python3 /path/to/openai-imagegen/scripts/generate_image.py \
  --prompt "A clean product-style render of a ceramic coffee mug on a white table" \
  --output /tmp/openai-imagegen-output.png
```

Image edit:

```bash
python3 /path/to/openai-imagegen/scripts/generate_image.py \
  --input-image /absolute/path/input.png \
  --prompt "Preserve the subject and change the background to a bright studio setup" \
  --output /tmp/openai-imagegen-edit.png
```

Override model per request only when the user asks or when the configured endpoint requires it:

```bash
python3 /path/to/openai-imagegen/scripts/generate_image.py \
  --model "$IMAGEGEN_MODEL" \
  --prompt "A minimalist app icon, flat vector style" \
  --output /tmp/app-icon.png
```

## Troubleshooting

- Missing key: set `IMAGEGEN_API_KEY` in the environment that launches Codex.
- Missing endpoint: set `IMAGEGEN_BASE_URL`, for example `https://example.com/v1`.
- Model not found: set `IMAGEGEN_MODEL` to a model name or gateway alias supported by the endpoint.
- Invalid JSON response: re-run with `--response-json /tmp/imagegen-response.json` and inspect the error fields without exposing secrets.
- Image edit ignored the source image: report it as a functional failure even if the API returned HTTP 200.

See `references/api.md` for endpoint details when manual debugging is needed.
