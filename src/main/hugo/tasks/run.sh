#!/usr/bin/env bash

echo "[INFO] Content of DIR HUGO_HOME"
ls -la $HUGO_HOME

echo "[INFO] Content of DIR HUGO_TASKS"
ls -la $HUGO_TASKS

echo "[INFO] Content of DIR HUGO_SOURCE"
ls -la $HUGO_SOURCE

echo "[INFO] Content of DIR HUGO_CONTENT"
ls -la $HUGO_CONTENT

echo "[INFO] PRINTENV"
printenv

while true; do
	# shellcheck disable=SC1090
	. ${HUGO_TASKS}/hugo_common.sh

	ls -la ${HUGO_SOURCE}
	echo "[INFO] Hugo MAIN loop..."

	if [[ $HUGO_WATCH != 'false' ]]; then
		if [[ $HUGO_FAST_RUN == 'true' ]]; then
			echo "[INFO] Hugo fast run..."
			hugo_server_common $@ || true
		else
			echo "[INFO] Hugo Watching..."
			hugo_server_common --ignoreCache --disableFastRender server "$@" || true
		fi
	else
		echo "[INFO] Building one time..."
		hugo_common "$@" || true
	fi

	if [[ $HUGO_REFRESH_TIME == -1 ]]; then
		echo "[INFO] Exit on negative HUGO_REFRESH_TIME..."
		exit 0
	fi
	echo "[INFO] Sleeping for $HUGO_REFRESH_TIME seconds..."
	sleep $SLEEP
done
