#!/usr/bin/env sh

docker run -d \
	--name frontend-hudc \
	-p 3000:3000 \
	--restart unless-stopped \
	hackudc-frontend
