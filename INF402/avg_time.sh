#!/bin/bash

rm -f /tmp/mtime.$$

for x in {1..20}
do
  /usr/bin/time -f "real %e user %U sys %S" -a -o /tmp/mtime.$$ $@
  tail -1 /tmp/mtime.$$
done

awk '{ et += $2; ut += $4; st += $6; count++ } END {  printf "Average:\nreal %.3f user %.3f sys %.3f\n", et/count, ut/count, st/count }' /tmp/mtime.$$
