# Clone projects for grading.
# Bart Massey 2022

import csv, re, subprocess, sys, zipfile
from pathlib import Path

project_archive = zipfile.ZipFile(sys.argv[1])
projects = []
for zipinfo in project_archive.infolist():
    user = re.sub(r"_.*$", r"", zipinfo.filename)
    body = str(project_archive.read(zipinfo))
    linkinfo = re.search(r'href="(https://git[^"/]*)/([^"/]+)/([^"/]+)(/[^"]*)?"', body)
    if linkinfo:
        linkage = [linkinfo[c] for c in [1, 2, 3]]
        _, _, slug = linkage
        link = '/'.join(linkage)
        projects.append((user, link, slug, body))
    else:
        print("{user}: could not find link in body")
        print(body)

f = open("failures.csv", "w")
failures = csv.writer(f)

dest = Path("staged")
if not dest.is_dir():
    dest.mkdir(mode=0o700)
for user, link, slug, body in projects:
    path = dest / slug
    if path.is_dir():
        continue
    print(f'clone {link}: ', end="", flush=True)
    url = re.sub(r"^http(s)?://", r"ssh://git@", link)
    if not re.match(r"ssh://git@", url):
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
        print()
        failures.writerow([slug, link, user])
        for l in proc.stderr.splitlines():
            if re.match("remote:.[A-Z]", l):
                print(l.strip())
        print()
        print(body)
        continue
    
    with open(path / "GRADING.txt", "w") as gr:
        print("Project Name", file=gr)
        print("Member Names", file=gr)
        print("-", file=gr)
        print(file=gr)
