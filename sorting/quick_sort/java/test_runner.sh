if [ -d "out" ]; then
  rm -rf out
fi
mkdir out

for f in ./*Test.java; do
    ## Check if the glob gets expanded to existing files.
    ## If not, f here will be exactly the pattern above
    ## and the exists test will evaluate to false.
    if [ -e "$f" ]; then
        src_file="$f"
    fi
    ## This is all we needed to know, so we can break after the first iteration
    break
done

for f in ./Test*.java; do
    ## Check if the glob gets expanded to existing files.
    ## If not, f here will be exactly the pattern above
    ## and the exists test will evaluate to false.
    if [ -e "$f" ] &&  [ "$f" != "./Testable.java" ]; then
        src_file="$f"
    fi
    ## This is all we needed to know, so we can break after the first iteration
    break
done

# compile the unit tests
javac -d out -cp .:./../../../_commons/java/junit-jupiter-api.jar:./../../../_commons/java/apiguardian-api.jar "${src_file}"
# launch the unit tests through junit console launcher with test discovery in classpath
java -jar ./../../../_commons/java/junit-platform-console-standalone.jar -cp .:./out --scan-classpath --details=tree

if [ -d "out" ]; then
  rm -rf out
fi 
