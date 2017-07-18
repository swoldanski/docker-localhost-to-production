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

Your local Docker should be in swarm mode - if this is not a case just run: docker swarm init

```
docker stack deploy -c docker-compose.yml app && docker stack ls && docker stack ps app
```

## Preparing production server

You need working server with ubuntu 16.04+ and key based ssh access.
Repleace "ubuntu" and 54.23.1.45 to your server user and server ip.

```
docker-machine create -d generic --swarm-master --generic-ssh-user "ubuntu" --generic-ip-address 54.23.1.45 production-server
```

## Production deployment

```
docker-compose build && docker-compose push

eval (docker-machine env production-server)

docker stack deploy -c docker-compose.yml app && docker stack ls && docker stack ps app
```

