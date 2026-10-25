# 1
mkdir -p project/src project/data project/docs
# 2
mv summary.py project/src
mv sample.txt project/data
# 3
touch project/docs/readme.txt
echo "# CS101 Practice 4" > project/docs/readme.txt
# 4
touch project/config.local
echo "API_KEY=demo-1234-ce-ne-spravzhniy-kliuch" > project/config.local
# 5
cp project/data/sample.txt project/data/backup.txt
rm project/data/sample.txt
# 6
ls -lR project > structure.txt
# 7
grep -r "коміт" project/data > found.txt
# 8
ls project/data | wc -l >> found.txt
