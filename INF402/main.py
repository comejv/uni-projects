from argparse import ArgumentParser
from genericpath import isfile
from classes import CNF, IDPool
from sat import cnf_to_3sat
import solver
import rules


# Parse arguments
parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="path to the input file")
parser.add_argument("-d", "--dimacs", dest="dimacs",
                    help="path to the already generated DIMACS file")
parser.add_argument("-c", "--cnf", dest="cnf",
                    help="path to the file where the CNF will be written")
parser.add_argument("-p", "--pysat", dest="pysat", action="store_true", default=False,
                    help="use PySAT instead of our own WalkSAT")
parser.add_argument("-t", "--sat3", dest="sat3", action="store_true", default=False,
                    help="convert CNF to 3 sat before using")
parser.add_argument("-w", "--write_file", dest="write_file", default="stdout",
                    help="Write the graphical solution to the given file")
parser.add_argument("--branching", dest="branching",
                    help="what branching heuristic walksat should use. jw or moms. \
                        If none provided, always chooses the same variable.")
parser.add_argument("--use-c-walk", dest="c_walk", action="store_true", default=False,
                    help="use the C implementation of our Walksat")
parser.add_argument("-q", "--quiet", dest="quiet", action="store_true",
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

# -i and -d are mutually exclusive
if args.input and args.dimacs:
    parser.error("You can only specify one input method.")

# ## Handle input ## #
if args.input:
    assert isfile(args.input)
    # Check file extension
    if args.input.endswith(".txt"):
        nodes = solver.create_nodes_from_text(args.input)
    elif args.input.endswith(".jpg") or args.input.endswith(".png"):
        nodes = solver.create_nodes_from_image(args.input)
    else:
        print("Invalid file extension.")
        exit(1)

elif args.dimacs:
    assert isfile(args.dimacs)
    cnf = solver.read_dimacs(args.dimacs)
    solution = solver.solve_cnf(
        cnf, pysat=args.pysat, quiet=args.quiet, jw=args.jw_walk)
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
    else:
        print("Invalid file extension.")
        raise SystemExit

# Create IDPool and cnf
vpool_bridges = IDPool()
cnf = CNF()

# Create every possible bridge
bridges = solver.all_bridges(nodes)

# ## Apply rules ## #

# Nodes must have {node.value} bridges exactly
for node in nodes:
    cnf.extend(solver.bridges_to_clauses(
        vpool_bridges, rules.connect_node(node)))

# Bridges can't cross each other
cnf.extend(solver.bridges_to_clauses(
    vpool_bridges, rules.no_crossing(bridges)))

# ## Connexity Rule ## #

# Create new IDPool
vpool = solver.IDPool(cnf.nvars() + 1)

# Connexity rule apply
cnf.extend(solver.arcs_ways_to_clauses(
    vpool, vpool_bridges, rules.connexite(nodes)))

# Convert to 3-SAT if asked
if args.sat3:
    cnf = cnf_to_3sat(cnf)

# ## Solve ## #
if args.cnf:
    cnf.to_file(args.cnf)
model = solver.solve_cnf(cnf, pysat=args.pysat,
                         quiet=args.quiet, heuristic=args.branching, c_walk=args.c_walk)

if model is not None:
    bridges = solver.cnf_to_bridges(
        vpool_bridges, model[:(vpool_bridges.next_id)-1])

    solver.pretty_print_model(nodes=nodes,
                              bridges=bridges,
                              fpath=args.write_file)

    if not args.quiet:
        print(f"Game is {'un' if model is None else ''}satisfiable.")
        print("One model is :")
        print("Variables :", model)
        print("Bridges :", bridges)

    exit(0)
else:
    exit(1)
