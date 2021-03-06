ALPH = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def encrypt(message, key):
    message_encrypted = []
    for char in message.lower():
        if char in ALPH:
            index = ALPH.index(char)
            index_encrypted = (index+key)%26
            char_encrypted = ALPH[index_encrypted]
            message_encrypted.append(char_encrypted.upper())

    sep = ""
    return sep.join(message_encrypted)


def decrypt(message_encrypted, key):
    message = []
    for char_encrypted in message_encrypted.lower():
        if char_encrypted in ALPH:
            index_encrypted = ALPH.index(char_encrypted)
            index = (index_encrypted-key)%26
            char = ALPH[index]
            message.append(char)

    sep = ""
    return sep.join(message)

if __name__ == "__main__":
    message = "Les renforts arrivent. L'ennemi attaquera demain matin par le nord."
    key = 3
    message_encrypted = encrypt(message, key)
    message_decrypted = decrypt(message_encrypted, key)
    print("\nmessage: {}\nmessage_encrypted: {} \nmessage_decrypted: {}\n".format(
        message, message_encrypted, message_decrypted))

for key in range (1, 26):
    print ("Key: {} - {}".format(key, decrypt(message_encrypted, key)))
   