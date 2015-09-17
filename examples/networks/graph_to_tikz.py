# coding: utf-8
import json
import argparse


def parse_graph(json_file, out_file):

    with open(json_file, "r") as f:
        graph = json.load(f)

    visited = set()

    with open(out_file, "w") as f:
        f.write("\graph [spring electrical layout',"
                "nodes={circle, draw, minimum width=2.2em},"
                "node distance=3.5em] {\n")
        for e in graph["edges"]:
            if (e["to"], e["from"]) not in visited:
                f.write("{0} -- {1};\n".format(e["from"], e["to"]))
                visited.add((e["from"], e["to"]))
        f.write("};\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", help="JSON graph file")
    parser.add_argument("out_file", help="File to save resulting TikZ code")
    args = parser.parse_args()

    parse_graph(args.graph, args.out_file)
