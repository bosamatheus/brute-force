import argparse
from time import time
from zipfile import ZipFile, BadZipFile
import string
import itertools

parser = argparse.ArgumentParser(description="Unzips a password protected .zip", usage="main.py -z easy.zip")
parser.add_argument("-z", "--zip", required=True, help="Location and the name of the .zip file.")
parser.add_argument("-k", "--k", type=int, required=True, help="Maximum length k for the password.")
parser.add_argument("-c", "--chars", required=False, help="String with ASCII characters to be used.")
args = parser.parse_args()

def main(zip_file, k, chars):
    print("Running brute force...")
    with ZipFile(zip_file) as zf:
        start = time()
        password = brute_force(zf, chars, max_length=k)
        end = time()
    print(f"Password: {password}")
    print(f"Total time: {end-start:.3f} seconds")

def brute_force(zf, chars, max_length=4):
    for length in range(1, max_length + 1):
        print(f"Trying password with {length} characters")
        for password in password_generator(chars, length):
            if extract(zf, password):
                return password
    return "Not found"

def password_generator(chars, length):
    if not chars:
        chars = string.digits + string.ascii_letters # "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for combination in itertools.product(chars, repeat=length):
        yield "".join(combination)

def extract(zf, password):
    try:
        zf.extractall(pwd = bytes(password, "utf-8"))
        return True
    except (RuntimeError, BadZipFile) as e:
        return False

if __name__ == "__main__":
    main(args.zip, args.k, args.chars)
