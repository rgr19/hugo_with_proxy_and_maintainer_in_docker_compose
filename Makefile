all:  reload d b upd maintain logs
clean: reload d
.PHONY: all clean default

SHELL := /usr/bin/env bash
MAKEFLAGS += --jobs=3


pip:
	pip install -r requirements.txt

reload:
	echo '>>> [MAKE] reload with MAKEFLAGS=${MAKEFLAGS}'
	python3.7 src/tasks/reload.py

d: reload
	echo '>>> [MAKE] d'
	docker-compose down --remove-orphans

b: reload d
	echo '>>> [MAKE] b'
	docker-compose build --parallel

up: reload d b
	echo '>>> [MAKE] up'
	docker-compose up

upd: reload d b
	echo '>>> [MAKE] upd'
	docker-compose up -d

logs: reload d b upd
	echo '>>> [MAKE] logs'
	docker-compose logs -f

maintain: reload d b upd
	echo '>>> [MAKE] maintain'
	python3.7 src/tasks/maintainer.py
