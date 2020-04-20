import time
from datetime import datetime
import ssl
import paho.mqtt.client as paho
mqtt_client = paho.Client("base")
mqtt_client.username_pw_set(username='prometheus-producer', password='123')
mqtt_client.connect('localhost', 1883)
mqtt_client.loop_start()
a = "1111111111111111111111111111111111111111"
try:
    while True:
        # break
        msg = datetime.now().isoformat()
        print(msg)
        message_info = mqtt_client.publish("payload/logbox/errors", a, qos=1)
        message_info.wait_for_publish()
        time.sleep(1)
        a = a + a
except KeyboardInterrupt:
    pass
finally:
    mqtt_client.loop_stop()
