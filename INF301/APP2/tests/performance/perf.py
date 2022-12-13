#!/usr/bin/env python3
#
# Script de test de performances.
# A lancer depuis le repertoire de travail principal de l'APP ainsi:
#
# Pour la version C :
# ./tests/performance/perf.py c
#
# Pour la version python :
# ./tests/performance/perf.py c
#

import sys
import os
import subprocess
import json

from drawgraph import drawgraph

DEBUG=False
# DEBUG=True

def debug(*args):
    if (DEBUG):
        print("".join(args))

def help():
    print ("Usage: ", sys.argv[0], " c [t] (pour tester l'implementation C)")
    print ("    or ", sys.argv[0], " py [t] (pour tester l'implementation Python)")
    print ("    or ", sys.argv[0], " gen [t] (pour générer des fichiers de tests)")
    print ()
    print ("Où [t] peut être laissé vide ou être un parmi : base,long,nested,memfree,piiile")
    print ("")
    print ("ATTENTION : l'affichage dans vos programmes peut prendre beaucoup")
    print ("de temps. Désactivez vos affichages ('print') en commentant les")
    print ("lignes concernées, ou mieux en les mettant dans des blocs conditionnels:")

    print ("""
En python:
         if not curiosity.silent_mode:
             <mettre ici votre code d'affichage>

En C:
         if (! silent_mode) {
             <mettre ici votre code d'affichage>
         }
""")
    print ("")
    exit (1)


c_prog = 'main'
py_prog = 'main.py'

prog = None

if __name__ == "__main__":
    if len (sys.argv) == 1:
        help()

    gen = False

    if sys.argv[1] == "c":
        prog = c_prog
        options = " -silent "
    elif sys.argv[1] == "py":
        prog = py_prog
        options = " -ascii -silent "
    elif sys.argv[1] == "gen":
        gen = True
    else:
        print ("Erreur: mauvais argument", sys.argv[1])


if prog and not os.path.exists(prog):
    print ("Erreur: impossible de trouver le programme '" + prog + "'")
    print ("Ce scrit est a lancer depuis le répertoire principal de travail de l'APP ainsi:")
    print ("./tests/performance/perf.py <c ou py>")
    exit(1)


to_test = None

if len (sys.argv) > 2:
    to_test = sys.argv[2]

perfdir=os.path.dirname(sys.argv[0])

# genprog = "./" + perfdir + "/gen-test.py"
genprog = os.path.join(perfdir, "gen-test.py")


time = subprocess.check_output("which -a time | grep -v shell | tail -n 1", shell=True)
time = time.decode().rstrip()
# timecmd = " time -f '\tTemps: %es  Mémoire max: %MKb' "
timecmd = time + " -f '%e;%M' "
timeout = 60
# timeout = 10
timeoutcmd = "timeout " + str(timeout) + "s "

def run_test(mode, message):
    msg =  "Running tests mode " + mode + " " + message
    print ("*" * len(msg))
    print (msg)

    size_curves = []
    temps_curves = []
    memoire_curves = []
    size = 1000
    size_max = 10000000

    tmppipe=os.popen("mktemp --tmpdir -u $USER.XXXXXXXXX.fifo").read().strip()
    debug("Pipe is", tmppipe)
    os.system("mkfifo -m 600 " + tmppipe)

    ret = None
    while ret == None and size < size_max:
        print ("Size ", "{:10}".format(size))


        if gen :
            f = "> perfs/test" + mode + str(size) + ".test"
        else:
            f = " > " + tmppipe + " &"

        # os.system("mkfifo /tmp/fifo")
        generation = "python3 " + genprog + " -s " + str(size) + " -m " + mode + f
        result = os.system(generation)
        debug("Executed: " + generation + " with result " + str(result))

        if not gen:

            command = timecmd + timeoutcmd + './' + prog + options + " " + tmppipe + " >/dev/null"

            try:
                debug("Executing: ", command)
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                result = result.decode().rstrip()
                parts = result.split(';', 2)
                temps = parts[0]
                memoire = str(int(parts[1]) / (1024*1024))
                print ("\tTemps: {}s  Mémoire max: {:.2f} GB".format(temps, float(memoire)))

                size_curves.append(size)
                temps_curves.append(float(temps))
                memoire_curves.append(float(memoire))
            except subprocess.CalledProcessError as e:
                print ("Error, return code", e.returncode)
                if e.returncode == 139:
                    ret = "Segmentation Fault"
                elif e.returncode == 134:
                    ret = "Assertion Failed"
                elif e.returncode == 127:
                    ret = "Command not found"
                else:
                    ret = "Timeout after "+ str(timeout) +"seconds"

        size*=2

    os.remove(tmppipe)

    if ret != None:
        print ("Problem with last size:", ret)
    drawgraph(size_curves, temps_curves, memoire_curves, mode)

all_tests = {
    "base": "(très long sans blocs)",
    "long": "(très long, beaucoup de blocs)",
    "nested": "(très long, beaucoup de blocs imbriqués)",
    "memfree": "(boucle exécutée de nombreuses fois)",
    "piiile": "(très grande pile)",
    }


if __name__ == "__main__":
    if to_test:
        if not to_test in all_tests:
            print ("Type de test inconnu:", to_test)
            print ("Allowed tests:")
            print (json.dumps(all_tests,indent=4))
            exit (1)
        run_test (to_test, all_tests[to_test])
    else:
        for t in all_tests:
            run_test (t, all_tests[t])
