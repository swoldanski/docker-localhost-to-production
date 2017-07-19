# Docker: localhost -> production
Simple example how to deploy local environment to production server using Docker.

This workshop is really introductory - don't expect too much. 
I want to make you curious what is possible not bored :D

**Requirements:**
 - local working Docker 17.03+
 - local working Docker machine 0.12+
 - working server in the cloud with installed Ubuntu 16.04+ and ssh access
 - after clonning repository **rename** provided env-example file to .env

## Local development & testing environment

Let's start with typical use case - we have epic application and we need a simple way to show a working Proof of Concept or MVP.

```
docker-compose up -d --build

docker-compose ps
docker-compose logs -f

```

**Endpoints to check:**

Our epic web app http://0.0.0.0

Broken sidekick http://0.0.0.0:8000

Master Rabbit http://0.0.0.0:9000

Backup Rabbit http://0.0.0.0:9001

*monitoring & info about our infrastructure:*

cAdvisor http://0.0.0.0:10000

Portainer http://0.0.0.0:10001


### Fix for our sidekick

- Uncomment (remove #) line with BROKER=rabbit-master
- Redeploy our stack executing in shell ```docker-compose up -d```

Now you know how to "fix" (configure) application using **environment variables** at runtime. Try to modify other variables and redeploy stack.



Clean up before **real test**

```
docker-compose down
```

## Production deployment preflight

Your local Docker should be in *swarm mode* - if this is not a case just run: **docker swarm init**

```
docker-compose build && docker stack deploy app --prune -c docker-compose.yml

docker stack ls
docker stack ps app
docker service ls
```

You can try the same endpoints like in previous step and maybe you can notice some changes? ;)

## Preparing production server

You need a working server with ubuntu 16.04+ and key based ssh access.
Replace "ubuntu" and 54.246.249.150 with your server user name and your server ip address or domain.

```
docker-machine create -d generic --generic-ssh-user "ubuntu" --generic-ip-address 54.246.249.150 production-server

eval $(docker-machine env production-server)
docker-machine ls
docker swarm init
docker node ls
```

## Production deployment

You have to push images of your application into registry (remember to change _swoldanski_ in docker-compose.yml to your registered user name for Docker registry):
```
docker-compose build && docker-compose push
```

Deployment to production server:
```
docker stack deploy app --prune -c docker-compose.yml

docker stack ls
docker stack ps app
docker service ls
```

Try the same endpoints like in previous steps but replace 0.0.0.0 with your server ip address or domain.

## What next?

You can continue development of your application. After every iteration bump __VERSION__ in __.env__ file and test it locally with __docker-compose__. When you are ready for next deployment to production or staging, just change ${VERSION:-__0.1.8__} for every service in __docker-compose.yml__ to match current __VERSION__ in __.env__ file and use __docker deploy stack__ to publish your changes.


## Clean up or switching between docker-compose and docker swarm

```
docker-compose down
```

```
docker stack rm app
```

## Clean up production server

```
eval $(docker-machine env production-server)
docker stack rm app
docker-machine rm production-server
```

