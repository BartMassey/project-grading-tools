#!/usr/bin/python3
import os, sys
from pathlib import Path

wd = Path(os.environ["PROJECT_DIR"])
gf = wd / "project-grading-order"
cmd = sys.argv[1]
with open(gf, "r") as f:
    projects = f.read().splitlines()
if cmd == "start":
    print("cd", projects[0])
elif cmd == "finish":
    print("cd ..")
    print("mv", projects[0], "../graded/")
    with open(gf, "w") as f:
        print('\n'.join(projects[1:]), file=f)
else:
    print("bad command", cmd, file=sys.stderr)
    exit(1)
