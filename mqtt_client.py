import os
import time

import paho.mqtt.client as mqtt
from config import MqttConfig
from threading import Thread


class MqttSendError(Exception):
    pass


class MqttClient:
    def __init__(self, config):
        self.mqtt_user = config.user
        self.mqtt_psw = config.psw
        self.mqtt_host = config.host
        self.mqtt_port = config.port
        self.mqtt_timeout = config.timeout
        self.qos = config.qos

        self.client_name = config.client_name
        self.topic = config.topic
        self._msg_count = 0

        self._client = mqtt.Client(config.client_name)

    def _connect(self) -> None:
        self._client.username_pw_set(username=self.mqtt_user, password=self.mqtt_psw)
        self._client.connect(self.mqtt_host, self.mqtt_port, self.mqtt_timeout)
        self._client.loop_start()

    def send(self, payload) -> None:
        self._connect()
        msg_info = self._client.publish(self.topic, payload, qos=self.qos)

        start_time = time.time()
        try:
            while time.time() - start_time < self.mqtt_timeout:
                if msg_info.is_published():
                    self._msg_count += 1
                    return
            else:
                raise Exception()
        except Exception:
            print(f"Could Not publish{payload} to Mqtt! Timed out in {self.mqtt_timeout}s")

            # raise MqttSendError(
            #     f"Could Not publish{payload} to Mqtt! Timed out in {self.mqtt_timeout}s")
        finally:
            self._client.loop_stop()
            self._client.disconnect()

    def send_synchrone(self, payload) -> None:
        self._connect()
        msg_info = self._client.publish(self.topic, payload, qos=self.qos)

        start_time = time.time()
        try:

            if msg_info.wait_for_publish():
                #self._msg_count += 1
                return
            else:
                raise Exception()
        except Exception:
            print(f"Could Not publish{payload} to Mqtt! Timed out in {self.mqtt_timeout}s")

            # raise MqttSendError(
            #     f"Could Not publish{payload} to Mqtt! Timed out in {self.mqtt_timeout}s")
        finally:
            self._client.loop_stop()
            self._client.disconnect()

    def run(self, iterations=5000, payload="1", x=2):
        for i in range(0, iterations):
            self.send(payload)
            time.sleep(x)

    def run_synchrone(self, iterations=5000, payload="1", x=2):
        for i in range(0, iterations):
            self.send_synchrone(payload)
            time.sleep(x)


if __name__ == "__main__":
    client_1 = MqttClient(config=MqttConfig())
    client_2 = MqttClient(config=MqttConfig(client_name='Thanos_2', qos=1))
    # client_3 = MqttClient(config=MqttConfig(client_name='Thanos_3'))
    # client_4 = MqttClient(config=MqttConfig(client_name='Thanos_4'))
    # client_5 = MqttClient(config=MqttConfig(client_name='Thanos_5'))

    th1 = Thread(target=client_1.run, args=[1000, ])
    th2 = Thread(target=client_2.run_synchrone, args=[1000, ])
    th1.start()
    th2.start()
    runing_threads = [th1, th2]
    for t in runing_threads:

        t.join()
