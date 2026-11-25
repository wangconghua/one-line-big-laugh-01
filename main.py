#!/usr/bin/env python3
"""One Line, Big Laugh.

Writes a single original one-line joke to /output/entry.txt.

Gate (from the kit): /output/entry.txt must be UTF-8 text of
1 to 200 characters, not only white space. The judge's brief adds:
the line must land entirely on its own, with no title, setup or
explanation around it; it must be a genuine joke (not a quirky
observation), turn somewhere unexpected, waste no words, feel
fresh, and stay in the head after one reading.

Validation runs in three stages: validate_structure checks the
shape of the line, validate_content checks the joke itself, and
validate_freshness guards originality (ASCII-only, no repeated
content word).
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


STOPWORDS = frozenset(
    {"i", "to", "my", "a", "an", "the", "in", "on", "like", "now",
     "them", "it", "is", "and", "of", "for", "with"}
)


def check_no_repeated_content_word(value):
    # Freshness: no content word may repeat; pronouns and stopwords
    # are allowed to recur, everything else must appear exactly once.
    seen = set()
    for raw in value.split():
        word = raw.strip(".,;:!?\"'").lower()
        if not word or word in STOPWORDS:
            continue
        if word in seen:
            raise ValueError("entry repeats content word %r" % word)
        seen.add(word)


def check_ascii_punctuation(value):
    # The line must survive any plain-text pipeline: only ASCII
    # letters, digits, spaces and ordinary punctuation allowed.
    for ch in value:
        if ord(ch) > 127:
            raise ValueError("entry must be ASCII-only, found %r" % ch)


def check_ends_with_period(value):
    # A finished joke ends on a full stop, not mid-thought.
    if not value.endswith("."):
        raise ValueError("entry must end with a full stop")


def check_no_blank_lines_inside(value):
    # No blank lines anywhere inside the entry (a single line has
    # none by definition, but guard against future multi-line edits).
    if "\n\n" in value or value.startswith("\n") or value.endswith("\n"):
        raise ValueError("entry must not contain blank lines")


def validate_structure(value):
    # Shape of the line: type, blankness, length, one line, clean
    # edges, encodable, no blank lines hiding inside.
    check_is_text(value)
    check_not_blank(value)
    check_total_length(value)
    check_single_line(value)
    check_no_surrounding_whitespace(value)
    check_is_utf8(value)
    check_no_blank_lines_inside(value)


def validate_content(value):
    # The joke itself: no label, a real turn, tight wording, and a
    # finished ending.
    check_no_setup_or_title(value)
    check_two_beats(value)
    check_tight(value)
    check_ends_with_period(value)


def validate_freshness(value):
    # Originality guards: plain ASCII and no content word repeated.
    check_ascii_punctuation(value)
    check_no_repeated_content_word(value)


def validate(value):
    validate_structure(value)
    validate_content(value)
    validate_freshness(value)
    return value


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    print("wrote /output/entry.txt (%d chars)" % len(ENTRY))


if __name__ == "__main__":
    main()
