#!/usr/bin/env sh

# SPDX-License-Identifier: Apache-2.0

docker network inspect hackudc-net >/dev/null 2>&1 || docker network create hackudc-net

docker run -d -it \
	--name postgres-hudc \
	--network hackudc-net \
	--env-file .env \
	-p 5432:5432 \
	-v pgdata:/var/lib/postgresql/data \
	--restart unless-stopped \
	hackudc-postgres
