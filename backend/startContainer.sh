#!/usr/bin/env sh

# SPDX-License-Identifier: Apache-2.0

docker network inspect hackudc-net >/dev/null 2>&1 || docker network create hackudc-net

docker run -d -it \
	--name backend-hudc \
	--network hackudc-net \
	--env-file .env \
	-e QDRANT_HOST=qdrant \
	-e POSTGRES_HOST=postgres-hudc \
	-p 8000:8000 \
	--restart unless-stopped \
	hackudc-backend
