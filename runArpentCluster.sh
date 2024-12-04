# run zookeeper
konsole --workdir "/opt/kafka" -e "bash ./bin/zookeeper-server-start.sh config/zookeeper.properties" &

sleep 10
# run kafka server
konsole --workdir "/opt/kafka" -e "bash ./bin/kafka-server-start.sh config/server.properties" &

sleep 20
# create kafka topics
konsole --workdir "/opt/kafka" -e awk -F';' '{ system("./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic=\"" $1 "\" --partitions=\"" $2 "\" --replication-factor=\"" $3 "\"") }' ~/Documents/Git\ project/SparkKafka/topics.txt