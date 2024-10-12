# Project Grading Tools
Bart Massey 2023

These tools are intended for a Canvas homework archive where
the homework consists of a text submission of a git repo
URL. The main use case is as follows:

1. Export `submissions.zip` from Canvas

2. Run `python3 clone-projects.py submissions.zip` with
   flags as needed to generate a `slugmap.csv`.

3. Edit `slugmap.csv` as needed to adapt to whatever the
   students did.

4. Use `ssh-add` to add keys to repository sites mentioned
   in the submissions, as needed.

5. Run `python3 clone-projects.py` (*without*
   `submissions.zip`) to clone projects into a `staged/`
   grading staging directory.

6. Edit each `GRADING.txt` file in the staging directory to
   grade, moving each project directory into `graded/`.

7. Use the code in `upload-grades/` to complete the grading
   process.

You can rerun `clone-projects.py` as needed: by default it
will not try to re-clone already-successfully-cloned
projects, nor re-create already-created grading directories
and files.

Various scripts for things are also here, and should be
documented.
