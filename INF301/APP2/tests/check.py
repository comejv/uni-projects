#!/usr/bin/env python3

import sys
import os
import time
import argparse
from pathlib import Path
from subprocess import (
    check_output,
    run,
    Popen,
    PIPE,
    DEVNULL,
    CalledProcessError,
    TimeoutExpired,
)
import re

from enum import Enum

from typing import List, Tuple, NamedTuple

TSTDIR = Path(__file__).parent
TSTFILE = TSTDIR / "LISEZMOI.txt"


class ValgrindChoice(Enum):
    NO_VALGRIND = 0
    VALGRIND_QUIET = 1
    VALGRIND_NORMAL = 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--silent", "-q", action="store_true", help="Pass -silent to ./main"
    )
    parser.add_argument(
        "--no-interactive",
        "-I",
        action="store_false",
        dest="interactive",
        help="Do not offer to re-run failed tests",
    )

    parser.add_argument("lang", choices=["c", "py"], help="Language to test")
    parser.add_argument(
        "--mem",
        action="store_const",
        default=ValgrindChoice.NO_VALGRIND,
        const=ValgrindChoice.VALGRIND_NORMAL,
        help="Check memory leaks using Valgrind (C only)",
    )
    parser.add_argument(
        "--mem-quiet",
        action="store_const",
        default=ValgrindChoice.NO_VALGRIND,
        const=ValgrindChoice.VALGRIND_QUIET,
        dest="mem",
        help="Check memory leaks using Valgrind without printing details (C only)",
    )

    args = parser.parse_args()
    if args.lang != "c" and args.mem != ValgrindChoice.NO_VALGRIND:
        parser.error("--mem can only be provided with C language")
    return args


RED = check_output(["tput", "setaf", "1"], text=True)
GREEN = check_output(["tput", "setaf", "2"], text=True)
ORANGE = check_output(["tput", "setaf", "3"], text=True)
BLUE = check_output(["tput", "setaf", "4"], text=True) + check_output(
    ["tput", "bold"], text=True
)
NORMAL = check_output(["tput", "sgr0"], text=True)


def color(text, color):
    return "{}{}{}".format(color, text, NORMAL)


COL = int(check_output(["tput", "cols"]))
COL -= 20
if COL > 60:
    COL = 60

TIMEOUT = 2  # seconds allowed to complete


def failed_test(name, info, txtcolor):
    print("\r", " " * COL, color(info, txtcolor), end="")
    print("\r    Test " + color(name, ORANGE), end="")
    print("\r" + color("[-]", RED))


def passed_test(name):
    print("\r", " " * COL, color("[pass]", GREEN), end="")
    print("\r    Test " + color(name, ORANGE), end="")
    print("\r" + color("[+]", GREEN))


class ValgrindResult(NamedTuple):
    definitely_lost: int
    indirectly_lost: int
    possibly_lost: int

    @classmethod
    def without_leaks(cls):
        return cls(0, 0, 0)

    @staticmethod
    def _to_bytes(val: int) -> str:
        units = [" B", "KB", "MB", "GB"]
        shifts = 0
        while val > 1000 and shifts < len(units):
            shifts += 1
            val //= 1000
        return f"{val:>3}{units[shifts]}"

    @classmethod
    def _format_figure(cls, val: int, colorize: bool = False) -> str:
        out = cls._to_bytes(val)
        if colorize:
            return color(out, RED if val > 0 else GREEN)
        return out

    def __str__(self):
        return self.to_str(colorize=False)

    def __bool__(self):
        return not any(self)

    def to_str(self, colorize=True):
        return "LOST: {} | IND: {} | MAYBE: {}".format(
            self._format_figure(self.definitely_lost, colorize=colorize),
            self._format_figure(self.indirectly_lost, colorize=colorize),
            self._format_figure(self.possibly_lost, colorize=colorize),
        )


