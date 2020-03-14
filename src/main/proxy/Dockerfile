FROM nginx:1.15.9-alpine AS PROXY_BASE

RUN apk add --update git make bash \
    && apk upgrade \
    && apk add --no-cache ca-certificates

FROM PROXY_BASE

WORKDIR /nginx
