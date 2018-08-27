#URLS="https://www.facebook.com/nataliia.semeniv"

#URLS="\
#https://www.facebook.com/olga.pogynaiko \
#https://www.facebook.com/sharhovska.olena"

#https://www.facebook.com/yaryna.ya
#https://www.facebook.com/ruslana.radchuk \
#https://www.facebook.com/yablonska.oksana.sevama \
#https://www.facebook.com/uakateryna \
#https://www.facebook.com/olena.pavlova

URLS=$@

for URL in $URLS 
do
  SHORT=`echo $URL | sed -E 's/^.*\/([^\/]+)$/\1/g'`
  echo $f $SHORT
  ./fb.py masha.shvedova@gmail.com zrivkoren2 $URL 2>&1 | tee $SHORT.log
  ls -lh $SHORT.txt
done

