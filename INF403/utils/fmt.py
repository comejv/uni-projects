def pitalic(s: str) -> None:
    """Affiche le texte en italique."""
    print("\x1b[3m" + s + "\x1b[0m")


def pbold(s: str) -> None:
    """Affiche le texte en gras."""
    print("\x1b[1m" + s + "\x1b[0m")


def perror(s: str) -> None:
    """Affiche le texte en rouge."""
    print("\x1b[31m" + s + "\x1b[0m")


def binput(prompt: str) -> bool:
    """Demande à l'utilisateur d'entrer une valeur booléenne."""
    str_input = pbold(prompt)
    bool_input = ['true', '1', 't', 'y', 'yes',
                  'false', '0', 'f', 'n', 'no']

    while str_input not in bool_input:
        print("\x1b[1F\x1b[K", end="")
        pbold(prompt)
        str_input = input()
    if str_input.lower() in bool_input[:5]:
        return True
    return False
