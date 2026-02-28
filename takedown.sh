#!/usr/bin/env sh
# SPDX-License-Identifier: Apache-2.0

docker rm -f backend-hudc frontend-hudc postgres-hudc qdrant

docker rmi hackudc-backend hackudc-frontend hackudc-postgres

docker volume remove pgdata qdrant_storage

docker network remove hackudc-net
