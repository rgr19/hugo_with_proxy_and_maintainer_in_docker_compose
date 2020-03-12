include .env.project
export # will export content of .env.project
all:  pip reload d b up maintain
clean: reload d
.PHONY: all clean default

SHELL := /usr/bin/env bash
MAKEFLAGS += --jobs=3

printenv:
	printenv

pip:
	pip install -r requirements.txt

reload: pip
	echo '>>> [MAKE] reload with MAKEFLAGS=${MAKEFLAGS}'
	python3.7 src/tasks/reload.py

d: reload
	echo '>>> [MAKE] d'
	docker-compose down --remove-orphans
	docker rm web-proxy web-hugo-blog web-hugo-docs -f || true

b: reload d
	echo '>>> [MAKE] b'
	docker-compose build --parallel

up: reload d b
	echo '>>> [MAKE] up'
	docker-compose up

logs: reload d b
	echo '>>> [MAKE] logs'
	docker-compose logs -f

maintain: reload d b
	echo '>>> [MAKE] maintain'
	python3.7 src/tasks/maintainer.py
