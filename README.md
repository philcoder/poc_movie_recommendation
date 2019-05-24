PoC for Movie Recommendation Engine (MRE)
====================================================================

This guide will provide you all the steps to run Movie Recommendation Engine web application.

### Technologies used:

1. Web side: Python 3.x, Flask, Javascript, Jquery and Bootstrap
2. Database: PostgreSQL
3. ML-Engine: rabbitMQ and python 3.x panda and numpy libraries
4. Others: Linux, ShellScript, Docker


How to Execute
-------

Start all services with docker compose

```
docker-compose -f docker-compose.yml up -d --build
```

Stop all services with docker compose
```
docker-compose -f docker-compose.yml down
```

Stop all services and clean-up volumes with docker compose
```
docker-compose -f docker-compose.yml down --volumes
```

Join inside docker container
```
docker exec -it <container_name> bash
```

Text TODO. 
