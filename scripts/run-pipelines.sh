
docker network create cassowarrynet
docker volume create --name ParsedResultsVolume

docker run -d -p 27017:27017 --net cassowarrynet --name mongocontainer mongo
docker run -d -p 5672:5672 --net cassowarrynet --name rabbitcontainer rabbitmq

docker build -t cassowary:requirements .
docker build -t cassowary:server cassowary/server/
docker build -t cassowary:parsers cassowary/parsers/
docker build -t cassowary:api cassowary/api/
docker build -t cassowary:saver cassowary/saver/
docker build -t cassowary:gui cassowary/gui/

echo "Wait for mongo & rabbit to start"
sleep 1m
docker run -d -e PARSER=pose --net cassowarrynet cassowary:parsers
docker run -d -e PARSER=color_image -v ParsedResultsVolume:/tmp/parsed_results --net cassowarrynet cassowary:parsers
docker run -d -e PARSER=depth_image -v ParsedResultsVolume:/tmp/parsed_results --net cassowarrynet cassowary:parsers
docker run -d -e PARSER=feelings --net cassowarrynet cassowary:parsers
docker run -d -e PARSER=personal_details --net cassowarrynet cassowary:parsers
docker run -d  --net cassowarrynet cassowary:saver
docker run -d -p 8888:8888 -v ParsedResultsVolume:/tmp/parsed_results --net cassowarrynet cassowary:api
docker run -d -p 8080:8080 -v ParsedResultsVolume:/tmp/parsed_results --net cassowarrynet cassowary:gui
docker run -d -p 0.0.0.0:8000:8000/tcp -v ParsedResultsVolume:/tmp/parsed_results --net cassowarrynet cassowary:server
