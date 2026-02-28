#!/usr/bin/env sh

docker run -d -it \
	--name backend-hudc \
	--env-file .env \
	-p 8000:8000 \
	--restart unless-stopped \
	hackudc-backend
