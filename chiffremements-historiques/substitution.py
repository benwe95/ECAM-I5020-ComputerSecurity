from random import randrange

ALPH = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def gen_key():
    my_list = ALPH.copy()
    key = []
    for char in ALPH:
        index = randrange(0, len(my_list))
        key.append(my_list[index])
        del my_list[index]
    return key

def encrypt(message, key):
    message_encrypted = []
    for char in message.lower():
        if char in ALPH:
            index = ALPH.index(char)
            char_encrypted = key[index]
            message_encrypted.append(char_encrypted.upper())
    sep = ""
    return sep.join(message_encrypted)

def decrypt(message_encrypted, key):
    message = []
    for char_encrypted in message_encrypted.lower():
        index = key.index(char_encrypted)
        char = ALPH[index]
        message.append(char.lower())
    sep = ""
    return sep.join(message)


if __name__ == "__main__":
    key = gen_key()
    print(ALPH)
    print(key)

    message = "Les renforts arrivent. L'ennemi attaquera demain matin par le nord."
    message_encrypted = encrypt(message, key)
    message_decrypted = decrypt(message_encrypted, key)

    print("\nmessage: {}\nmessage_encrypted: {} \nmessage_decrypted: {}\n".format(
        message, message_encrypted, message_decrypted))