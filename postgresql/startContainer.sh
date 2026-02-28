#!/usr/bin/env sh

docker run -d -it \
	--name postgres-hudc \
	--env-file .env \
	-p 5432:5432 \
	-v pgdata:/var/lib/postgresql/data \
	--restart unless-stopped \
	hackudc-postgres
