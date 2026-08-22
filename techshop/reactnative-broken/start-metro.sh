#!/bin/zsh
ulimit -n 65536
exec npx expo start --port 8081
