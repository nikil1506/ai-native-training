import subprocess, sys
for t in ("t201", "t202", "t203"):
    r = subprocess.run([sys.executable, "-m", "unittest", f"capstone_tests.test_{t}"], capture_output=True)
    print(t, "FIXED" if r.returncode == 0 else "open")
