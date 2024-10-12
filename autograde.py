#!/usr/bin/python3
# Generate initial portfolio grade
# Bart Massey 2024

import os, re, sys
from pathlib import Path

def name_re(name, short=False):
    if short:
        if re.search(r"\.", name) is None:
            return None
        name = "^" + re.sub(r"\..*$", "", name)
    else:
        name = re.sub(r"\.", r"\\.", name)
    return re.compile(name, flags=re.I)

portfnames = (
    ("README.md", False),
    ("notebook.md", False),
    ("code", True),
)
portfiles = tuple((name, name_re(name), name_re(name, short=True), is_dir)
                  for name, is_dir in portfnames)

def file_info(fi):
    name, name_re, short_name_re, is_dir = fi
    entry = None
    short = False
    for p in Path().iterdir():
        if name_re.fullmatch(str(p)) is not None:
            entry = p
            break
        if short_name_re is not None and short_name_re.match(str(p)) is not None:
            short = True
            entry = p
            break

    if entry is None:
        if is_dir:
            return (None, 0, [])
        return (None, 20, [f"The {name} file seems to be missing."])

    deduction = 0
    failings = []
    if short:
        deduction += 5
        failings.append(
            f"Please name {name} exactly as shown (same prefix and case)."
        )
    elif str(name) != str(entry):
        deduction += 5
        failings.append(f"Please rename {entry} to {name} (match the case).")

    if not is_dir:
        lines = 0
        with entry.open() as f:
            for _ in f:
                lines += 1
        if lines < 5:
            deduction += 5
            failings.append(f"{entry} currently looks pretty empty.")

    return (entry, deduction, failings)

def grade_portfolio(author):
    points = 100
    messages = []
    for p in portfiles:
        name, deduction, pmessages = file_info(p)
        messages += pmessages
        points -= deduction

    grading = Path("GRADING.txt")
    with grading.open() as f:
        project, fullname, url = list(f)[:3]
    grading_bak = grading.rename("GRADING.txt.bak")

    doc = [
        project.strip(),
        fullname.strip(),
        url.strip(),
        str(points),
        "",
        "These notes were produced by an automatic grading program.",
        "If there is a problem, please contact me on Zulip.",
        "",
    ]
    if points == 100:
        doc.append("Everything looks fine. Good job.")
    else:
        doc.append("Here's issues we found:")
        doc.append("")
        for m in messages:
            doc.append(f"* {m}")
        doc.append("")
        doc.append("The score isn't important here, but please do try to fix these.")

    with grading.open(mode="w") as f:
        for line in doc:
            print(line, file=f)
    grading_bak.unlink()

staged = Path("staged")
graded = Path("graded")
for path in (staged, graded):
    if not path.is_dir():
        print(f"missing {path}", file=sys.stderr)
        exit(1)
basedir = os.getcwd()

targets = [p for p in staged.iterdir()]
for p in targets:
    os.chdir(p)
    grade_portfolio(str(p.name))
    os.chdir(basedir)
    p.rename(graded / p.name)
