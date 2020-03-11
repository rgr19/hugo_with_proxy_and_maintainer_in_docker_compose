#!/usr/bin/env bash

while true; do
	NGINX_REPLAY=${PROXY_REPLAY:=3600}
	echo "[INFO] Run Nginx"
	timeout -t $NGINX_REPLAY nginx -g 'daemon off;'
	sleep 5
done
