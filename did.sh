#! /bin/sh
# This script is based on the following idea: https://theptrk.com/2018/07/11/did-txt-file/
cd $(dirname $0)
git pull > /dev/null
d=$(dirname $0)/did
f=$(date +"%W-%Y").txt
touch $d/$f
nvim +'normal Go' +'r!date' $d/$f
git add --all > /dev/null
git commit -m "$(date)" > /dev/null
git push origin master > /dev/null
