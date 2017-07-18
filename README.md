# Docker: localhost -> production
Simple example how to deploy local environment to production server using Docker 

Requirements:
 - Docker 17.03+
 - Docker machine 0.12+

## Local development & testing environment
```
docker-compose up -d --build && docker-compose ps && docker-compose logs -f

```

## Local deployment preflight

Your local Docker should be in *swarm mode* - if this is not a case just run: **docker swarm init**

```
docker-compose build && docker stack deploy -c docker-compose.yml app && docker stack ls && docker stack ps app && docker service ls
```

## Preparing production server

You need a working server with ubuntu 16.04+ and key based ssh access.
Replace "ubuntu" and 54.246.249.150 to your server user and server ip.

```
docker-machine create -d generic --generic-ssh-user "ubuntu" --generic-ip-address 54.246.249.150 production-server
eval $(docker-machine env production-server) && docker-machine ls && docker swarm init
```

## Production deployment

If you don't have images of your application in registry, yet:
```
docker-compose build && docker-compose push
```

Deployment to production server:
```
docker stack deploy -c docker-compose.yml app && docker stack ls && docker stack ps app && docker service ls
```

## Clean up or switching from docker-compose to docker swarm

```
docker-compose down
```

```
docker stack rm app
```

## Clean up production server

```
docker stack rm app
docker-machine rm production-server
```

