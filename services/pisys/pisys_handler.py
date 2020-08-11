import datetime
import decimal
import logging

import boto3
from aws_xray_sdk.core import patch_all

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

patch_all()

dynamodb = boto3.resource('dynamodb')


def save_message_handler(event, context):
    pisys_monitoring = dynamodb.Table('iot-gg-example-pisys-monitoring')

    logger.info('Receive event: event=%s', event)

    if event['timestamp'] is None:
        timestamp = datetime.datetime.utcnow()
    else:
        timestamp = datetime.datetime.fromtimestamp(event['timestamp'] / 1000)
    timestamp_str = timestamp.isoformat(timespec='milliseconds') + 'Z'

    data_item = {
        'device_id': event['device_id'],
        'register_timestamp': timestamp_str,
        'cpu_usage': decimal.Decimal(str(event['cpu_usage'])),
        'cpu_temp': decimal.Decimal(str(event['cpu_temp'])),
        'memory_usage': decimal.Decimal(str(event['memory_usage'])),
        'disk_usage': decimal.Decimal(str(event['disk_usage']))
    }

    pisys_monitoring.put_item(
        Item=data_item
    )

    return
