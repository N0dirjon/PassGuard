#!/usr/bin/env python3
"""
Quick tests for passguard.py.

Run with:  python3 test_passguard.py
No external libraries needed.
"""

import passguard as pg


def expect(name, got, want):
    status = "PASS" if got == want else "FAIL"
    print(f"[{status}] {name}: got={got!r} want={want!r}")
    return got == want


def main():
    common = pg.load_common_passwords()
    all_ok = True

    # Length scoring
    all_ok &= expect("short length", pg.check_length("abc"), 0)
    all_ok &= expect("medium length", pg.check_length("abcdefgh"), 1)
    all_ok &= expect("long length", pg.check_length("abcdefghijkl"), 2)

    # Character checks
    all_ok &= expect("has lowercase", pg.check_lowercase("aB1!"), 1)
    all_ok &= expect("no uppercase", pg.check_uppercase("ab1!"), 0)
    all_ok &= expect("has digit", pg.check_digit("ab1!"), 1)
    all_ok &= expect("has symbol", pg.check_symbol("ab1!"), 1)
    all_ok &= expect("no symbol", pg.check_symbol("ab1c"), 0)

    # Required behaviour from the brief:
    # abc123 must be Weak, a long mixed password must be Strong.
    weak_total, _, weak_common = pg.score_password("abc123", common)
    all_ok &= expect("abc123 is Weak", pg.rating_from_score(weak_total, weak_common), "Weak")

    strong_total, _, strong_common = pg.score_password("Tr0ub4dour&3xplore!", common)
    all_ok &= expect(
        "long mixed is Strong",
        pg.rating_from_score(strong_total, strong_common),
        "Strong",
    )

    # Common-password override: always Weak even if it looks varied.
    _, _, is_c = pg.score_password("password", common)
    all_ok &= expect("password is flagged common", is_c, True)

    print()
    print("ALL TESTS PASSED" if all_ok else "SOME TESTS FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
