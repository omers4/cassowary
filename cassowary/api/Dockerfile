FROM python:3.8-alpine
COPY ../../requirements.txt /
RUN pip install -r /requirements.txt
COPY cassowary/ /cassowary
CMD ["python", "-m", "cassowary.api", "run-server"]