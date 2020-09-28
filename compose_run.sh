#!/bin/bash

docker-compose run --rm "$@"
EXIT_CODE=$?
docker-compose down
exit $EXIT_CODE
