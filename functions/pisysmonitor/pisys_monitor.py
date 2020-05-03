import json
import logging
import os

import psutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PisysMonitor:
    """
    Raspberry Pi のシステム情報をモニタリングを行います。
    Greengrass の Lambda 設定で「/sys ディレクトリへの読み込みアクセス」を有効化する必要があります。
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

        # Greengrass上では、ホスト名が 'sandbox' になるため、環境変数から取得する。
        hostname = os.getenv('AWS_IOT_THING_NAME', None)
        if hostname is None:
            hostname = os.uname().nodename

        topic = 'takanorig/gg_example/%s/monitor' % hostname
        payload = self._measure_utilities()

        logging.info('Monitor result: %s', payload)
        logging.info('Monitor result: topic=%s, payload=%s', topic, payload)

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
            import gpiozero
            cpu_temp = gpiozero.CPUTemperature().temperature
        except Exception as err:
            cpu_temp = None
        # メモリ使用量
        memory_usage = psutil.virtual_memory().percent
        # ディスク使用率
        # TODO Greengrass上だと0になってしまう。
        disk_usage = psutil.disk_usage(path='/').percent

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
