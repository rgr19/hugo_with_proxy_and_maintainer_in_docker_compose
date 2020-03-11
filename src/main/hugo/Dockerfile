# Use Alpine Linux as our base image so that we minimize the overall size our final container, 
# and minimize the surface area of packages that could be out of date.
FROM python:3.8-alpine AS HUGO_BASE

RUN apk add --update git asciidoctor libc6-compat libstdc++ make bash \
    && apk upgrade \
    && apk add --no-cache ca-certificates

FROM HUGO_BASE as HUGO

LABEL description="Docker container for building static sites with the Hugo static site generator."

ARG HUGO_VERSION
ARG HUGO_TYPE
ARG HUGO_ID=hugo${HUGO_TYPE}_${HUGO_VERSION}
ARG HUGO_FILE=${HUGO_ID}_Linux-64bit.tar.gz
ARG HUGO_DOWNLOAD_ROOT=https://github.com/gohugoio/hugo/releases/download

RUN wget ${HUGO_DOWNLOAD_ROOT}/v${HUGO_VERSION}/${HUGO_FILE} -O /tmp/${HUGO_FILE} \
    && tar -xf /tmp/${HUGO_FILE} -C /tmp \
    && mkdir -p /usr/local/sbin \
    && mv /tmp/hugo /usr/local/sbin/hugo 

FROM HUGO

ARG HUGO_HOME
WORKDIR ${HUGO_HOME}

EXPOSE 1313