import argparse
import os.path
from cryptography.fernet import Fernet, InvalidToken
import traceback

def run(args):
    if args.E and args.D:
        print("Invalid options: choose [-E] or [-D] (not both)")
    elif args.E:
        if args.k:
            try: 
                key = open(args.k, 'r').read()
                encrypt(args.file, key)
            except Exception as e:
                print(repr(e))
        else:
            key = gen_key(args.g) if args.g else gen_key()
            encrypt(args.file, key)
    elif args.D:
        if args.k:
            try: 
                key = open(args.k, 'r').read()
                decrypt(args.file, key)
            except Exception as e:
                print(repr(e))
        else:
            print("Key missing! Please provide your key with [-g] KEYPATH")

    else:
        print("Missing options [-E] or [-D]")

def encrypt(file_path, key):
    f = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            print('file opened')
            file_data = file.read()
        
        encrypt_data = f.encrypt(file_data)

        with open(file_path, "wb") as file:
            file.write(encrypt_data)

    except FileNotFoundError:
        print("File not found. Please check the path.")
    except e:
        print(e.message)

def decrypt(file_path, key):
    f = Fernet(key)

    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        
        decrypted_data = f.decrypt(encrypted_data)

        with open(file_path, "wb") as file:
            file.write(decrypted_data)

    except FileNotFoundError:
        print("File not found. Please check the path.")
    except InvalidToken:
        print("The key or the file is invalid!")
    except Exception as e:
        print(repr(e))
        traceback.print_exc()

def gen_key(filename="key"):
    key = Fernet.generate_key()
    file_path = filename + ".key"
    with open(file_path, "wb") as key_file:
        key_file.write(key)
    return key
    

def main():
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt a file")
    parser.add_argument("file", help="the file to encrypt/decrypt", type=str)
    parser.add_argument("-E", help="encrypt the file", action="store_true")
    parser.add_argument("-D", help="decrypt the file", action="store_true")
    parser.add_argument("-g", help="generate a new key KEY", type=str)
    parser.add_argument("-k", help="the key to use", type=str)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


