#!/bin/bash
#hw-8 downloader
#loops every minute for an hour

page="https://finance.yahoo.com/most-active"

cnt=0
cnt=$((cnt+1))
while [ $cnt -le 60 ]
do
    cDate="$(date +'%Y_%m_%d_%H_%M_%S')"
    fn="yahoo_${cDate}.html"
    newfn="yahoo_${cDate}.xhtml"
    wget -O $fn $page
    java -jar /usr/share/java/tagsoup-1.2.1.jar --files $fn
    va=$(python3 hw8.py $newfn 2>&1)
    php table.php $va > index.html
    mv /home/nicholas/cs288/hw8/index.html /var/www/html
    cnt=$((cnt+1))
    sleep 60
done
