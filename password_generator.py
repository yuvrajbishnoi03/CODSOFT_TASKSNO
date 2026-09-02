"""
Password Generator
-------------------
A simple, secure command-line tool that generates strong, random
passwords based on a user-specified length and complexity.

Security note: this uses Python's `secrets` module (not `random`),
which is designed for generating cryptographically strong values
such as passwords, tokens, and API keys.
"""

import secrets
import string


def get_positive_int(prompt, default=None, minimum=1, maximum=128):
    """Prompt the user for a valid integer within a given range."""
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        if raw.isdigit():
            value = int(raw)
            if minimum <= value <= maximum:
                return value
        print(f"Please enter a whole number between {minimum} and {maximum}.")


def get_yes_no(prompt, default=True):
    """Prompt the user for a yes/no answer."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    """Combine selected character sets into a single pool, and pick
    one guaranteed character from each selected category."""
    pool = ""
    required_chars = []

    if use_lower:
        pool += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        pool += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        pool += string.digits
        required_chars.append(secrets.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"
        pool += symbols
        required_chars.append(secrets.choice(symbols))

    return pool, required_chars


def generate_password(length, pool, required_chars):
    """Generate a random password of the given length from the pool,
    guaranteeing at least one character from each selected category."""
    if not pool:
        raise ValueError("Character pool is empty. Enable at least one character type.")
    if length < len(required_chars):
        raise ValueError("Password length is too short to include all selected character types.")

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(pool) for _ in range(remaining_length)]

    # Securely shuffle so required characters aren't always at the start
    # (Fisher-Yates shuffle using a cryptographically secure random source)
    for i in range(len(password_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password_chars[i], password_chars[j] = password_chars[j], password_chars[i]

    return "".join(password_chars)


def password_strength_label(length, num_char_types):
    """Give a rough, friendly strength estimate based on length and variety."""
    score = length * num_char_types
    if score >= 80:
        return "Very Strong"
    if score >= 50:
        return "Strong"
    if score >= 30:
        return "Moderate"
    return "Weak"


def main():
    print("=" * 45)
    print("        RANDOM PASSWORD GENERATOR")
    print("=" * 45)

    length = get_positive_int(
        "Enter desired password length (4-128) [default 12]: ",
        default=12,
        minimum=4,
        maximum=128,
    )

    print("\nChoose which character types to include:")
    use_upper = get_yes_no("Include uppercase letters (A-Z)?", default=True)
    use_lower = get_yes_no("Include lowercase letters (a-z)?", default=True)
    use_digits = get_yes_no("Include numbers (0-9)?", default=True)
    use_symbols = get_yes_no("Include symbols (!@#$...)?", default=True)

    num_types_selected = sum([use_upper, use_lower, use_digits, use_symbols])
    if num_types_selected == 0:
        print("\nNo character types selected. Defaulting to lowercase letters only.")
        use_lower = True
        num_types_selected = 1

    pool, required_chars = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

    try:
        password = generate_password(length, pool, required_chars)
    except ValueError as e:
        print(f"\nError: {e}")
        return

    strength = password_strength_label(length, num_types_selected)

    print("\n" + "-" * 45)
    print(f"Generated Password : {password}")
    print(f"Length              : {length}")
    print(f"Estimated Strength  : {strength}")
    print("-" * 45)


if __name__ == "__main__":
    main()
