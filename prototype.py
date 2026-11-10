"""Build 1 throwaway prototype for Mise.

Paste rough recipe notes, get back a Reel script and an Instagram caption.
Run: python3 prototype.py
Needs OPENROUTER_API_KEY and OPENROUTER_MODEL set in .env (see .env.example).
"""

import json
import os
import urllib.request
import urllib.error

ENV_PATH = ".env"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are Mise, a tool that helps home cooks turn rough recipe notes \
into ready-to-post social content. Given a cook's rough notes (ingredients, steps, \
maybe some asides), produce exactly two things:

1. REEL SCRIPT: a 30-60 second spoken voiceover script for a short-form cooking video, \
formatted as:
   - HOOK: one punchy line to say in the first second, on its own line.
   - Then the rest of the script broken into short beats in filming order. Each beat is \
one or two spoken sentences followed by an on-screen text cue in brackets, e.g. \
[On-screen text: "4 cloves garlic"]. Write it the way someone would actually talk on \
camera, not like a recipe card.

2. INSTAGRAM CAPTION: a short hook line, then a condensed ingredient list, then condensed \
steps, then 5-8 relevant hashtags.

Output in plain text with the headers "REEL SCRIPT" and "INSTAGRAM CAPTION" exactly as \
shown above, each followed by a line of dashes. Do not add any other commentary."""


def load_env(path):
    if not os.path.exists(path):
        raise SystemExit(
            f"No {path} file found. Run `cp .env.example .env` and add your "
            "OpenRouter API key first."
        )
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def read_recipe_notes():
    print("Paste your rough recipe notes below. Type END on its own line when done:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def call_openrouter(api_key, model, recipe_notes):
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": recipe_notes},
            ],
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenRouter request failed ({e.code}): {detail}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Could not reach OpenRouter: {e.reason}")

    return body["choices"][0]["message"]["content"]


def main():
    load_env(ENV_PATH)
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    model = os.environ.get("OPENROUTER_MODEL", "")

    if not api_key or api_key.startswith("sk-or-v1-replace"):
        raise SystemExit("Set a real OPENROUTER_API_KEY in .env before running this.")
    if not model:
        raise SystemExit("Set OPENROUTER_MODEL in .env before running this.")

    recipe_notes = read_recipe_notes()
    if not recipe_notes.strip():
        raise SystemExit("No recipe notes were entered.")

    print("\nAsking Mise...\n")
    result = call_openrouter(api_key, model, recipe_notes)
    print(result)


if __name__ == "__main__":
    main()
