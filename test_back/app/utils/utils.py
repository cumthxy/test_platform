from app.izi import client
import datetime
import pandas as pd
import yaml
import os
import json
api_test001 = client("LxiDHIMGFpXzpLGIehps", "jXUlrGhblTtxWduqtCDMLxiDHIMGFpXzpLGIehps")
def reverse_ktp_md5(ktp_md5):
    url_md5 = "http://10.0.13.253:8910/v1/md5ktp"
    post_data = {"ktp": ktp_md5}
    ktpjsonData = json.loads(api_test001.request(url_md5, post_data))
    ktp = ktpjsonData['message']
    return ktp

def reverse_phone_md5(phone_md5):
    url_md5 = "http://10.0.13.253:8910/v1/md5phone"
    post_data = {"phone": phone_md5 }
    phonejsonData = json.loads(api_test001.request(url_md5, post_data))
    phone = phonejsonData['message']
    return phone

def reverse_mxphone_md5(phone_md5):
    url_md5 = "http://10.0.13.253:8910/v1/mxmd5phone"
    post_data = {"phone": phone_md5 }
    phonejsonData = json.loads(api_test001.request(url_md5, post_data))
    phone = phonejsonData['message']
    return phone



def format_ts(tx, country):
    ts = str(tx)
    print("ts",ts)
    if "+08:00" in ts:
        country = "CN"
        print("CCCCCNNNNNNNN")
    if pd.isna(tx) or ts == '' or  ts == 'Nan' or ts == 'nan':
        return ''
    now = datetime.datetime.now()
    try:
        if not ts.isdigit():
            ts = pd.to_datetime(ts)
            if country =="MX":
                ts = ts +datetime.timedelta(hours=6)
            elif country =="IN":
                ts = ts - datetime.timedelta(hours=5.5)
            elif country =="CN":
                ts = ts - datetime.timedelta(hours=8)
            else:
                ts = ts - datetime.timedelta(hours=7)
            return ts.strftime('%Y%m%d')
        elif len(ts) == 10 and ts.isdigit():
            # unixtimestamp
            ts = datetime.datetime.fromtimestamp(int(ts))
            return ts.strftime('%Y%m%d')
        elif len(ts) == 8 and ts.isdigit():
            return ts
        elif len(ts) == 13 and ts.isdigit():
            # unixtimestamp * 1000, millseconds
            ts = datetime.datetime.fromtimestamp(int(ts[:10]))
            return ts.strftime('%Y%m%d')
        elif '.' in ts and ts.replace('.', '').isdigit() and len(ts) >= 13:
            ts = datetime.datetime.fromtimestamp(int(ts[:10]))
            return ts.strftime('%Y%m%d')
        else:
            return ""
    except Exception as e:
        print(e)
        print("--------------------------ts 出错了，都是空的--------------------------")
        return ""
    
