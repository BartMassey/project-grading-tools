# Synopsize graded projects as YAML.
# Bart Massey 2022

import sys, yaml
from pathlib import Path


# https://github.com/yaml/pyyaml/issues/240#issuecomment-1018712495
# https://til.simonwillison.net/python/style-yaml-dump
# Yeesh.
def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data"""
    if data.find('\n') >= 0:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(str, str_presenter)
# to use with safe_dump
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

graded = Path("graded")
synopses = dict()
for slug in graded.iterdir():
    if not slug.is_dir():
        continue
    with open(slug / "GRADING.txt", "r") as graded:
        name = next(graded).strip()
        authors = next(graded).strip()
        grade = next(graded).strip()
        try:
            grade = int(grade)
        except:
            print(f"{slug}: could not read grade", file=sys.stderr)
            continue
        next(graded)
        comments = '\n'.join([line.strip() for line in graded])
        gradeinfo = {
            "name" : name,
            "authors" : authors,
            "grade" : grade,
            "comments" : comments,
        }
        synopses[slug.name] = gradeinfo

with open("synopses.yaml", "w") as s:
    # https://stackoverflow.com/a/10656291/364875
    # Yeesh. (Srsly? `encoding="utf-8"` does not imply allowing Unicode?)
    yaml.safe_dump(synopses, s, encoding="utf-8", allow_unicode=True, default_flow_style=False)