class CheckValgrindOutput:
    DEF_LOST_RE = re.compile(
        r"\sdefinitely lost: (?P<lost>[0-9,]+) bytes in (?P<blocks>[0-9,]+) blocks"
    )
    IND_LOST_RE = re.compile(
        r"\sindirectly lost: (?P<lost>[0-9,]+) bytes in (?P<blocks>[0-9,]+) blocks"
    )
    POSS_LOST_RE = re.compile(
        r"\spossibly lost: (?P<lost>[0-9,]+) bytes in (?P<blocks>[0-9,]+) blocks"
    )
    CLEAN_STR = "All heap blocks were freed -- no leaks are possible"

    class BadValgrindOutput(Exception):
        pass

    def _apply_re(self, stderr: str, rex: re.Pattern) -> Tuple[int, int]:
        res = rex.search(stderr)
        if res:
            return (
                int(res.group("lost").replace(",", "")),
                int(res.group("blocks").replace(",", "")),
            )
        raise self.BadValgrindOutput("Bad valgrind output")

    def __call__(self, stderr: str) -> ValgrindResult:
        if self.CLEAN_STR in stderr:
            return ValgrindResult.without_leaks()
        return ValgrindResult(
            self._apply_re(stderr, self.DEF_LOST_RE)[0],
            self._apply_re(stderr, self.IND_LOST_RE)[0],
            self._apply_re(stderr, self.POSS_LOST_RE)[0],
        )


check_valgrind_output = CheckValgrindOutput()


def do_test(test_name, args) -> bool:
    use_valgrind = False
    capture_output = False
    silent = args.silent
    if args.mem != ValgrindChoice.NO_VALGRIND:
        use_valgrind = True
        capture_output = True

    test_file = TSTDIR / (test_name + ".test")
    assert test_file.exists()

    # using 'yes' command to cancel all keypresses waiting
    command = 'yes | {valgrind} {main} {silent} "{test}"'.format(
        valgrind="valgrind" if use_valgrind else "",
        main="./main" if args.lang == "c" else "python3 ./main.py -ascii",
        silent="-silent" if silent else "",
        test=test_file,
    )

    print("\r    Test " + color(test_name, ORANGE), end="")
    try:
        run_result = run(
            command,
            shell=True,
            check=True,
            timeout=TIMEOUT,
            stdout=PIPE if capture_output else DEVNULL,
            stderr=PIPE if capture_output else DEVNULL,
            text=capture_output,
        )
        if use_valgrind:
            if args.mem == ValgrindChoice.VALGRIND_NORMAL:
                print(run_result.stderr)

            vg_out = check_valgrind_output(run_result.stderr)
            if not vg_out:
                failed_test(test_name, "[LEAK]", ORANGE)
                out = vg_out.to_str(colorize=True)
                print(" " * 8 + out)
                return False

    except KeyboardInterrupt:
        failed_test(test_name, "[INTERRUPTED]", ORANGE)
        time.sleep(0.3)  # to allow double ctrl-C to stop whole script
        return False

    except TimeoutExpired:
        failed_test(test_name, "[TIMEOUT]", RED)
        return False

    except CalledProcessError as e:
        if e.returncode == 1:
            failed_test(test_name, "[FAIL]", RED)
        elif e.returncode == 2:
            failed_test(test_name, "[TRICHE]", RED)
        elif e.returncode == 134:
            failed_test(test_name, "[ASSERTION]", RED)
        elif e.returncode == 139:
            failed_test(test_name, "[SEGFAULT]", RED)
        else:
            failed_test(test_name, "[SOME PROBLEM]", RED)
        return False

    else:
        passed_test(test_name)
        return True


def main():
    args = parse_args()
    failed: List[str] = []

    print(f"Directory for tests: {TSTDIR}")
    print(f"Getting tests files from {TSTFILE}")
    with TSTFILE.open("r") as f:
        for line in f.readlines():
            if line.startswith("-"):
                test = line[1:].strip()
                if not do_test(test, args):
                    failed.append(test)
            elif "Acte" in line:
                print(color("\n" + line + "=================", BLUE))

    print("Finished testing")

    if failed:
        print("************")
        print(color(" Failed tests: " + " ".join(failed), RED))
        print("************")

    if args.interactive:
        for t in failed:
            print("Press <q> to quit the tests")
            print("Press <r> to restart test '" + color(t, RED) + "' with output")
            print("(then press <q> to continue)")
            print("Press any other key to check the next failed test")
            key = input()
            if key == "r":
                out = run(
                    "yes | {} {} 2>&1 | less".format(
                        "./main" if args.lang == "c" else "python3 ./main.py -ascii",
                        TSTDIR / (t + ".test"),
                    ),
                    shell=True,
                )
                linecolor = ORANGE if out.returncode != 0 else GREEN
                print(color(f"-- Exited with status {out.returncode} --", linecolor))
            if key == "q":
                break


if __name__ == "__main__":
    main()
