import json
import time

import requests

from config import *
import utils

@utils.logged
class TradingService(object):
    
    def __init__(self, username=None, password=None, trading_mode='paper', 
            token=None, websocket_endpoint=None, startup_done_webhook=None):
        self.trading_mode = trading_mode
        self.username = username
        self.password = password
        self.token = token
        self.base_url = TRADING_SERVICE_BASE_URL
        self.startup_done_webhook = startup_done_webhook
        self.websocket_endpoint = websocket_endpoint

    def start(self):
        url = self.base_url + '/start-service' 
        data = {
          "trading_mode": self.trading_mode,
          "endpoint": self.websocket_endpoint,
          "ib_username": self.username,
          "ib_password": self.password,
          "startup_done_webhook": self.startup_done_webhook,
        }
        r = requests.post(url, data=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        self.logger.info('START')
        self.logger.info(r.text)
        resp = r.json()
        token = resp.get('token')
        self.token = token
        return token, self.parse_status(resp)

    def stop(self):
        url = self.base_url + '/stop-service' 
        r = requests.post(url, headers={'token': self.token})
        self.logger.info('STOP')
        self.logger.info(r.text)
        resp = r.json()
        return self.parse_status(resp)

    def check(self):
        url = self.base_url + '/check-service' 
        r = requests.get(url, headers={'token': self.token})
        self.logger.info('CHECK')
        self.logger.info(r.text)
        resp = r.json()
        return self.parse_status(resp)

    def parse_status(self, resp):
        """ 
            "CONNECTED", "DISCONNECTED", "CONNECTING"
        """
        status = 'DISCONNECTED'
        self.logger.info(resp)
        if resp:
            try:
                resp = dict(resp)
                status = resp.get('status')
            except Exception as e:
                self.logger.error(e)
      
        return status
        
     

if __name__ == '__main__':
    username = IB_USERNAME
    password = IB_PASSWORD
    websocket_endpoint = WEBSOCKET_ENDPOINT
    webhook_url = API_ENDPOINT + '/webhooks/trading_service'
    #t = TradingService(token='7b1ezHDUEa4l7JQXKHpca0-TsNY3cyp57NroGPYMMCQ')
    #print(t.stop())
    t = TradingService(
      username, password, 'paper', 
      websocket_endpoint=websocket_endpoint, 
      startup_done_webhook=webhook_url,
    )
    print(t.start())
    while True:
        time.sleep(4)
        print(t.check())
        
   
   


    
