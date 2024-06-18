#!/usr/bin/python3

import csv

slugs = dict()

with open("slugmap-proposals.csv", "r") as f:
    for ident, student, slug, name, url in csv.reader(f):
        slugs[ident] = [student, slug, name]

with open("slugmap-projects.csv", "r") as f:
    for ident, student, slug, name, url in csv.reader(f):
        slugs[ident].append(url)

with open("slugmap.csv", "w") as f:
    w = csv.writer(f)
    for ident in slugs:
        fields = slugs[ident]
        w.writerow([ident] + fields)

