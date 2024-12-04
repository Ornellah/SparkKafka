# delete topics
konsole --workdir "/opt/kafka" -e awk -F';' '{ system ("./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic=\"" $1 "\"") }' ~/Documents/Git\ project/SparkKafka/topics.txt

# kill kafka server
konsole --workdir "/opt/kafka" -e "bash ./bin/kafka-server-stop.sh"

# kill zookeeper server
konsole --workdir "/opt/kafka" -e "bash ./bin/zookeeper-server-stop.sh"


# kill all konsole
# killall -9 konsole