#!/bin/sh

# works for execution and for sourcing
SCRIPT_PATH=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd )

export PYTHONPATH="${SCRIPT_PATH}"
export AWS_DEFAULT_REGION="us-west-2"
export AWS_ACCESS_KEY_ID="your key"
export AWS_SECRET_ACCESS_KEY="your secret"

python3 -m radiopi
