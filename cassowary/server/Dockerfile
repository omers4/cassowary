FROM cassowary:requirements
EXPOSE 8000
ENTRYPOINT ["python3", "-m", "cassowary.server", "run-server", "rabbitmq://rabbitcontainer.cassowarrynet:5672/"]
