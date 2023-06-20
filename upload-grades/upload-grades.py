import argparse, csv
from pathlib import Path
import canvasgrader

parser = argparse.ArgumentParser(
    prog='upload-grades',
    description='Upload project grades to Canvas',
)
parser.add_argument('--check', action='store_true')
parser.add_argument('--test', action='store_true')
parser.add_argument('--both', action='store_true')
parser.add_argument('--baseurl', default="canvas.pdx.edu")
parser.add_argument('courseid', nargs='?')
parser.add_argument('asgid', nargs='?')
args = parser.parse_args()

with open("students.csv", "r") as f:
    ids = csv.reader(f)
    index = { sname : sid for sname, sid in ids}

grades = dict()
comments = dict()
projects = list(Path("graded").iterdir())
if args.both:
    projects += list(Path("both").iterdir())
for project in projects:
    fgrading = project / "GRADING.txt"
    with fgrading.open() as f:
        grading = f.read()
    sgrading = grading.splitlines()
    assert sgrading[4] == "", f"bad GRADING: {fgrading}"
    title = sgrading[0]
    names = sgrading[1].split(", ")
    url = sgrading[2]
    score = int(sgrading[3])
    body = "\n".join(sgrading[5:]) + "\n"
    for n in names:
        if n not in index:
            print("missing student:", n, project)
            continue
        if args.check:
            continue
        sid = index[n]
        grades[sid] = score
        comments[sid] = body

if args.check:
    exit(0)

assert args.courseid and args.asgid, "need course and assignment ids"

grader = canvasgrader.CanvasGrader(
    args.baseurl,
    args.courseid,
)
if args.test:
    sid = list(grades.keys())[0]
    grades = {sid : grades[sid]}
    comments = {sid : comments[sid]}
    grader.grade_assignment(
        args.asgid,
        grades=grades,
        comments=comments,
    )
    exit(0)

grader.grade_assignment(
    args.asgid,
    grades=grades,
    comments=comments,
)
