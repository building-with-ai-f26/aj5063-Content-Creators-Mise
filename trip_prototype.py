"""Build 1 throwaway prototype for Fernweh.

Enter trip details and a profile for each friend, get back AI-suggested
restaurants and activities that fit the whole group.
Run: python3 trip_prototype.py
Needs OPENROUTER_API_KEY and OPENROUTER_MODEL set in .env (see .env.example).
"""

import json
import os
import urllib.request
import urllib.error

ENV_PATH = ".env"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are Fernweh, a virtual travel agent for friend groups. You are given \
trip details (destination, dates, group size, budget, vibe) and a short profile from each \
friend in the group (budget comfort, food preferences/restrictions, activity interests, \
energy level, dealbreakers).

Suggest exactly 8 restaurants and 8 activities in the destination that fit the whole group, \
balancing everyone's profiles, not just one person's. For each suggestion include:
- Name
- Price level ($, $$, $$$, or $$$$)
- One line: why this fits the group, referencing specific details from the profiles
- Rough cost per person

Label every single suggestion as "(unverified - AI-suggested, confirm before booking)" since \
you cannot check real-time availability, prices, or hours.

Output in plain text with the headers "RESTAURANTS" and "ACTIVITIES" exactly as shown above, \
each followed by a line of dashes, then a numbered list of exactly 8 items. Do not add any \
other commentary."""


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


def read_trip_details():
    print("Let's set up the trip.\n")
    destination = input("Destination: ")
    dates = input("Dates: ")
    group_size = input("Group size: ")
    budget = input("Budget (overall or per person): ")
    vibe = input("Vibe (e.g. relaxed, adventurous, foodie): ")
    return (
        f"Destination: {destination}\n"
        f"Dates: {dates}\n"
        f"Group size: {group_size}\n"
        f"Budget: {budget}\n"
        f"Vibe: {vibe}"
    )


def read_friend_profiles():
    print("\nNow enter a profile for each friend, simulating what they'd fill out "
          "through the trip link.")
    try:
        count = int(input("How many friend profiles will you enter? "))
    except ValueError:
        raise SystemExit("Please enter a whole number.")

    profiles = []
    for i in range(1, count + 1):
        print(
            f"\nFriend {i} profile — budget comfort, food preferences/restrictions, "
            "activity interests, energy level, dealbreakers. Type END on its own line "
            "when done:\n"
        )
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        profiles.append(f"Friend {i}:\n" + "\n".join(lines))

    return "\n\n".join(profiles)


def call_openrouter(api_key, model, user_content):
    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
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

    trip_details = read_trip_details()
    friend_profiles = read_friend_profiles()
    user_content = f"{trip_details}\n\nFriend profiles:\n\n{friend_profiles}"

    print("\nAsking Fernweh...\n")
    result = call_openrouter(api_key, model, user_content)
    print(result)


if __name__ == "__main__":
    main()
