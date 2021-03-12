# Docker Local Environment

## Prerequisities

In order to run this environment, you'll need Docker installed and Kafka's CLI tools.

1. This was tested using [Docker Desktop](https://www.docker.com/products/docker-desktop) for macOS Engine version 20.10.2.

2. The CLI tools can be downloaded [here](https://www.confluent.io/download/) as a `tar` or `zip`. After the download is complete and the files extracted, you'll need to add it to your `PATH` environment variable.

    If using `bash`, edit the *bash_profile* file available at `~/.bash_profile` and add the following: `PATH=$PATH:~/bin/confluent-6.0.1/bin` (Assuming that the files were extracted to the `~/bin` location. Any other location will work as long as the path of the `PATH` environment is targeting the right path).

    If using `zshell`, you'll need to edit `~/.zshrc` instead.

3. Update local `hosts` file.

Execute the `update-hosts.sh` script to update your local `/etc/hosts` file to resolve the name of the containers.

```shell
bash update-hosts.sh
```

## Docker Image

It was decided to use the [Bitnami](https://bitnami.com/stack/kafka/containers) images for its ready-to-use approach, well-known reliability, and it's a [non-root container](https://docs.bitnami.com/tutorials/work-with-non-root-containers/).

**References**:

- [Bitnami Zookeeper documentation](https://github.com/bitnami/bitnami-docker-zookeeper)
- [Bitnami Kafka documentation](https://github.com/bitnami/bitnami-docker-kafka)

## Docker Compose

A [docker-compose file](https://docs.docker.com/compose/compose-file/) is provided [here](./build/docker-compose.yml) to spin ZooKeeper in [replicated mode](https://zookeeper.apache.org/doc/current/zookeeperStarted.html#sc_RunningReplicatedZooKeeper) and a 3 node [Kafka Broker cluster](https://kafka.apache.org/081/documentation.html#introduction).

To spin up:

```bash
docker-compose -f ./build/docker-compose.yml build
```

### Zookeeper Configuration

The containers only expose the `client port` accordingly to the container:

- container 1: 12181/TCP
- container 2: 22181/TCP
- container 3: 32181/TCP

#### Zookeeper Environment Variables

- `ALLOW_ANONYMOUS_LOGIN` - Allow to accept connections from unauthenticated users.
- `ZOO_SERVER_ID` - ID of the server in the ensemble.
- `ZOO_SERVERS` - Comma, space, or semi-colon separated list of servers.
- `ZOO_PORT_NUMBER` - ZooKeeper client port
- `ZOO_TICK_TIME`: Basic time unit in milliseconds used by ZooKeeper for heartbeats.
- `ZOO_INIT_LIMIT`: ZooKeeper uses to limit the length of time the ZooKeeper servers in quorum have to connect to a leader.
- `ZOO_SYNC_LIMIT`: How far out of date a server can be from a leader.
- `ZOO_AUTOPURGE_PURGEINTERVAL`: the time interval in hours for which the purge task has to be triggered.
- `ZOO_AUTOPURGE_SNAPRETAINCOUNT`: number of most recent snapshots and the corresponding transaction logs in the dataDir and dataLogDir to keep.
- `ZOO_MAX_CLIENT_CNXNS`: Limits the number of concurrent connections that a single client may make to a single member of the ZooKeeper ensemble.
- `ZOO_HEAP_SIZE`: Size in MB for the Java Heap options (Xmx and XMs).

### Kafka Configuration

The containers only expose the following ports:

- `INTERNAL` 9092 - for intra-cluster communication
- `EXTERNAL` - for connection from local computer
  - kafka-1: 19093
  - kafka-2: 29093
  - kafka-3: 39093

#### Kafka Broker Environment Variables

- `KAFKA_CFG_ZOOKEEPER_CONNECT`: Comma separated host:port pairs, each corresponding to a Zookeeper Server.
- `ALLOW_PLAINTEXT_LISTENER`: Allow to use the PLAINTEXT listener.
- `KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP`: Map between listener names and security protocols.
- `KAFKA_CFG_LISTENERS`: Comma-separated list of URIs we will listen on and the listener names.
- `KAFKA_CFG_ADVERTISED_LISTENERS`: Listeners to publish to ZooKeeper for clients to use, if different than the listeners config property.
- `KAFKA_INTER_BROKER_LISTENER_NAME`: Name of listener used for communication between brokers.
- `KAFKA_CFG_NUM_PARTITIONS`: The default number of log partitions per topic
- `KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE`: Allow automatic topic creation on the broker when subscribing to or assigning a topic.
- `KAFKA_CFG_DEFAULT_REPLICATION_FACTOR`: default replication factors for automatically created topics
- `KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR`: The replication factor for the offsets topic
- `KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR`: The replication factor for the transaction topic
- `KAFKA_HEAP_OPTS`: Kafka's Java Heap size.
- `KAFKA_CFG_BROKER_ID`: Kafka's broker custom id.

#### Validate Environment

- Confirm that the containers are up and running:

`docker-compose -f build/docker-compose.yml ps`

it should return similar information:

```bash
      Name                    Command               State                                Ports                              
----------------------------------------------------------------------------------------------------------------------------
build_kafka-ui_1   /kafdrop.sh                      Up      0.0.0.0:8080->8080/tcp                                          
kafka-1            /opt/bitnami/scripts/kafka ...   Up      0.0.0.0:19093->19093/tcp, 9092/tcp                              
kafka-2            /opt/bitnami/scripts/kafka ...   Up      0.0.0.0:29093->29093/tcp, 9092/tcp                              
kafka-3            /opt/bitnami/scripts/kafka ...   Up      0.0.0.0:39093->39093/tcp, 9092/tcp                              
zk-1               /opt/bitnami/scripts/zooke ...   Up      0.0.0.0:12181->12181/tcp, 2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp
zk-2               /opt/bitnami/scripts/zooke ...   Up      2181/tcp, 0.0.0.0:22181->22181/tcp, 2888/tcp, 3888/tcp, 8080/tcp
zk-3               /opt/bitnami/scripts/zooke ...   Up      2181/tcp, 2888/tcp, 0.0.0.0:32181->32181/tcp, 3888/tcp, 8080/tcp
```

- Certify that communication can be established with the `Zookeeper`:

`zookeeper-shell zk-1:12181 get /zookeeper/config`

it should return similar information:

```bash
Connecting to zk-1:12181

WATCHER::

WatchedEvent state:SyncConnected type:None path:null
server.1=0.0.0.0:2888:3888:participant;0.0.0.0:12181
server.2=zookeeper2:2888:3888:participant;0.0.0.0:12181
server.3=zookeeper3:2888:3888:participant;0.0.0.0:12181
version=0
```

- List the `Kafka Brokers` registered with `Zookeeper` executing:

`zookeeper-shell zk-1:12181 ls /brokers/ids`

it should return similar information:

```bash
Connecting to zk-1:12181

WATCHER::

WatchedEvent state:SyncConnected type:None path:null
[1001, 1002, 1003]
```

## Kafdrop

[Kafdrop](https://github.com/obsidiandynamics/kafdrop) is a web UI for viewing Kafka topics and browsing consumer groups. The tool displays information such as brokers, topics, partitions, consumers, and lets you view messages.

To use Kafdrop we must access [http://localhost:8080](http://localhost:8080). This application is a graphical representation of:

1. View brokers, all topics and settings
2. View all data on topics
3. View messages sent
4. View consumer groups
5. Create topics (with few configurations)
