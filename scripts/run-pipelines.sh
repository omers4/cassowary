cd $ROOT/server/
docker build -t cassowary:server .
cd $ROOT/parsers/
docker build -t cassowary:parsers .
cd $ROOT/api/
docker build -t cassowary:api .
cd $ROOT/saver/
docker build -t cassowary:saver .

docker run -d -p 8000:8000 cassowary:server
docker run -d -p 5672:5672 rabbitmq
docker run -d -e PARSER=pose cassowary:parsers
docker run -d -e PARSER=color_image cassowary:parsers
docker run -d -e PARSER=depth_image cassowary:parsers
docker run -d -e PARSER=feelings cassowary:parsers
docker run -d -e PARSER=personal_details cassowary:parsers
docker run -d -p 27017:27017 mongo
docker run -d cassowary:saver
docker run -d -p 8888:8888 cassowary:api_server
