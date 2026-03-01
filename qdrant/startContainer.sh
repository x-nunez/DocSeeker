#!/usr/bin/env sh

# SPDX-License-Identifier: Apache-2.0

docker network inspect hackudc-net >/dev/null 2>&1 || docker network create hackudc-net

docker run -d -it \
	--name qdrant \
	--network hackudc-net \
	-p 6333:6333 \
	-v qdrant_storage:/qdrant/storage \
	--restart unless-stopped \
	qdrant/qdrant
