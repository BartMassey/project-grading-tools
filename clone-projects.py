# Clone projects for grading.
# Bart Massey 2022

import csv, re, subprocess, yaml
from pathlib import Path

with open("projects.yaml", "r") as p:
    projects = yaml.safe_load(p)

f = open("failures.csv", "w")
failures = csv.writer(f)

dest = Path("staged")
if not dest.is_dir():
    dest.mkdir(mode=0o700)
for p in projects:
    members = [m["name"] for m in p["members"]]
    member_names = ", ".join(members)
    path = dest / p["slug"]
    if path.is_dir():
        continue
    print(f'clone {p["name"]}: ', end="")
    url = re.sub("^http(s)?://", "ssh://git@", p["repo"])
    if not re.match("ssh://git@", url):
        print("bad url: ", url)
        continue
    proc = subprocess.run(
        ["git", "clone", url, path],
        capture_output=True,
        encoding="utf-8",
    )
    if proc.returncode == 0:
        print("ok")
    else:
        print("failed")
        #people = [f'{m["name"]} <{m["email"]}>' for m in p["members"]]
        #failures.writerow([p["slug"], p["repo"], ','.join(people)])
        failures.writerow([p["slug"], p["repo"]])
        for l in proc.stderr.splitlines():
            if re.match("remote:.[A-Z]", l):
                print(l.strip())
        continue
    
    with open(path / "GRADING.txt", "w") as gr:
        print(p["name"], file=gr)
        print(member_names, file=gr)
        print("-", file=gr)
        print(file=gr)
