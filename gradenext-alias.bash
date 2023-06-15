export PROJECTS=`pwd`
function gradenext {
    cd "$PROJECTS"/staged/ &&
    mv "`ls | head -1`" ../graded/ &&
    cd "`ls | head -1`" &&
    emacs -nw GRADING.txt
}
