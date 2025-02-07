docker exec -it mynodered bash

docker ps
docker commit 34311c8b4fd9 hpcooltool:version0.0
docker tag hpcooltool:version0.0 chinkeonglam12345/hpcooltool:version0.0
docker login
docker push chinkeonglam12345/hpcooltool:version0.0

