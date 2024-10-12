# Clone projects for grading.
# Bart Massey 2022

import argparse, csv, re, subprocess, sys, zipfile
from pathlib import Path

parser = argparse.ArgumentParser(
    prog='clone-projects',
    description='Clone a student project repo for grading',
)
parser.add_argument(
    "--overwrite-grading",
    help="allow overwriting GRADING.txt files",
    action="store_true",
)
parser.add_argument(
    "--both",
    help="kludge for projects submitted to more than one course",
    action="store_true",
)
parser.add_argument(
    "--force-slugmap",
    help="overwrite existing slugmap when used with submissions file",
    action="store_true",
)
parser.add_argument(
    "--project-name",
    help="force the official project name rather than inferring it",
)
parser.add_argument(
    "filename",
    help="submission filename, normally submissions.zip",
    nargs="?",
)
args = parser.parse_args()

slugmap_file = Path("slugmap.csv")
slugmap = dict()
if args.filename:
    if slugmap_file.is_file():
        assert args.force_slugmap, "slugmap.csv exists"
    project_archive = zipfile.ZipFile(args.filename)
    projects = []
    for zipinfo in project_archive.infolist():
        user = re.sub(r"_.*$", r"", zipinfo.filename)
        body = str(project_archive.read(zipinfo))
        linkinfo = re.search(r'(https://git[^"/]*)/([^"/]+)/([^"/ <]+)(\.git)?', body)
        userline = re.search(r'<h1>.*: (.*)</h1>', body)
        username = userline[1]
        if linkinfo:
            linkage = [linkinfo[c] for c in [1, 2, 3]]
            _, _, slug = linkage
            if slug in slugmap:
                slug = slugmap[slug]
            link = '/'.join(linkage)
            projects.append((user, username, slug, link, body))
        else:
            print(f"{user}: could not find link in body")
    with open(slugmap_file, "w") as f:
        slugmap = csv.writer(f)
        for user, username, slug, link, body in projects:
            if args.project_name:
                slug = user
            slugmap.writerow([user, username, slug, slug, link])
    exit(0)

with open(slugmap_file) as f:
    for user, username, slug, name, link in csv.reader(f):
        slugmap[slug] = (user, username, link, slug, name)

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
for user, username, link, slug, name in slugmap.values():
    spath = sdest / slug
    has_spath = spath.is_dir()
    gpath = gdest / slug
    has_gpath = gpath.is_dir()
    has_bpath = False
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
        has_spath = True
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
            print()
            failures.writerow([slug, link, user])
            for l in proc.stderr.splitlines():
                if re.match("remote:.[A-Z]", l):
                    print(l.strip())
            print("failed", username)
            continue
    
    grading = path / "GRADING.txt"
    if not grading.is_file() or (args.overwrite_grading and has_spath):
        with open(grading, "w") as gr:
            if args.project_name:
                print(args.project_name, file=gr)
            else:
                print(name, file=gr)
            print(username, file=gr)
            print(link, file=gr)
            print("-", file=gr)
            print(file=gr)
