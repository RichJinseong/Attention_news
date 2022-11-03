import datetime
import boto3
import uuid
from decimal import Decimal
import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DDB:
    def __init__(self, **kwargs):
        ACCESS_KEY_ID = kwargs.get("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = kwargs.get("AWS_SECRET_ACCESS_KEY")
        self.dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY_ID,
                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                       region_name='ap-northeast-2')

    def divide_number(self, n):
        if n - int(n) == 0:
            return int(n)
        if n - int(n) != 0:
            return float(n)

    def type_convert(self, body: dict or list):
        if type(body) == dict:
            for k, v in body.items():
                if type(v) == list:
                    body[k] = self.type_convert(v)
                elif type(v) != str:
                    body[k] = self.divide_number(float(v))
                elif type(v) == str:
                    body[k] = v

            return body

        if type(body) == list:
            bucket = []
            for i in body:
                if type(i) == list:
                    return self.type_convert(i)
                elif type(i) != str:
                    bucket.append(self.divide_number(float(i)))
                elif type(i) == str:
                    bucket.append(i)

            return bucket

    def create(self, table, **kwargs):
        session = self.dynamodb.Table(table)
        kwargs['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(kwargs)
        item = json.loads(json.dumps(kwargs), parse_float=Decimal)
        try:
            res = session.put_item(Item=item)
            if res['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception('에러')
            return kwargs[table+'_id']
        except Exception as e:
            raise Exception('에러')

    def get(self, table, **kwargs):
        session = self.dynamodb.Table(table)
        try:
            res = session.get_item(Key=kwargs)
            if res['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception('에러')
            if res.get('Item'):
                res['Item'] = json.loads(json.dumps(res['Item'], cls=DecimalEncoder))
                return res['Item']
            return None
        except Exception as e:
            raise Exception('에러')