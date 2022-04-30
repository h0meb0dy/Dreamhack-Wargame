encoded_file_name = './release/secretMessage.enc'
encoded_file = open(encoded_file_name, 'rb')
encoded_file_content = encoded_file.read()
encoded_file_len = len(encoded_file_content)
encoded_file.close()

original_file_content = b''

idx = 0

while 1:
    if idx >= encoded_file_len:
        break

    if idx == 0:
        original_file_content += bytes([encoded_file_content[idx]])

    elif encoded_file_content[idx] == encoded_file_content[idx - 1]:
        original_file_content += bytes([encoded_file_content[idx]])
        count = encoded_file_content[idx + 1]
        original_file_content += bytes([encoded_file_content[idx]]) * count
        idx += 1
        
        if idx + 1 < encoded_file_len:
            idx += 1
            original_file_content += bytes([encoded_file_content[idx]])

    elif encoded_file_content[idx] != encoded_file_content[idx - 1]:
        original_file_content += bytes([encoded_file_content[idx]])

    idx += 1


original_file_name = 'secretMessage.raw'
original_file = open(original_file_name, 'wb')
original_file.write(original_file_content)
original_file.close()