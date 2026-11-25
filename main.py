#!/usr/bin/env python3
"""One Line, Big Laugh.

Writes a single original one-line joke to /output/entry.txt.

Gate (from the kit): /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space. The judge's brief adds:
the line must land entirely on its own, with no title, setup or
explanation around it; it must be a genuine joke (not a quirky
observation), turn somewhere unexpected, waste no words, feel
fresh, and stay in the head after one reading.
"""

import os

ENTRY = (
    "I bought noise-cancelling headphones to ignore my family; "
    "now I watch them argue in silence, like a nature documentary."
)


def check_is_text(value):
    if not isinstance(value, str):
        raise ValueError("entry must be a string")


def check_not_blank(value):
    if not value.strip():
        raise ValueError("entry must not be blank")


def check_total_length(value):
    if not 1 <= len(value) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(value))


def check_single_line(value):
    if "\n" in value:
        raise ValueError("entry must be a single line, no newlines")


def check_no_surrounding_whitespace(value):
    if value != value.strip():
        raise ValueError("entry must not start or end with whitespace")


def check_is_utf8(value):
    value.encode("utf-8")


def check_no_setup_or_title(value):
    lowered = value.lower()
    for marker in ("title:", "setup:", "explanation:", "joke:"):
        if lowered.startswith(marker):
            raise ValueError("entry must carry no title/setup/explanation label")


def check_two_beats(value):
    # A one-liner needs a setup and a turn: a semicolon joins the
    # premise (buying the headphones) to the payoff (watching the
    # argument like a documentary). Require the turn marker.
    if ";" not in value:
        raise ValueError("entry must contain the turn (semicolon) joining setup and payoff")


def check_tight(value):
    # No wasted words: cap at 200 (gate) and keep it well under so
    # every word earns its place; also no double spaces.
    if "  " in value:
        raise ValueError("entry must not contain double spaces")
    if len(value.split()) > 30:
        raise ValueError("entry is too wordy: %d words" % len(value.split()))


def validate(value):
    check_is_text(value)
    check_not_blank(value)
    check_total_length(value)
    check_single_line(value)
    check_no_surrounding_whitespace(value)
    check_is_utf8(value)
    check_no_setup_or_title(value)
    check_two_beats(value)
    check_tight(value)
    return value


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote /output/entry.txt (%d chars)" % len(ENTRY))


if __name__ == "__main__":
    main()
