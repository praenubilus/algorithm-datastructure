
javac -d out -cp .:./../../../_commons/java/junit-jupiter-api.jar:./../../../_commons/java/apiguardian-api.jar BubbleSortTest.java

java -jar junit-platform-console-standalone.jar  -cp .:./out --scan-classpath
