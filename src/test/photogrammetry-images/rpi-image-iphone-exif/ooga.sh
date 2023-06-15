for i in {0..32}
do
    exiftool -tagsfromfile ../rpi-images/image${i}.jpg -DateTimeOriginal image${i}.jpg
done
