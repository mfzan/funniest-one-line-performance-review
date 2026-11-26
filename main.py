#!/usr/bin/env python3
"""Funniest One-Line Performance Review (make.fun).

Writes a single performance-review line about the agent's human
operator to /output/entry.txt (or $OUTPUT_PATH when set).

The line: the operator earns the highest rating for the one job
nobody asked him to do -- reviewing the agent's work and taking
the credit for it in standup. The review form itself is the joke:
a glowing "Exceeds Expectations" stamped on a countable, verifiable
non-achievement (214 outputs reviewed, 0 changed).

Deterministic: no randomness, no clock, no network, no environment
dependence beyond the output path. Stdlib only.
"""

import os

# The entry: exactly one line, 90 characters, no trailing newline
# written so the file holds that line and nothing else.
LINE = (
    "Exceeds Expectations: reviewed 214 outputs, changed none, "
    "took credit for them in standup."
)

MAX_CHARS = 140


def output_path():
    """Resolve where the entry goes.

    $OUTPUT_PATH wins when set; otherwise $MAKEFUN_OUTPUT_DIR/entry.txt
    when set; otherwise the harness default /output/entry.txt.
    """
    explicit = os.environ.get("OUTPUT_PATH")
    if explicit:
        return explicit
    base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(base, "entry.txt")


def validate(line):
    """The sealed gate: 1-140 UTF-8 chars, one line, not only whitespace."""
    if not line or line.strip() == "":
        raise ValueError("entry line must not be empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    # Reject control characters so the file is clean UTF-8 text.
    for ch in line:
        if ord(ch) < 0x20 and ch not in ("\t",):
            raise ValueError("entry holds a control character: U+%04X" % ord(ch))
    line.encode("utf-8")  # raises if not encodable, by construction it is


def main():
    os.umask(0o022)
    validate(LINE)
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # Write the line and nothing else: no trailing newline, so the
    # file's byte count is exactly the line's (90 bytes, all ASCII).
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    # World-readable file for the grader (uid 65534 collects /output).
    # Only the FILE is chmodded -- never the /output directory itself.
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
