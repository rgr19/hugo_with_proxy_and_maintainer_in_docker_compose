#!/usr/bin/env bash

set -e

# shellcheck disable=SC1090
. ${HUGO_TASKS}/hugo_common.sh

echo "[INFO] Hugo cleanup"

if [ "$HUGO_GC" == 'true' ]; then
	$HUGO --gc || true
fi

(
	mkdir -p /tmp/hugo
	if [ -f $HUGO_OUTPUT/.git ]; then
		cp .git* /tmp/hugo
	fi
	if [ -f $HUGO_OUTPUT/CNAME ]; then
		cp CNAME /tmp/hugo
	fi
	echo "[INFO] Try to remove OLD ${HUGO_OUTPUT}"
	rm -Rf ${HUGO_OUTPUT}/*

	if [ ! -z "$(ls -A /tmp/hugo)" ]; then
		cp /tmp/hugo/* ${HUGO_OUTPUT}
	fi
)

if [ -n "$HUGO_THEME" ]; then
	if [ -d "${HUGO_SOURCE}/themes/$HUGO_THEME/public" ]; then
		rm ${HUGO_SOURCE}/themes/$HUGO_THEME/public -Rf
	fi
fi
