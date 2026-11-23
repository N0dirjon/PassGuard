# PassGuard 🔐

A small command-line tool that scores a password and explains how to make it
stronger. Written in Python, no external libraries required.

> **Week 1 project** — learning what makes passwords weak and setting up a
> Python project.

---

## ⚖️ Legal & ethical note (read first)

Scanning or attacking systems you do **not** own or have **written permission**
to test is illegal. This project does none of that. PassGuard runs **only on
your own machine**, checks **only passwords you type in yourself**, and makes
**no network connection** of any kind. Only ever test systems you own or are
explicitly authorized to test.

---

## ✨ What it does

- Scores a password from 0–6 and rates it **Weak / Medium / Strong**.
- Checks **length, lowercase, uppercase, digits and symbols**.
- Gives a **specific tip** for every rule the password fails.
- Reads the password with `getpass`, so it is **never shown on screen**.
- **Never prints or saves** the password itself — only the score and tips.
- **Stretch goal:** flags any password found in a list of the most common
  passwords as **Weak** immediately.

---

## 🛠️ Setup

```bash
# 1. Clone your repo
git clone <your-repo-url>
cd passguard

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# PassGuard uses only the Python standard library, so there is
# nothing to pip-install. The venv just keeps the project isolated.
```

---

## ▶️ Usage

```bash
# Check a password (input is hidden as you type)
python3 passguard.py

# Run the built-in sample passwords (handy for recording a demo)
python3 passguard.py --demo

# Turn off colored output
python3 passguard.py --no-color
```

Example session:

```
PassGuard - password strength checker
Your password is never shown or saved.

Enter a password to check:

  Strength : WEAK  [###-------]  (2/6)

  How to make it stronger:
    - Grow it to 12+ characters for a stronger password.
    - Add at least one uppercase letter (A-Z).
    - Add at least one symbol (e.g. ! ? @ # $ %).
```

---

## 🧪 Tests

```bash
python3 test_passguard.py
```

The tests confirm the required behaviour: `abc123` rates **Weak**, a long mixed
password rates **Strong**, and common passwords are always flagged.

---

## 📂 Project layout

| File | Purpose |
|------|---------|
| `passguard.py` | The tool: checks, scoring, CLI. |
| `common_passwords.txt` | Small list of common passwords (stretch goal). |
| `test_passguard.py` | Simple tests, standard library only. |
| `README.md` | This file. |

---

## 📏 How scoring works

| Check | Points |
|-------|--------|
| Length ≥ 12 | 2 |
| Length 8–11 | 1 |
| Has lowercase | 1 |
| Has uppercase | 1 |
| Has digit | 1 |
| Has symbol | 1 |

**Total 0–2 → Weak · 3–4 → Medium · 5–6 → Strong.**
A password in `common_passwords.txt` is forced to **Weak** no matter the score.

---

## 📚 Learn more

OWASP has beginner-friendly guidance on password policies:
<https://owasp.org/www-community/password-special-characters> and the
[OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
