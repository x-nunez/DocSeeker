#!/usr/bin/env sh

# SPDX-License-Identifier: Apache-2.0

docker run -d -it \
	--name frontend-hudc \
	-p 3000:3000 \
	--restart unless-stopped \
	hackudc-frontend
