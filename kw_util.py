# -*- coding:utf-8 -*-
from bottle import HTTPResponse
import time, datetime
import json


# 文字列(YYYY-MM-DD)で表される開始日付 from_date, 終了日付 to_dateから期間の日付リストを生成
def generate_dates(from_date, to_date):
    if from_date is None:
        from_datetime = datetime.datetime.now()
        from_date = from_datetime.strftime('%Y-%m-%d')
    else:
        from_datetime = datetime.datetime.strptime(from_date, '%Y-%m-%d')


    if to_date is None:
        to_datetime = from_datetime + datetime.timedelta(days=6)
        to_date = to_datetime.strftime('%Y-%m-%d')
    else:
        to_datetime = datetime.datetime.strptime(to_date, '%Y-%m-%d')

    dates = []
    datetime_l = from_datetime
    while datetime_l <= to_datetime:
        dates.append(datetime_l.strftime('%Y-%m-%d'))
        datetime_l = datetime_l + datetime.timedelta(days=1)
    return dates


def generate_response_if_auth_failed():
    header = {"Content-Type": "application/text"}
    res = HTTPResponse(status=302, headers=header)
    res.set_header('location', '/')
    return res

def generate_api_response_if_auth_failed():
    header = {"Content-Type": "application/text"}
    res = HTTPResponse(status=302, headers=header)
    return res

def generate_api_response(res_body):
    header = {"Content-Type": "application/json"}
    res = HTTPResponse(status=200, body=json.dumps(res_body), headers=header)

    return res
