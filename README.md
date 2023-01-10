# Users microservice

## INFO
Responsible for:
- User registration
- User login
- User logout
- Returning user profile data
- Updating user profile data
- Returning a list of all users (for demonstration purposes)

## Build Setup
```bash
# build docker image from Dockerfile
$ docker-compose build

# run docker container in detached mode
$ docker-compose up -d
```

## Post config to consul server
```bash
# get an interactive shell of the running docker-compose service
$ docker-compose exec users_api bash
```

```bash
# enter python shell
$ python
```

```python
# import script post_consul_config()
from app.common.scripts import post_consul_config
# run the script
post_consul_config()
```
