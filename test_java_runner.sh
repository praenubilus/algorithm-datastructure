if [ $# -ne 1 ];then
	echo 'incorrect arguments. Should be test_java_runner.sh <target_folder_path>'
	exit 1
fi

if [ ! -d "$1" ]; then
	echo 'Incorrect target directory. Not existing or cannot find.'
  exit 1
fi

if [ ! -d "$1/java" ]; then
	echo 'Incorrect target directory. The "java" subdirectory does not exist.'
  exit 1
fi

## using the relative program/module path as input
target="$1"
origin_dir=$(pwd)

## change dir to target program/project folder
cd "${target}/java"

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
    if [ -e "$f" ] && [ "$f" != "./Testable.java" ]; then
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

## change directory back to original folder
cd "${origin_dir}"