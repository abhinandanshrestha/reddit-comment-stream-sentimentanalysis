# Real time sentiment analysis of reddit comment stream data using Kafka

### Step1: Change directory to Kafka
cd Kafka/kafka_2.12-3.4.0/bin

### Step2: Start the zookeeper server
./windows/zookeeper-server-start.bat ../config/zookeeper.properties

### Step3: Start the Kafka Broker
./windows/kafka-server-start.bat ../config/server.properties

### Step 4: Ensure that topic is ready for the Kafka Producers to write messages to the topic.

./windows/kafka-topics.bat --list --bootstrap-server localhost:9092

### Step 5: Incase topic isn't present, create a new topic
./windows/kafka-topics.bat --create --topic soccer --bootstrap-server localhost:9092 

### Step 6: Ensure all the python packages are installed
pip install -r requirements.txt

### Step 7: Run Producer 
python producer.py

### Step 8: Run Consumer code (Plotly dash Application)
python plotly-consumer.py
