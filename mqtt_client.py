import os
import time

import paho.mqtt.client as mqtt
from config import MqttConfig


class MqttSendError(Exception):
    pass

class MqttClient:
    def __init__(self, config):
        self.mqtt_user = config.user
        self.mqtt_psw = config.psw
        self.mqtt_host = config.host
        self.mqtt_port = config.port
        self.mqtt_timeout = config.timeout

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
        msg_info = self._client.publish(self.topic, payload, qos=1)

        start_time= time.time()
        try:
            while time.time() < start_time + self.mqtt_timeout:
                if msg_info.is_published():
                    self._msg_count += 1
                else:
                    raise Exception()
        except Exception:
            raise MqttSendError(f"Could Not publish to Mqtt! Timed out in {self.mqtt_timeout}s")
        finally:
            self._client.loop_stop()
            self._client.disconnect()

if __name__ == "__main__":
    client_1 = MqttClient(config= MqttConfig())
    #client_2 = MqttClient(config=MqttConfig())
    while True:
        client_1.send('1')
        #client_2.send('2')
        time.sleep(5)


