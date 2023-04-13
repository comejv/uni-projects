from argparse import ArgumentParser
from genericpath import isfile
import solver
import rules


# Parse arguments
parser = ArgumentParser()
parser.add_argument("-i", "--image", dest="image",
                    help="path to the image file")
parser.add_argument("-t", "--text", dest="text", help="path to the text file")
parser.add_argument("-d", "--dimacs", dest="dimacs",
                    help="path to the already generated DIMACS file")
parser.add_argument("-c", "--cnf", dest="cnf",
                    help="path to the file where the CNF will be written")
parser.add_argument("-q", "--quiet", dest="quiet",
                    help="do not print the solution")
parser.add_argument("-b", "--bridge-help", dest="bridge_help", action="store_true",
                    help="show how the bridges are numbered")
args = parser.parse_args()

if args.bridge_help:
    print("The first number of a bridge id is its level.\n" +
          "Then comes the node it connects from and to, represented by their number " +
          "(left to right and top to bottom).\n" +
          "Positive means the bridge is used, negative it isn't.")
    exit(0)

# -i, -t and -d are mutually exclusive
if sum([args.image is not None, args.text is not None, args.dimacs is not None]) > 1:
    parser.error("The arguments -i, -t and -d are mutually exclusive")

# ## Handle input ## #
if args.image:
    assert isfile(args.image)
    nodes = solver.create_nodes_from_image(args.image)
elif args.text:
    assert isfile(args.text)
    nodes = solver.create_nodes_from_text(args.text)
elif args.dimacs:
    assert isfile(args.dimacs)
    cnf = solver.read_dimacs(args.dimacs)
    solution = solver.solve_cnf(cnf)
    solver.write_solution_to_text(solution, args.output)
    if not args.quiet:
        print(solution)
        exit()
else:
    fpath = input("Enter the path to the input file:\n")
    # Check file extension
    if fpath.endswith(".txt"):
        nodes = solver.create_nodes_from_text(fpath)
    elif fpath.endswith(".jpg") or fpath.endswith(".png"):
        nodes = solver.create_nodes_from_image(fpath)

# Create IDPool and cnf
vpool = solver.IDPool()
cnf = solver.CNF()

# Create every possible bridge
bridges = solver.all_bridges(nodes)

# ## Apply rules ## #

# Nodes must have {node.value} bridges exactly
for node in nodes:
    dnf = solver.bridges_to_clauses(vpool, rules.connect_node(node))
    cnf.extend(dnf)

# Bridges can't cross each other
cnf.extend(solver.bridges_to_clauses(vpool, rules.no_crossing(bridges)))

# ## Solve ## #
if args.cnf:
    solver.write_dimacs(args.cnf, cnf)
satsolve = solver.solve_cnf(cnf, vpool, quiet=args.quiet)
solvable = satsolve.solve()

if not args.quiet:
    print(f"Game is {'un' if not solvable else ''}atisfiable.")
    if solvable:
        print("One model is :")
        print("Variables :", satsolve.get_model())
        print("Bridges :", solver.cnf_to_bridges(vpool, satsolve.get_model()))
