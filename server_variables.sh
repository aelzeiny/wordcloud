#!/usr/bin/env bash
# AWS information
export AWS_REGION_NAME="us-east-1"
# Map this EC2 with IAM roles. Then you don't need an access_key, secret_key, or token
# export AWS_ACCESS_KEY_ID="<Set the IAM role instead of assigning this correctly>"
# export AWS_SECRET_ACCESS_KEY="<Set the IAM role instead of assigning this correctly>"
# export AWS_SESSION_TOKEN="<Set the IAM role instead of assigning this correctly>"

# Database connectivity
export db_host="<your_rds_host>"
export db_port="<your_rds_port>"
export db_user="<your_rds_user>"
export db_pass="<your_rds_password>"