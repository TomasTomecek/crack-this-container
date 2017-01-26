# crack-this-container
This is just a game.


## Development

How to connect:

```
$ ssh -i files/id_rsa [-p 9922] root@172.17.0.3
```

Run with

```
$ docker run -v /dev/log:/dev/log ssh
```

Build with

```
$ docker build -t ssh .
```

Set password

```
$ docker exec -ti crackthiscontainer_web_1 python3 ./manage.py createsuperuser
```
