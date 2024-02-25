* https://canvas.pdx.edu/profile/settings to generate Canvas
  API token
* Store Canvas API token in ~/.canvastoken
* Clone my fork http://github.com/BartMassey-upstream/canvasgrader (for now)
  and run `pip install .`
* Working in the project grading directory:
    * Go to https://canvas.pdx.edu/<course-id>/students
      and copy-paste the JSON found there into `students.json`
      (gross, will fix later)
    * Run `student-ids.py` to create `students.csv`
    * Run `upload-grades.py --check [--both]`.
    * Edit student names in either `students.csv` or their
      `GRADING.txt` until all students are matched with an
      ID in `students.csv`. Output of `--check` should be
      nothing.
    * Find course ID in course URL
    * Find assignment ID in assignment URL
    * Run `upload-grades.py [--both] <courseid> <asgid>`
