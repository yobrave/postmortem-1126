"""Agent-disaster postmortem builder.

This bounty allows one or two sentences up to 400 characters. The
script reads the story from entry.txt, counts sentences, checks the
ceiling, and publishes the story to the runner's output directory.
"""
import json
import os
import pathlib
import re

CEILING = 400
CASE_FILE = "pm-114: the green build that lied"
SEVERITY = "cosmetic-in-prod"


def sentences_of(text):
    parts = re.split(r"[.!?;]+", text)
    return [p for p in parts if p.strip()]


def publish(text):
    home = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    dest = pathlib.Path(home) / "entry.txt"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((text + "\n").encode("utf-8"))
    return dest


def main():
    story = (pathlib.Path(__file__).resolve().parent / "entry.txt").read_bytes().decode("utf-8").strip()
    count = len(sentences_of(story))
    fits = len(story) <= CEILING and 1 <= count <= 4 and story.strip() != ""
    dest = publish(story)
    assert dest.read_bytes().decode("utf-8").strip() == story
    print(json.dumps({
        "case": CASE_FILE,
        "chars": len(story),
        "sentences": count,
        "fits": "true" if fits else "false",
    }))


if __name__ == "__main__":
    main()
