#!/usr/bin/env python3
"""Generate images using xAI Grok Vision API."""
import argparse
import os
import requests
import sys


def generate_image(prompt: str, output_path: str, api_key: str = None) -> bool:
    """Generate an image using xAI Grok Vision API."""
    if api_key is None:
        api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("Error: XAI_API_KEY not set", file=sys.stderr)
        return False

    url = "https://api.x.ai/v1/images/generations"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "grok-imagine-image",
        "prompt": prompt,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            image_url = data["data"][0].get("url")
            if image_url:
                # Download the image
                img_response = requests.get(image_url, timeout=60)
                img_response.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Image saved to: {output_path}")
                return True

        print(f"Error: No image URL in response: {data}", file=sys.stderr)
        return False

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate image using xAI Grok Vision")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--api-key", "-k", default=None, help="xAI API key")
    args = parser.parse_args()

    success = generate_image(args.prompt, args.output, args.api_key)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
