import pika
"""
Sounds good, so the console is here http://18.214.12.198:35840/
12:12
user sixtysix pass sixtysix
12:12
exchange that you’d be interested in is denbc999-paper.dashboard
12:13
as in {user-ID}-{trading-mode}.dashboard
12:14
topic is updates

54.87.105.95
"""
connection = pika.BlockingConnection(
    pika.ConnectionParameters('18.214.12.198', 35840, '/', pika.PlainCredentials("sixtysix", "sixtysix")))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f'{body} is received')
    
channel.basic_consume(queue="updates", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
