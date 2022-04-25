import hashlib

ps = 0

while 1:
    hash_result = hashlib.md5()
    hash_result.update(str(ps).encode())
    
    if b'\'=\'' in hash_result.digest():
        break
    else:
        ps += 1

print(ps)