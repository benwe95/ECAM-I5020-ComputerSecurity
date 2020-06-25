import hashlib

CLEAR = "clear.txt"
HASHES_MD5 = "hashes-md5.txt"
HASHES_SHA_256 = "hashes-sha-256.txt"

with open(CLEAR, 'r') as file:
    clear = [item.strip() for item in file.readlines()]

with open(HASHES_MD5, 'w') as file:
    for pwd in clear:
        hash_md5 = hashlib.md5(pwd.encode())
        file.write(hash_md5.hexdigest()+'\n')

with open(HASHES_SHA_256, 'w') as file:
    for pwd in clear:
        hash_sha_256 = hashlib.sha256(pwd.encode())
        file.write(hash_sha_256.hexdigest()+'\n')