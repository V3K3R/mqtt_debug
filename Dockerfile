FROM rabbitmq:3.8.3-management

COPY rabbitmq/definitions.json /etc/definitions/
COPY rabbitmq/rabbitmq.config /etc/rabbitmq/rabbitmq.conf
COPY rabbitmq/enabled_pugins /etc/rabbitmq/enabled_plugins

RUN rabbitmq-plugins enable --offline rabbitmq_management

EXPOSE 15672
