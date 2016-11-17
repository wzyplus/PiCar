#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2016-11-16 22:25'

import time
import threading
import random

random.seed()

class DHT(object):

    def __init__(self, pin, interval=60, mock=False):
        '''
        DHT11温度和湿度传感器
        :param pin: DHT使用的GPIO引脚
        :param interval: 读取间隔，默认60秒
        :param mock: 是否模拟
        '''

        self._humidity = 0.0
        self._temperature = 0.0

        self._pin = pin
        self._mock = mock
        self._interval = interval
        self._job = threading.Thread(target=self._run)
        self._job.daemon = True
        self._job.start()

    @property
    def humidity(self):
        '''
        湿度
        :return: float number
        '''
        return self._humidity

    @property
    def temperature(self):
        '''
        温度, 摄氏度
        :return: float number
        '''
        return self._temperature

    @property
    def value(self):
        return {
            'humidity': self.humidity,
            'temperature': self._temperature,
        }

    def _run(self):
        if not self._mock:
            import Adafruit_DHT
        else:
            self._humidity = 44.0
            self._temperature = 20.0

        while True:
            if not self._mock:
                h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, self._pin)
            else:
                h = self._random_change(self._humidity)
                t = self._random_change(self._temperature)

            self._humidity = h
            self._temperature = t

            time.sleep(self._interval)

    def _random_change(self, value):
        incr = random.choice([False, True])
        change = random.random()
        if incr:
            return value + change
        else:
            return value - change
