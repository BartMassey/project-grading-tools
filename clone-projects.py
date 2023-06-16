# Clone projects for grading.
# Bart Massey 2022

import argparse, csv, re, subprocess, sys, zipfile
from pathlib import Path

parser = argparse.ArgumentParser(
    prog='clone-projects',
    description='Clone a student project repo for grading',
)
parser.add_argument("--overwrite-grading", action="store_true")
parser.add_argument("--both", action="store_true")
parser.add_argument("filename")
args = parser.parse_args()

project_archive = zipfile.ZipFile(args.filename)
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

def mkfdir(root):
    fdest = Path(root)
    if not fdest.is_dir():
        fdest.mkdir(mode=0o700)
    return fdest

sdest = mkfdir("staged")
gdest = mkfdir("graded")
if args.both:
    broot = Path("both")
    if not broot.is_dir():
        print("no 'both' symlink: giving up")
        exit(1)
    bdest = mkfdir(broot / "graded")
for user, link, slug, body in projects:
    spath = sdest / slug
    has_spath = spath.is_dir()
    gpath = gdest / slug
    has_gpath = gpath.is_dir()
    if args.both:
        bpath = bdest / slug
        has_bpath = bpath.is_dir()
    clone = False
    path = spath
    if has_gpath:
        path = gpath
    elif has_bpath:
        path = bpath
    elif not has_spath:
        clone = True
    if clone:
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
    
    grading = path / "GRADING.txt"
    if not grading.is_file() or args.overwrite_grading:
        with open(grading, "w") as gr:
            print("Project Name", file=gr)
            print("Member Names", file=gr)
            print(link, file=gr)
            print("-", file=gr)
            print(file=gr)
