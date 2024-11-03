# run zookeeper
konsole --workdir "/opt/kafka" -e "bash ./bin/zookeeper-server-start.sh config/zookeeper.properties" &

sleep 10
# run kafka server
konsole --workdir "/opt/kafka" -e "bash ./bin/kafka-server-start.sh config/server.properties" &

sleep 20
# create kafka topic
konsole --workdir "/opt/kafka" -e "bash ./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic arpent-resultats-diplomes --partitions 1 --replication-factor 1"