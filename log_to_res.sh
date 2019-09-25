# Every current log becomes the standard test solution
if [ $# -eq 0 ]
then
  echo "Missing: Argument"
  echo "Inform the addressing mode abbreviation."
  echo "Example: log_to_res.sh imd"
  exit 1
fi

cp -a log/*$1* res/

for x in res/*.log; do
    mv "$x" "${x%.log}.r";
done
