# API Reference

Use this reference only when debugging endpoint behavior or making manual calls.

## Configuration

```bash
export IMAGEGEN_API_KEY="your-image-api-key"
export IMAGEGEN_BASE_URL="https://your-openai-compatible-host/v1"
export IMAGEGEN_MODEL="gpt-image-2"
```

Never paste real keys into files, prompts, logs, commits, or screenshots.

## Text To Image

Endpoint: `POST /images/generations`

```bash
curl -sS "$IMAGEGEN_BASE_URL/images/generations" \
  -H "Authorization: Bearer $IMAGEGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"${IMAGEGEN_MODEL:-gpt-image-2}"'",
    "prompt": "A clean product-style render of a glass teapot on a white table",
    "size": "1024x1024",
    "n": 1
  }'
```

## Image To Image

Endpoint: `POST /images/edits`

Send multipart form data with the source image in field `image`.

```bash
curl -sS "$IMAGEGEN_BASE_URL/images/edits" \
  -H "Authorization: Bearer $IMAGEGEN_API_KEY" \
  -F model="${IMAGEGEN_MODEL:-gpt-image-2}" \
  -F size=1024x1024 \
  -F n=1 \
  -F image=@/absolute/path/input.png \
  -F prompt="Preserve the subject and change the background to a bright studio setup"
```

## Response Checks

- Success should include `data[0].b64_json` or `data[0].url`.
- `revised_prompt` may appear on the image item or top-level object.
- For edits, transport success is not enough: visually compare output with input when preservation matters.
