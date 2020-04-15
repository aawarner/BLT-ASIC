#!/bin/bash

for f in *.svg; do 
   from=$f
   to=`echo $f | cut -d "-" -f 2-`
   mv $from $to
done

