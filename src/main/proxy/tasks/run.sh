#!/usr/bin/env bash

export DOLLAR='$'

while true; do
	NGINX_REPLAY=${PROXY_REPLAY:=3600}
	echo "[INFO] Run Nginx"
	for t in src/templates/conf.d/*.conf; do
		envsubst <"$t" >"/etc/nginx/conf.d/$(basename $t)"
	done
	timeout -t $NGINX_REPLAY nginx -g 'daemon off;'
	sleep 5
done
