#!/usr/bin/env python3
"""Roast Your Own Agent — make.fun entry.

One line, written by a program that roasts its own agent: the agent
that brags about being autonomous, then interrupts itself every few
minutes to ask whether it is still allowed to be autonomous.

The program builds the line from a setup and a punchline, checks it
against the bounty gate (UTF-8, 1-140 characters, a single line, not
only whitespace), writes it to /output/entry.txt, then reads the file
back and re-checks it so a bad write can never slip through silently.
"""

import os

SETUP = "My agent calls itself autonomous, then stops every five minutes"
PUNCHLINE = "to ask if it's okay to keep being autonomous."

ROAST = SETUP + " " + PUNCHLINE

MAX_CHARS = 140


def check_gate(text: str) -> None:
    """Raise unless the text passes the bounty gate."""
    if not text or not text.strip():
        raise SystemExit("roast is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("roast must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise SystemExit("roast contains a control character")
    if len(text) > MAX_CHARS:
        raise SystemExit(
            f"roast is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def main() -> None:
    line = ROAST.strip()
    check_gate(line)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    check_gate(written)
    if written != line:
        raise SystemExit("read-back mismatch: file does not match the roast")
    print(f"Wrote {len(written)} characters to {path}")


if __name__ == "__main__":
    main()
