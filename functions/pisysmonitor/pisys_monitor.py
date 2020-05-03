import json
import logging
import os

import psutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PisysMonitor:
    """
    Raspberry Pi のシステム情報をモニタリングを行います。
    """

    def __init__(self, client=None):
        # Greengrass SDK が読み込めない場合は、Boto3 を読み込んで実行できるようにする。
        # greengrasssdk をモック実行できるようにするため。
        if client is None:
            try:
                import greengrasssdk
                iotdata = greengrasssdk.client('iot-data')
                logger.info('Use greengrasssdk.')
            except:
                import boto3
                iotdata = boto3.client('iot-data')
                logger.info('Use boto3.')

            self.__client = iotdata
        else:
            self.__client = client

    def monitor(self):
        """
        システムのハードウェア情報を測定し、結果を Greengrass Core へ通知します。
        """

        topic = 'takanorig/gg_example/%s/monitor' % os.uname()[1]
        payload = self._measure_utilities()

        logging.info('Monitor result: %s', payload)

        try:
            self.__client.publish(topic=topic, payload=json.dumps(payload))
        except Exception as err:
            logger.exception('Failed to publish message. : topic=%s', topic)

    def _measure_utilities(self):
        """
        システムのハードウェア情報を取得します。

        return 測定結果
        """

        # CPU使用率（1秒平均）
        cpu_usage = psutil.cpu_percent(interval=1)
        # CPU温度
        try:
            cpu_temp = psutil.sensors_temperatures()['coretemp']
        except AttributeError as err:
            cpu_temp = None
        # ディスク使用率
        disk_usage = psutil.disk_usage(path='/').percent
        # メモリ使用量
        memory_usage = psutil.virtual_memory().percent

        utilities = {
            'cpu_usage': cpu_usage,
            'cpu_temp': cpu_temp,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage
        }

        # None要素の除去
        filtered = {k: v for k, v in utilities.items() if v is not None}
        utilities.clear()
        utilities.update(filtered)

        return utilities
