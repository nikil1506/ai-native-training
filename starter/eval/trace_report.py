"""L11 task 2: summarise traces into report.md: success rate, typical (median) and slowest time, tokens and cost per task,
and the TOP THREE COSTS. python starter/eval/trace_report.py starter/eval/traces/*.jsonl"""
import json
import sys


def load(paths):
    return [[json.loads(l) for l in open(p, encoding="utf-8")] for p in paths]


def main(paths):
    traces = load(paths)
    # TODO 2: per trace (= one task): total tokens, total seconds, estimated cost (see starter/common.py PRICES), success flag.
    # Then print: success rate, median and slowest seconds, tokens/cost per task, and the 3 most expensive steps (by name).
    raise NotImplementedError("TODO 2")


if __name__ == "__main__":
    main(sys.argv[1:])
