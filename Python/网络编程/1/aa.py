import argparse

parse = argparse.ArgumentParser(description=" ooo ? hahahaha")
# parse.add_argument("qwe", help="qwe can echo string you input", type=int)
parse.add_argument(
    "-v", "--verbosity", help="increase output verbosity", action="store_true")
args = parse.parse_args()
if args.verbosity:
    print("verbosity turn on")
