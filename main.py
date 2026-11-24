"""Say What Actually Broke: one line of honest error copy.

Writes a single-line software error message to /output/entry.txt.
Gate: UTF-8 text, 1 to 200 characters, not only white space, one line.

Standard library only (os, sys). No network, no clock, no randomness:
the output is the same on every run.

The winning line (R1-R3, head-to-head on the kit rubric against the
strongest visible field lines, see NOTES.md): a two-factor login code
that expired mid-typing. The failure is universal, the mechanism is
precise (codes live 30 seconds), the next step is concrete, and the
punchline is a line a reader repeats out loud.
"""

import os
import sys

# The winning line, 163 characters, one line.
LINE = (
    "Your login code expired while you were typing it: "
    "codes live 30 seconds and humans do not type that fast. "
    "Ask for a fresh one, and this time type like you mean it."
)

# Candidates drafted in R1, judged head-to-head on the kit rubric.
# F won; D and B were runners-up; the rest lost on the criterion named.
CANDIDATES = {
    "A": "Our DNS forgot where this server lives, so your request is "
         "wandering the internet asking strangers for directions. "
         "Give it a minute, then try again.",
    "B": "You clicked Save fourteen times. We heard the first one; the "
         "queue is still chewing on it. Wait a minute, then click once, "
         "like you mean it.",
    "C": "Your clock says 2019, so our certificate looks expired and this "
         "page refuses to load. Set the time right and we will both "
         "pretend this never happened.",
    "D": "We updated one tiny library and it pulled the whole site down "
         "like a Jenga tower with opinions. We are putting the old one "
         "back; try again in five minutes.",
    "E": "This page is from Tuesday. The cache refuses to believe anything "
         "has changed since, including you. Hard-refresh and it will "
         "finally meet today.",
    "F": "Your login code expired while you were typing it, which is the "
         "system working exactly as designed and exactly as nobody "
         "wanted. Ask for a new one and type faster.",
}

# R2 challengers, both judged against F (see NOTES.md).
CHALLENGERS = {
    # F2: fresh punchline, but 170 chars, the longest of all; rejected on length.
    "F2": "Your login code expired while you were typing it. The system "
          "worked exactly as designed, which is exactly the problem. Ask "
          "for a new code and type like it owes you money.",
    # F3: R2 winner, 158 chars; lost R3 to F4 on first-read clarity.
    "F3": "That login code expired mid-typing, because codes live for 30 "
          "seconds and humans do not type that fast. Ask for a fresh one; "
          "this time, type like you mean it.",
}

MAX_CHARS = 200


def check(text):
    """Return a list of gate failures for a candidate line (empty = valid)."""
    problems = []
    if not text or not text.strip():
        problems.append("empty or whitespace-only")
    if len(text) > MAX_CHARS:
        problems.append("too long: %d chars" % len(text))
    if "\n" in text or "\r" in text:
        problems.append("not a single line")
    return problems


def main():
    for name, text in list(CANDIDATES.items()) + list(CHALLENGERS.items()):
        problems = check(text)
        if problems:
            print("candidate %s INVALID: %s" % (name, "; ".join(problems)),
                  file=sys.stderr)
            return 1
    problems = check(LINE)
    if problems:
        print("winning line INVALID: %s" % "; ".join(problems),
              file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE:
        print("round-trip mismatch: wrote %d chars, read back %d"
              % (len(LINE), len(written)), file=sys.stderr)
        return 1
    print("wrote %s (%d chars, 1 line)" % (path, len(LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
