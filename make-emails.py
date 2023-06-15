import yaml

with open("projects.yaml", "r") as p:
    projects = yaml.safe_load(p)

index = { p["slug"] : p for p in projects }

fails = open("failures.csv", "r")
for f in fails:
    slug = f.strip()
    p = index[slug]
    people = [f'{m["name"]} <{m["email"]}>' for m in p["members"]]
    print(', '.join(people))
    print('Rust project inaccessible')
    print('Greetings! We tried to clone your Rust project repo at')
    print(p["repo"])
    print('so that we could grade it.')
    print('Unfortunately, the repo is inaccessible to us right now.')
    print('Please add me (BartMassey) as a Maintainer to your repo')
    print('or make the repo public. The sooner you do this, the sooner')
    print('we can grade your work.')
    print()
    print('Thanks much!')
    print()
    print()
