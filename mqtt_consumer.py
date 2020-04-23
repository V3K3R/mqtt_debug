import os
import time

import paho.mqtt.client as mqtt
from config import MqttConfig


class Consumer:
    messages = []

    def _on_message(self, client, userdata, message):
        self.messages.append(message)

    def mqtt_subscriber(self):

        subscriber = mqtt.Client("Consumer")
        subscriber.on_message = self._on_message
        self._client.username_pw_set(username=self.mqtt_user, password=self.mqtt_psw)
        self._client.connect(self.mqtt_host, self.mqtt_port, self.mqtt_timeout)
        subscriber.loop_start()

        yield subscriber

        subscriber.loop_stop()
        subscriber.disconnect()

    def wait_for_message(self, timeout=15):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if self.messages:
                print(self.messages)
            time.sleep(2)

        raise Exception("Message did not arrive within timeout")

if __name__ == "__main__":
    x = Consumer()
    x.wait_for_message()