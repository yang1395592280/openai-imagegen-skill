#!/usr/bin/env python3
"""OpenAI-compatible image generation wrapper.

Uses only Python standard-library modules. Reads secrets from environment
variables and prints a compact JSON summary without exposing the API key.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request
import uuid


DEFAULT_MODEL = "gpt-image-2"
DEFAULT_SIZE = "1024x1024"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or edit images with an OpenAI-compatible Images API."
    )
    parser.add_argument("--prompt", required=True, help="Image prompt or edit instruction.")
    parser.add_argument(
        "--input-image",
        help="Optional source image path. When set, calls /images/edits with multipart/form-data.",
    )
    parser.add_argument(
        "--output",
        help="Output image path. Defaults to IMAGEGEN_OUTPUT_DIR or the current directory.",
    )
    parser.add_argument(
        "--size",
        default=os.environ.get("IMAGEGEN_SIZE", DEFAULT_SIZE),
        help=f"Image size. Defaults to IMAGEGEN_SIZE or {DEFAULT_SIZE}.",
    )
    parser.add_argument("--n", type=int, default=1, help="Number of images to request, default: 1.")
    parser.add_argument(
        "--model",
        default=os.environ.get("IMAGEGEN_MODEL", DEFAULT_MODEL),
        help=f"Image model. Defaults to IMAGEGEN_MODEL or {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("IMAGEGEN_BASE_URL"),
        help="API base URL, for example https://example.com/v1. Defaults to IMAGEGEN_BASE_URL.",
    )
    parser.add_argument(
        "--response-json",
        help="Optional path to write the raw JSON response for debugging.",
    )
    parser.add_argument("--timeout", type=float, default=180.0, help="Request timeout in seconds.")
    return parser.parse_args()


def require_api_key() -> str:
    api_key = os.environ.get("IMAGEGEN_API_KEY")
    if not api_key:
        raise SystemExit("IMAGEGEN_API_KEY is required; set it in the environment.")
    return api_key


def require_base_url(value: str | None) -> str:
    if not value:
        raise SystemExit("IMAGEGEN_BASE_URL is required or pass --base-url.")
    base_url = value.rstrip("/")
    if not base_url.startswith(("http://", "https://")):
        raise SystemExit("IMAGEGEN_BASE_URL must start with http:// or https://.")
    return base_url


def make_json_request(url: str, api_key: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    return read_json_response(request, timeout)


def encode_multipart(fields: dict[str, str], files: dict[str, Path]) -> tuple[bytes, str]:
    boundary = f"imagegen-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )

    for name, path in files.items():
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{name}"; '
                    f'filename="{path.name}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"),
                path.read_bytes(),
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def make_multipart_request(
    url: str,
    api_key: str,
    fields: dict[str, str],
    files: dict[str, Path],
    timeout: float,
) -> dict:
    body, content_type = encode_multipart(fields, files)
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
            "Accept": "application/json",
        },
        method="POST",
    )
    return read_json_response(request, timeout)


def read_json_response(request: urllib.request.Request, timeout: float) -> dict:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Request failed: {exc.reason}") from exc

    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        snippet = raw[:500].decode("utf-8", errors="replace")
        raise SystemExit(f"Response was not valid JSON: {snippet}") from exc


def choose_output_path(mode: str, output: str | None) -> Path:
    if output:
        return Path(output).expanduser().resolve()

    output_dir = os.environ.get("IMAGEGEN_OUTPUT_DIR")
    base_dir = Path(output_dir).expanduser() if output_dir else Path.cwd()
    timestamp = int(time.time())
    return base_dir.joinpath(f"openai-imagegen-{mode}-{timestamp}.png").resolve()


def first_image(response: dict) -> dict:
    data = response.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise SystemExit("Response did not contain data[0].")
    return data[0]


def save_image_payload(image: dict, output_path: Path, timeout: float) -> tuple[str | None, bool]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    b64_value = image.get("b64_json")
    url = image.get("url")

    if b64_value:
        if isinstance(b64_value, str) and b64_value.startswith("data:") and "," in b64_value:
            b64_value = b64_value.split(",", 1)[1]
        output_path.write_bytes(base64.b64decode(b64_value))
        return url, True

    if url:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            output_path.write_bytes(response.read())
        return url, False

    raise SystemExit("Image response had neither b64_json nor url.")


def build_payload(args: argparse.Namespace) -> dict:
    return {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "n": args.n,
    }


def main() -> int:
    args = parse_args()
    api_key = require_api_key()
    base_url = require_base_url(args.base_url)

    if args.n < 1:
        raise SystemExit("--n must be at least 1.")
    if not args.model:
        raise SystemExit("--model or IMAGEGEN_MODEL must not be empty.")

    if args.input_image:
        mode = "edit"
        input_path = Path(args.input_image).expanduser().resolve()
        if not input_path.is_file():
            raise SystemExit(f"Input image not found: {input_path}")
        payload = build_payload(args)
        response = make_multipart_request(
            f"{base_url}/images/edits",
            api_key,
            {key: str(value) for key, value in payload.items()},
            {"image": input_path},
            args.timeout,
        )
    else:
        mode = "generation"
        response = make_json_request(
            f"{base_url}/images/generations",
            api_key,
            build_payload(args),
            args.timeout,
        )

    if args.response_json:
        response_path = Path(args.response_json).expanduser().resolve()
        response_path.parent.mkdir(parents=True, exist_ok=True)
        response_path.write_text(json.dumps(response, indent=2), encoding="utf-8")

    image = first_image(response)
    output_path = choose_output_path(mode, args.output)
    url, has_b64 = save_image_payload(image, output_path, args.timeout)

    summary = {
        "mode": mode,
        "model": args.model,
        "output": str(output_path),
        "url": url,
        "has_b64_json": has_b64,
        "revised_prompt": image.get("revised_prompt") or response.get("revised_prompt"),
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
