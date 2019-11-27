ALPH = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def gen_keyword_indices(keyword):
    keyword_indices = []
    for char in keyword.lower():
        if char in ALPH:
            keyword_indices.append(ALPH.index(char))
    return keyword_indices

def encrypt(message, keyword_indices):
    message_encrypted = []
    count = 0
    for char in message.lower():
        if char in ALPH:
            index = ALPH.index(char)
            index_encrypted = (index+keyword_indices[count])%26
            char_encrypted = ALPH[index_encrypted]
            message_encrypted.append(char_encrypted.upper())

            count += 1
            count = count % len(keyword_indices)
    sep = ""
    return sep.join(message_encrypted)

def decrypt(message_encrypted, keyword_indices):
    message = []
    count = 0
    for char_encrypted in message_encrypted.lower():
        if char_encrypted in ALPH:
            index_encrypted = ALPH.index(char_encrypted)
            index = (index_encrypted-keyword_indices[count])%26
            char = ALPH[index]
            message.append(char)
            count += 1
            count = count % len(keyword_indices)
    sep = ""
    return sep.join(message)


if __name__ == "__main__":
    keyword = "Bleu"
    keyword_indices = gen_keyword_indices(keyword)
    print("Keyword: {}\t indices: {}".format(keyword, keyword_indices))

    message = "Les renforts arrivent. L'ennemi attaquera demain matin par le nord."
    message_encrypted = encrypt(message, keyword_indices)
    message_decrypted = decrypt(message_encrypted, keyword_indices)

    print("\nmessage: {}\nmessage_encrypted: {} \nmessage_decrypted: {}\n".format(
        message, message_encrypted, message_decrypted))