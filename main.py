import argparse
from zipfile import ZipFile, BadZipFile

parser = argparse.ArgumentParser(description="Unzips a password protected .zip", usage="main.py -z easy.zip")
parser.add_argument("-z", "--zip", metavar="", required=True, help="Location and the name of the .zip file.")
args = parser.parse_args()

RANGE_PASSWORD = 10000

def main(zip_file):
    with ZipFile(zip_file) as zf:
        zf.printdir()
        for password in range(RANGE_PASSWORD):
            if extract(zf, password=f"{password:04}"):
                print(f"File extracted with: {password}")
                break

def extract(zf, password):
    try:
        zf.extractall(pwd = bytes(password, "utf-8"))
        return True
    except (RuntimeError, BadZipFile) as e:
        pass

if __name__ == "__main__":
    main(args.zip)
