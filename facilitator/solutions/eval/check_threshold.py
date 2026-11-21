import json
import sys


def main(report_path, threshold):
    s = json.load(open(report_path))["summary"]["overall_code"]
    ok = s is not None and s >= threshold
    print(f"{'PASS' if ok else 'FAIL'}: overall_code={s} threshold={threshold}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], float(sys.argv[2])))
