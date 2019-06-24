#!/usr/bin/env bash
# Assuming you start in with a fresh Ubuntu instance.
# (on a side-note. If you hate doing this then learning Docker is worth your time)
sudo apt-get update
git clone https://github.com/aelzeiny/wordcloud
sudo apt-get install -y python3 python3-pip nodejs npm mysql-client
sudo apt-get install python3-pymysql
