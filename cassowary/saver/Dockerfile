FROM python:3.8-alpine
COPY ../../requirements.txt /
RUN pip install -r /requirements.txt
COPY cassowary/ /cassowary
CMD ["python", "-m", "cassowary.saver", "run-saver", "mongodb://127.0.0.1:27017", "rabbitmq:127.0.0.1:5672"]