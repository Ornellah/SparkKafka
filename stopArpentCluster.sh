# delete topics
konsole --workdir "/opt/kafka" -e awk -F';' '{ system ("./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic=\"" $1 "\"") }' ~/Documents/Git\ project/SparkKafka/topics.txt

# kill all konsole
killall -9 konsole