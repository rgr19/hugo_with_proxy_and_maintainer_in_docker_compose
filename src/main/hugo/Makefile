# Makefile
include .env
include .env.local

SHELL := /usr/bin/env bash
CPUS ?= $(shell sysctl -n hw.ncpu || echo 1)
MAKEFLAGS += --jobs=$(CPUS)

.PHONY: all docker
all: clean run
docker: docker_build docker_run

check_env:
	echo 	\
		"HUGO_VERSION=${HUGO_VERSION}" \
		"HUGO_TYPE=${HUGO_TYPE}" \
		"HUGO_HOME=${HUGO_HOME}" \
	    "${HOST_HUGO_OUTPUT}:${HUGO_HOME}:rw"  \
		"${HOST_HUGO_CONTENT}:${HUGO_OUTPUT}:ro" \
		"${HOST_HUGO_CACHE}:${HUGO_RESOURCES}:rw"

clean:
	echo "[MAKE] Clean"
	bash ${HUGO_TASKS}/cleanup.sh
run:
	echo "[MAKE] Run"
	bash ${HUGO_TASKS}/run.sh

docker_build:
	docker build \
		--tag blog-docker \
		--build-arg HUGO_VERSION=${HUGO_VERSION} \
        --build-arg HUGO_TYPE=${HUGO_TYPE} \
        --build-arg HUGO_HOME=${HUGO_HOME} \
        .

docker_run: docker_build
	docker run \
		-it \
		--env-file .env \
		--expose ${HUGO_PORT} \
		--net host \
		-v "${PWD}/:${HUGO_HOME}:ro" \
		-v "${PWD}/${HOST_HUGO_OUTPUT}:${HUGO_OUTPUT}:rw"  \
		-v "${PWD}/${HOST_HUGO_CONTENT}:${HUGO_CONTENT}:ro" \
		-v "${PWD}/${HOST_HUGO_CACHE}:${HUGO_RESOURCES}:rw" \
		blog-docker \
		make all
