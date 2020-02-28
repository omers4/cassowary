FROM cassowary:requirements
EXPOSE 8888
ENTRYPOINT python3 -m cassowary.api run-server -p 8888 -d mongodb://mongocontainer.cassowarrynet:27017
