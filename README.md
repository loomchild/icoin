#icoin
[![Build Status](https://travis-ci.org/loomchild/icoin.svg?branch=master)](https://travis-ci.org/loomchild/icoin)

## Deployment
The easiest way to deploy icoin and start playing with it is to use docker.

Create docker machine
	docker-machine create -d virtualbox dev
	eval "$(docker-machine env dev)"

Deploy icoin and its dependencies:
    cd deploy/dev
	docker-compose build
	docker-compose up-d

Access icoin
	docker-machine ls 

Take the IP address of your machine and go to <IP>:8080 to access the system and <IP>:8025 to access the emails.
The ports can also be forwarded.
