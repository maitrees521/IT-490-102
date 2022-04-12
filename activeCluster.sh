#!/bin/bash
sudo rabbitmqctl cluster_status --formatter=json | jq -r .running_nodes[]
