#!/bin/bash
docker stop mysql-cmdline;
docker rm mysql-cmdline;
docker run -it --name mysql-cmdline --link mysql:db mysql:5.7.14 bash
