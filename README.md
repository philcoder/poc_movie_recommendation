PoC for Movie Recommendation Engine (MRE)
====================================================================

This guide will provide you all the steps to run Movie Recommendation Engine web application.


### System Requeriments:

1. Ubuntu LTS 18.04 (tested distro) or another linux
2. Components docker and docker-compose already installed on machine
3. HDD 2 GB available

### Technologies used:

1. Web side: Python 3.x, Flask, Javascript, Jquery and Bootstrap
2. Database: PostgreSQL
3. ML-Engine: rabbitMQ and python 3.x panda and numpy libraries
4. Others: Linux, ShellScript, Docker


### How to Execute like Dev

Go inside clone folder '../poc_movie_recommendations' and execute follows commands as you wish.

For startup all services
```
docker-compose -f docker-compose.yml up -d --build
```

For manually started 'web' container follow commands.
```
docker exec -it web bash

#only at first time as dev (for build database)
./web_run db_build

#to see flask running
./web_run start

CTRL+C for stop executing
```

Access web service: http://localhost:16000/webui

For manually started 'ml-service' container follow commands.
```
docker exec -it ml-service bash

#execute
./main.py

CTRL+C for stop executing
```

### How to Deploy all services to production

Go inside clone folder '../poc_movie_recommendations' and execute follows commands as you wish.

For startup all services
```
docker-compose -f docker-compose-deploy.yml up -d --build
```

For stop all services
```
docker-compose -f docker-compose-deploy.yml down
```

For stop and cleanup volumes 
```
docker-compose -f docker-compose-deploy.yml down --volumes
```

Access web service: http://localhost:16000/webui

### Future Works

- Implements Pattern Database per service
-- Remove ml-service from database access
-- Only the web componente will manipulate database (using Schema-per-service)

- Each web-front client will publish to activemq (have own queue) and wait for the recommended movies (Choreography-based saga)
