import argparse, sys, zipfile
from pathlib import Path
from zipfile import Path as ZipPath

parser = argparse.ArgumentParser(
    prog='get-gradefiles',
    description='Zip up project grade files for distribution',
)
parser.add_argument("--both", action="store_true")
args = parser.parse_args()

def get_gradefiles(path):
    grpath = path / "graded"
    return [(p.name, p / "GRADING.txt") for p in grpath.iterdir()]

grades = get_gradefiles(Path("."))
if args.both:
    grades += get_gradefiles(Path("both"))

with zipfile.ZipFile("gradefiles.zip", mode='w') as z:
    gradefiles_dir = "gradefiles"
    z.mkdir(gradefiles_dir)

    for name, path in grades:
        gradename = Path(gradefiles_dir) / (name + "-GRADING.txt")
        z.write(path, arcname=gradename)
