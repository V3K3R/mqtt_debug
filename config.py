from dataclasses import dataclass


@dataclass
class MqttConfig:
    user: str = 'prometheus-producer'
    psw: str = '123'
    host: str = 'localhost'
    port: int = 1883
    topic: str = 'payload/logbox/errors'
    timeout: int = 10
    client_name: str = 'Thanos_1'
    qos: int = 1


@dataclass
class Reading:
    asset_group_id: int
    asset_id: int
    mp_id: int
    timestamp: int
