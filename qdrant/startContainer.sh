#!/usr/bin/env sh

docker run -d \
	--name qdrant \
	-p 6333:6333 \
	-v qdrant_storage:/qdrant/storage \
	--restart unless-stopped \
	qdrant/qdrant
