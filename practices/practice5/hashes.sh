# 1
sha256sum document.txt > document.sha256
# 2
sha256sum -c document.sha256 > hash_check.txt
# 3
echo "будь-який рядок" >> document.txt
# 4
sha256sum -c document.sha256 >> hash_check.txt
# 5
echo -n "parol123" | sha256sum >> hash_check.txt
echo -n "parol124" | sha256sum >> hash_check.txt
