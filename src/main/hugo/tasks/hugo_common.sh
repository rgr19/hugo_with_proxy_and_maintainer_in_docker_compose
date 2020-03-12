#!/usr/bin/env bash

set -e

WATCH="${HUGO_WATCH:=false}"
HUGO_DEBUG="${HUGO_DEBUG:=false}"
SLEEP=${HUGO_REFRESH_TIME:=-1}
HUGO_OUTPUT="${HUGO_OUTPUT:=/output}"
HUGO_PORT="${HUGO_PORT:=1313}"
HUGO_REPLAY=${HUGO_REPLAY:=3600}
HUGO_FAST_RUN=${HUGO_FAST_RUN:=false}
echo "HUGO_FAST_RUN: " $HUGO_FAST_RUN
echo "HUGO_WATCH:" $WATCH
echo "HUGO_GC:" $HUGO_GC
echo "HUGO_SOURCE: " $HUGO_SOURCE
echo "HUGO_CONTENT: " $HUGO_CONTENT
echo "HUGO_OUTPUT: " $HUGO_OUTPUT
echo "HUGO_REFRESH_TIME:" $HUGO_REFRESH_TIME
echo "HUGO_THEME:" $HUGO_THEME
echo "HUGO_BASEURL" $HUGO_BASEURL
echo "HUGO_DEBUG: " $HUGO_DEBUG
echo "HUGO_LANGUAGES_EN_contentdir: " $HUGO_LANGUAGES_EN_contentdir
echo "HUGO_LANGUAGES_KO_contentdir: " $HUGO_LANGUAGES_KO_contentdir
echo "ARGS" $@

mkdir -p ${HUGO_OUTPUT}

HUGO=/usr/local/sbin/hugo
echo "Hugo path: $HUGO"
ls -la $HUGO

echo "Hugo version: "
$HUGO version

if [ -z "$HUGO_THEME" ] || [ -z "$HUGO_BASEURL" ]; then
	echo "Required ENV variables not provided."
	exit 1
fi

function hugo_common() {
	timeout $HUGO_REPLAY $HUGO $@ \
		--theme="$HUGO_THEME" \
		--source="$HUGO_SOURCE" \
		--destination="$HUGO_OUTPUT" \
		--contentDir=$HUGO_CONTENT \
		--baseURL="$HUGO_BASEURL" \
		--watch="$HUGO_WATCH" \
		--debug="$HUGO_DEBUG" \
		--gc="$HUGO_GC"
}

function hugo_server_common() {
	hugo_common server \
		--bind="${HUGO_WEB_NAME}" \
		--port="$HUGO_PORT" \
		--environment="${HUGO_ENV}" \
		--appendPort=false \
		$@
}
