#!/bin/sh
HOST=${1:-"default"}

export BOKEH_SECRET_KEY=$(bokeh secret)
export HOST_IP=$(docker-machine ip ${HOST})
echo "running on ${HOST_IP}"
if [ $HOST = "default" ]; then 
 export DJANGO_DEBUG=True
else 
 export DJANGO_DEBUG=False
fi

# docker-machine env ${HOST}

eval $(docker-machine env ${HOST})

docker-compose -f docker-compose.yml up -d --no-deps --force-recreate --build
sleep 1
docker ps