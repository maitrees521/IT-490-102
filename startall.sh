#!/bin/bash
echo Enter 1 to start all, 2 to check status, 3 to stop all
read input

case $input in
        1)
         echo Pinging Database Server
         ping -c 2 25.2.14.158
         ssh -t zcarino@25.2.14.158 sudo systemctl start mysql

         echo Pinging Rabbit-MQ-Server
         ping -c 2 25.9.66.151
         ssh -t maitree@25.9.66.151 sudo systemctl start rabbitmq-server 

         echo Pinging Backend Server
         #ping -c 2 25.9.117.215
         #ssh -t erik123@25.9.117.215 sudo systemctl start

         echo Pinging Frontend Server
         ping -c 2 25.4.49.8
         ssh -t shayna@25.4.49.8 sudo systemctl start apache2
         ;;
        2)
        echo Pinging Database Server
        ping -c 2 25.2.14.158
        ssh -t zcarino@25.2.14.158 sudo systemctl status mysql

        echo Pinging Rabbit-MQ-Server
        ping -c 2 25.9.66.151
        ssh -t maitree@25.9.66.151 sudo systemctl status rabbitmq-server 

        echo Pinging Backend Server
        #ping -c 2 25.9.117.215
        #ssh -t erik123@25.9.117.215 sudo systemctl status apache2

        echo Pinging Frontend Server
        ping -c 2 25.4.49.8
        ssh -t shayna@25.4.49.8 sudo systemctl status apache2
        ;;
        3)
        echo Pinging Database Server
        ping -c 2 25.2.14.158
        ssh -t zcarino@25.2.14.158 sudo systemctl stop mysql
        echo Pinging Rabbit-MQ-Server
        ping -c 2 25.9.66.151
        ssh -t maitree@25.9.66.151 sudo systemctl stop rabbitmq-server 

        echo Pinging Backend Server
        #ping -c 2 25.9.117.215
        #ssh -t erik123@25.9.117.215 sudo systemctl stop

        echo Pinging Frontend Server
        ping -c 2 25.4.49.8
        ssh -t shayna@25.4.49.8 sudo systemctl stop apache2
        ;;
esac