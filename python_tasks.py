import os
import csv
import sys
import time
import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime, date, timedelta, timezone

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

def api_ohlcv(timestamp):
    headers = {'Content-Type': 'application/json'}
    api_url_base = 'https://public.bitbank.cc'
    pair = 'btc_jpy'
    period = '1min'
    api_url = '{0}/{1}/candlestick/{2}/{3}'.format(api_url_base, pair, period, timestamp)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        ohlcv = json.loads(response.content.decode('utf-8'))['data']['candlestick'][0]['ohlcv']
        return ohlcv
    else:
        return None

def csv_ohlcv():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    yesterday = "{0:%Y%m%d}".format(yesterday)
    ohlcv = self.api_ohlcv(yesterday)
    open, high, low, close, volume, timestamp = [],[],[],[],[],[]

    for i in ohlcv:
        open.append(int(i[0]))
        high.append(int(i[1]))
        low.append(int(i[2]))
        close.append(int(i[3]))
        volume.append(float(i[4]))
        time_str = str(i[5])
        timestamp.append(datetime.fromtimestamp(int(time_str[:10])).strftime('%Y/%m/%d %H:%M:%M'))
    date_time_index = pd.to_datetime(timestamp) # convert to DateTimeIndex type
    df = pd.DataFrame({'open': open, 'high': high, 'low': low, 'close': close, 'volume': volume}, index=date_time_index)

    f = lambda x: 1 if x>0.0001 else -1 if x<-0.0001 else 0 if -0.0001<=x<=0.0001 else np.nan
    y = df.rename(columns={'close': 'y'}).loc[:, 'y'].pct_change(1).shift(-1).fillna(0)
    X = df.copy()
    y_ = pd.DataFrame(y.map(f), columns=['y'])
    df_ = pd.concat([X, y_], axis=1)
    os.makedirs('../data', exist_ok=True)
    df_.to_csv('../data/ohlcv.csv', header=False, index=False)

def upload_tos3(object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    bucket = os.getenv('AWS_S3_EXAMPLE_BUCKET')
    file_name = '../data/ohlcv.csv'
    object_name = 'ohlcv.csv'

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client(
        's3',
        region_name='ap-northeast-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        config=Config(connect_timeout=5, read_timeout=5)
    )

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def my_task():
    print("awesome execution")

def version():
    print("Python version: {}".format(sys.version))

