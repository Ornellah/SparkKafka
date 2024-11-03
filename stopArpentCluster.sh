# delete topic
konsole --workdir "/opt/kafka" -e "bash ./bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic arpent-resultats-diplomes"

# kill all konsole
killall -9 konsole