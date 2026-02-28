#!/usr/bin/env sh

cd qdrant
bash startContainer.sh

cd ../postgresql
bash buildImage.sh
bash startContainer.sh

cd ../frontend
bash buildImage.sh
bash startContainer.sh

cd ../backend
bash buildImage.sh
bash startContainer.sh
