import pika
import logging
from consumers import compress_and_crop, extract_subs_into_ass, \
      convert_video_format, crop_video, merge_vids, burn_subs_into_video, add_color_filters


if __name__ == "__main__":
    logging.basicConfig(filename="application.log", encoding='utf-8', level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
    logging.info("HELLO")
    creds = pika.PlainCredentials(
        'guest',
        'guest'
    )
    params = pika.ConnectionParameters(
        host='192.168.0.108',
        port=5672,
        virtual_host='videos',
        credentials=creds
    )

    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='task_exchange', exchange_type='direct')

    channel.queue_declare(queue='compress_and_crop')
    channel.queue_declare(queue='extract_subs')
    channel.queue_declare(queue='convert')
    channel.queue_declare(queue='crop_video')
    channel.queue_declare(queue='merge_vids')
    channel.queue_declare(queue='burn_subs')
    channel.queue_declare(queue='add_color_filters')
    channel.queue_declare(queue='change_video_and_audio_speed')
    channel.queue_declare(queue='mute_video')

    channel.queue_bind(exchange='task_exchange', queue='compress_and_crop', routing_key='compress_and_crop')
    channel.queue_bind(exchange='task_exchange', queue='extract_subs', routing_key='extract_subs')
    channel.queue_bind(exchange='task_exchange', queue='convert', routing_key='convert')
    channel.queue_bind(exchange='task_exchange', queue='crop_video', routing_key='crop_video')
    channel.queue_bind(exchange='task_exchange', queue='merge_vids', routing_key='merge_vids')
    channel.queue_bind(exchange='task_exchange', queue='burn_subs', routing_key='burn_subs')
    channel.queue_bind(exchange='task_exchange', queue='add_color_filters', routing_key='add_color_filters')
    channel.queue_bind(exchange='task_exchange', queue='change_video_and_audio_speed', routing_key='change_video_and_audio_speed')
    channel.queue_bind(exchange='task_exchange', queue='mute_video', routing_key='mute_video')
    logging.info("Queues and bindings created successfully.")

    channel.basic_consume(queue='compress_and_crop', on_message_callback=compress_and_crop, auto_ack=True)
    channel.basic_consume(queue='extract_subs', on_message_callback=extract_subs_into_ass, auto_ack=True)
    channel.basic_consume(queue="convert", on_message_callback=convert_video_format, auto_ack=True)
    channel.basic_consume(queue="crop_video", on_message_callback=crop_video, auto_ack=True)
    channel.basic_consume(queue="merge_vids", on_message_callback=merge_vids, auto_ack=True)
    channel.basic_consume(queue="burn_subs", on_message_callback=burn_subs_into_video, auto_ack=True)
    channel.basic_consume(queue="add_color_filters", on_message_callback=add_color_filters, auto_ack=True)
    logging.info("Going to start consuming messages...")
    channel.start_consuming()

    connection.close()