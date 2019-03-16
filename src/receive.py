import pika, configparser, json
from FHIR.utilities import Utilities;

config = configparser.ConfigParser();
config.read('config/config.ini');
connection = pika.BlockingConnection(pika.ConnectionParameters(config['MESSAGE_QUEUE']['HOST']));
channel = connection.channel();
channel.basic_qos(0, 1);
channel.queue_declare(queue=config['MESSAGE_QUEUE']['NAME'], durable=True);

def callback(channel, method, properties, body):

    body = body.decode("utf-8");
    jsonBody = json.loads(body);

    if ( Utilities.createFHIRResource(jsonBody['resource'], body) == 200 ):
        channel.basic_ack(method.delivery_tag)

channel.basic_consume(callback, queue=config['MESSAGE_QUEUE']['NAME']);

if __name__ == '__main__':
    channel.start_consuming()
