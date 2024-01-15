from kafka import KafkaConsumer
import json

# Specify the data type you want to focus on
desired_data_type = "minute"

# Kafka consumer configuration
consumer = KafkaConsumer(
    'telemetry_topic',
    bootstrap_servers=['192.168.68.108:9092'],
    auto_offset_reset='earliest'
)


# Function to print data in a readable format
def print_message(data_type, data):
    if data is not None:
        # Check if data is a list
        if isinstance(data, list):
            for item in data:
                print(f"Type: {data_type}, Timestamp: {item.get('timestamp', 'N/A')}, Data: {item}")
        else:
            # Assuming data is a dictionary if not a list
            print(f"Type: {data_type}, Timestamp: {data.get('timestamp', 'N/A')}, Data: {data}")
    else:
        print(f"Type: {data_type}, Data: None")


# Process and print messages from the topic
for message in consumer:
    try:
        message_data = json.loads(message.value)
        data_type = message_data.get("type")

        # Check if the message is of the desired type
        if data_type == desired_data_type:
            data_content = message_data.get("data")
            print_message(data_type, data_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
