#!/usr/bin/env bash

# works for execution and for sourcing
SCRIPT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd )

tmux new-session -d -s radiopi
tmux send-keys ". \"${SCRIPT_PATH}/runRadioPi.sh\"" C-m
