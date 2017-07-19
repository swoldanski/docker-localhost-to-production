# Docker: localhost -> production
Simple example how to deploy local environment to production server using Docker.

This workshop is really introductory - don't expect too much. 
I want to make you curious what is possible not bored :D

Requirements:
 - Docker 17.03+
 - Docker machine 0.12+
 - working server with installed Ubuntu 16.04+ and ssh access

## Local development & testing environment

Let's start with typical use case - we have epic application and we need a simple way to show a working Proof of Concept or MVP.

```
docker-compose up -d --build

docker-compose ps
docker-compose logs -f

```

**Endpoints to check:**

http://0.0.0.0

http://0.0.0.0:8000

http://0.0.0.0:8080

http://0.0.0.0:8090



Clean up before **real test**

```
docker-compose down -v
```

## Local deployment preflight

Your local Docker should be in *swarm mode* - if this is not a case just run: **docker swarm init**

```
docker-compose build && docker stack deploy -c docker-compose.yml app

docker stack ls
docker stack ps app
docker service ls
```

You can try same endpoints like in previous step and maybe you can notice some changes? ;)

## Preparing production server

You need a working server with ubuntu 16.04+ with key based ssh access.
Replace "ubuntu" and 54.246.249.150 with your server user and your server ip.

```
docker-machine create -d generic --generic-ssh-user "ubuntu" --generic-ip-address 54.246.249.150 production-server

eval $(docker-machine env production-server)
docker-machine ls
docker swarm init
```

## Production deployment

If you don't have images of your application in registry, yet:
```
docker-compose build && docker-compose push
```

Deployment to production server:
```
docker stack deploy -c docker-compose.yml app

docker stack ls
docker stack ps app
docker service ls
```

## Clean up or switching between docker-compose and docker swarm

```
docker-compose down -v
```

```
docker stack rm app
```

## Clean up production server

```
docker stack rm app
docker-machine rm production-server
```

