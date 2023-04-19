def clear() -> None:
    """Efface l'écran."""
    print("\x1b[3J\x1b[H\x1b[J", end="")


def pitalic(s: str, end="\n") -> None:
    """Affiche le texte en italique."""
    print("\x1b[3m" + s + "\x1b[0m", end=end)


def pbold(s: str) -> None:
    """Affiche le texte en gras."""
    print("\x1b[1m" + s + "\x1b[0m")


def perror(s: str) -> None:
    """Affiche le texte en rouge et en gras."""
    print("\x1b[31m" + s + "\x1b[0m")


def binput(prompt: str) -> bool:
    """Demande à l'utilisateur d'entrer une valeur booléenne."""
    bprompt = "\x1b[1m" + prompt + "\x1b[0m"
    try:
        str_input = input(bprompt).lower()
    except KeyboardInterrupt:
        print()
        exit(0)
    bool_input = ['true', '1', 't', 'y', 'yes', 'o',
                  'false', '0', 'f', 'n', 'no', 'n']

    while True:
        try:
            if bool_input.index(str_input) < 6:
                return True
            else:
                return False
        except ValueError:
            try:
                str_input = input(bprompt).lower()
            except KeyboardInterrupt:
                print()
                exit(0)


def print_table(data: list, headers: list) -> None:
    """Affiche les données dans un tableau."""
    max_length_column = [0] * len(headers)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if len(str(data[i][j])) > max_length_column[j]:
                max_length_column[j] = len(str(data[i][j]))

    print("\x1b[1m|", end="")
    for i, header in enumerate(headers):
        if len(header) > max_length_column[i]:
            max_length_column[i] = len(header)
        print(" " + header.ljust(max_length_column[i]) + " |", end="")
    print("\x1b[0m")

    for row in data:
        print("|", end="")
        for i in range(len(row)):
            print(" " + str(row[i]).ljust(max_length_column[i]) + " |", end="")
        print()


def print_as_form(inputs: list) -> list[str]:
    """Affiche un formulaire et renvoie les réponses de l'utilisateur."""
    answers = [None] * len(inputs)

    # Calcul des longueurs des labels
    inputs = [i + " : " for i in inputs]
    label_lengths = [len(i) for i in inputs]
    n_labels = len(inputs)

    # Affichage des labels
    print("\x1b[1m", end="")
    print(*inputs, sep="\n", end="")
    print("\x1b[0m", end="")

    # Affichage des champs de saisie
    print(f"\x1b[{n_labels - 1}F", end="")
    for i in range(n_labels):
        print(f"\x1b[{label_lengths[i]}C", end="")
        try:
            answers[i] = input()
        except KeyboardInterrupt:
            clear()
            return None
    return answers
