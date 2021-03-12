#/bin/bash
if grep "Kafka Training host entries" /etc/hosts >/dev/null; then
  echo "Already done!"
  exit 0
fi

cat << EOF | sudo tee -a /etc/hosts >/dev/null

# Kafka Training host entries
127.0.0.1 kafka-1
127.0.0.1 kafka-2
127.0.0.1 kafka-3
127.0.0.1 zk-1
127.0.0.1 zk-2
127.0.0.1 zk-3

EOF
echo Done!