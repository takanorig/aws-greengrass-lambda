import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
sys.path.append('../')

# ダミーのcredential情報を環境変数に設定する。
os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
os.environ['AWS_ACCESS_KEY_ID'] = 'DO_NOT_CHANGE_THIS_VALUE'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'DO_NOT_CHANGE_THIS_VALUE'
