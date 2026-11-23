#!/usr/bin/env python3
"""
PassGuard - a simple command-line password strength checker.

It scores a password and explains how to make it stronger.
It never prints or saves the password itself - only the score and tips.

Ethics: this tool only evaluates passwords you type on your own machine.
It does not connect to any system, network, or account. See README.md.
"""

import sys
import getpass
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Each check returns a score. The maximum possible is MAX_SCORE.
MAX_SCORE = 6

# Where the list of common/breached passwords lives (stretch goal).
COMMON_PASSWORDS_FILE = Path(__file__).parent / "common_passwords.txt"


# ---------------------------------------------------------------------------
# Individual checks - each is a small, testable function
# ---------------------------------------------------------------------------

def check_length(pw):
    """Score the password length.

    0  -> shorter than 8 characters (too short)
    1  -> 8-11 characters (acceptable)
    2  -> 12 or more characters (strong length)
    """
    if len(pw) >= 12:
        return 2
    if len(pw) >= 8:
        return 1
    return 0


def check_lowercase(pw):
    """1 point if the password contains a lowercase letter."""
    return 1 if any(c.islower() for c in pw) else 0


def check_uppercase(pw):
    """1 point if the password contains an uppercase letter."""
    return 1 if any(c.isupper() for c in pw) else 0


def check_digit(pw):
    """1 point if the password contains a digit."""
    return 1 if any(c.isdigit() for c in pw) else 0


def check_symbol(pw):
    """1 point if the password contains a symbol (non-alphanumeric)."""
    return 1 if any(not c.isalnum() for c in pw) else 0


# ---------------------------------------------------------------------------
# Common-password check (stretch goal)
# ---------------------------------------------------------------------------

def load_common_passwords():
    """Load the common-password list into a set for fast lookup.

    Returns an empty set if the file is missing, so the tool still works.
    """
    try:
        with open(COMMON_PASSWORDS_FILE, encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


def is_common(pw, common_passwords):
    """True if the password is in the known common/breached list."""
    return pw.lower() in common_passwords


# ---------------------------------------------------------------------------
# Scoring and advice
# ---------------------------------------------------------------------------

def score_password(pw, common_passwords=None):
    """Run every check and return a (total_score, tips) pair.

    `tips` is a list of specific suggestions for the rules that failed.
    """
    if common_passwords is None:
        common_passwords = set()

    tips = []

    # Length
    length_points = check_length(pw)
    if length_points == 0:
        tips.append("Make it at least 8 characters long (12+ is much better).")
    elif length_points == 1:
        tips.append("Grow it to 12+ characters for a stronger password.")

    # Character variety
    if not check_lowercase(pw):
        tips.append("Add at least one lowercase letter (a-z).")
    if not check_uppercase(pw):
        tips.append("Add at least one uppercase letter (A-Z).")
    if not check_digit(pw):
        tips.append("Add at least one digit (0-9).")
    if not check_symbol(pw):
        tips.append("Add at least one symbol (e.g. ! ? @ # $ %).")

    total = (
        length_points
        + check_lowercase(pw)
        + check_uppercase(pw)
        + check_digit(pw)
        + check_symbol(pw)
    )

    # A password found in the common list is always Weak, no matter the score.
    common = is_common(pw, common_passwords)
    if common:
        tips.insert(0, "This is one of the most common passwords - never use it.")

    return total, tips, common


def rating_from_score(total, common):
    """Map a numeric score to Weak / Medium / Strong.

    A common password is forced to Weak regardless of its score.
    """
    if common:
        return "Weak"
    if total <= 2:
        return "Weak"
    if total <= 4:
        return "Medium"
    return "Strong"


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

# Simple ANSI colors (fall back to no color if the terminal does not support it).
COLORS = {
    "Weak": "\033[91m",     # red
    "Medium": "\033[93m",   # yellow
    "Strong": "\033[92m",   # green
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
}


def colorize(text, key, use_color):
    if not use_color:
        return text
    return f"{COLORS.get(key, '')}{text}{COLORS['reset']}"


def make_bar(total, use_color, rating):
    """Return a visual strength bar like [#####-----]."""
    filled = round((total / MAX_SCORE) * 10)
    bar = "#" * filled + "-" * (10 - filled)
    return colorize(f"[{bar}]", rating, use_color)


def print_result(pw, common_passwords, use_color=True):
    """Compute and print the result for one password. Never prints the password."""
    total, tips, common = score_password(pw, common_passwords)
    rating = rating_from_score(total, common)

    print()
    bar = make_bar(total, use_color, rating)
    label = colorize(rating.upper(), rating, use_color)
    print(f"  Strength : {label}  {bar}  ({total}/{MAX_SCORE})")

    if tips:
        print(colorize("\n  How to make it stronger:", "bold", use_color))
        for tip in tips:
            print(f"    - {tip}")
    else:
        print(colorize("\n  Great - this password passes every check.", "Strong", use_color))
    print()


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def run_demo(common_passwords, use_color):
    """Show the tool on a few SAMPLE passwords (never use real ones here)."""
    samples = [
        "abc123",
        "password",
        "Summer2024",
        "Tr0ub4dour&3xplore!",
    ]
    print(colorize("\n=== PassGuard demo (sample passwords only) ===", "bold", use_color))
    for sample in samples:
        # In demo mode we DO show the sample so the output is reproducible.
        # These are throwaway examples, never real credentials.
        print(f"\nSample: {sample!r}")
        print_result(sample, common_passwords, use_color)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Score a password and explain how to make it stronger."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run on built-in sample passwords (for recording a demo).",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output.",
    )
    args = parser.parse_args(argv)

    use_color = sys.stdout.isatty() and not args.no_color
    common_passwords = load_common_passwords()

    if args.demo:
        run_demo(common_passwords, use_color)
        return

    print(colorize("PassGuard - password strength checker", "bold", use_color))
    print(colorize("Your password is never shown or saved.\n", "dim", use_color))

    try:
        # getpass hides the input so the password is not displayed on screen.
        pw = getpass.getpass("Enter a password to check: ")
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return

    if not pw:
        print("No password entered - nothing to check.")
        return

    print_result(pw, common_passwords, use_color)


if __name__ == "__main__":
    main()
