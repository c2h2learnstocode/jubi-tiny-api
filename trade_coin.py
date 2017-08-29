# -*- coding: utf-8 -*-

"""
成功请求的参数顺序：
signature,nonce,key
nonce,singature,key
(nonce参数一定要在key前头)
"""

import requests
import time
import hashlib
import hmac
import collections


class Jubi(object):

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def get_nonce(self):
        curr_stamp = time.time()*100
        nonce = int(curr_stamp)
        return nonce

    def get_md5(self,s):
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest()

    def get_params(self):
        nonce_value = self.get_nonce()
        key_value = self.public_key
        private_key = self.private_key
        string = ('nonce=' + str(nonce_value) + '&' + 'key=' + key_value).encode('utf-8')
        private_key_md5 = self.get_md5(private_key).encode('utf-8')
        signature = hmac.new(private_key_md5, string, digestmod=hashlib.sha256).hexdigest()
        dict_ordered = collections.OrderedDict()
        dict_ordered['signature'] = signature
        dict_ordered['nonce'] = nonce_value
        dict_ordered['key'] = key_value
        return dict_ordered

    def get_trade_param(self, amount, price, order_type, coin):
        nonce_value = self.get_nonce()
        key_value = self.public_key
        private_key = self.private_key
        string = ('nonce=' + str(nonce_value) + '&key=' + key_value+'&amount='+str(amount)+'&price='+str(price)+'&type='+str(order_type)+'&coin='+str(coin)).encode('utf-8')
        dict_ordered = collections.OrderedDict()
        private_key_md5 = self.get_md5(private_key).encode('utf-8')
        signature = hmac.new(private_key_md5, string, digestmod=hashlib.sha256).hexdigest()
        dict_ordered['signature'] = signature
        dict_ordered['nonce'] = nonce_value
        dict_ordered['key'] = key_value
        dict_ordered['amount']=amount
        dict_ordered['price']=price
        dict_ordered['type']=order_type
        dict_ordered['coin']=coin
        return dict_ordered
        

pub_key="your_pubkey"
pri_key="your_prikey"


jubi = Jubi(pub_key,pri_key)


data = jubi.get_trade_param(1.1, 64.01, "sell", "lsk")
#data = jubi.get_params()
print(data)
#resp = requests.post(url='https://www.jubi.com/api/v1/balance/',data=data).text
resp = requests.post(url='https://www.jubi.com/api/v1/trade_add/',data=data).text
print(resp)


