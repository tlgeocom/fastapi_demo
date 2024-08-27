#!/bin/bash
version=v1.0
name=fastapi_demo
container_id=$(docker ps -aqf "name=${name}")
if [ "$container_id" != "" ]
then
  docker stop $container_id
  docker rm $container_id
else
  echo '未发现容器信息'
fi
image_id=$(docker images -q $name:$version)
if [ "$image_id" != "" ]
then
  docker rmi $image_id
else
  echo '未发现镜像信息'
fi

docker build -t ${name}:$version .   
docker run -d -p 8000:8000 --name ${name} --restart=always $name:$version
echo "SUCCESS"
