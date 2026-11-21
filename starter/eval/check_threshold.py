"""L10 task 5: fail (exit 1) if a report's score is below a threshold.
    python starter/eval/check_threshold.py starter/eval/reports/after.json 0.7"""
import json
import sys


def main(report_path, threshold):
    # TODO: load the report, read summary["overall_code"], print PASS/FAIL, and return the right exit code.
    # Prove it works: it must FAIL on a deliberately worse agent version.
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], float(sys.argv[2])))
