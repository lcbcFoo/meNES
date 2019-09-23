# Every current log becomes the standard test solution
cp -a log/. res/

for x in res/*.log; do 
    mv "$x" "${x%.log}.r";
done