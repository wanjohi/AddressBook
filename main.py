import sys
from AddressBook import AddressBook

def main():
    if len(sys.argv) != 2:
        print("Wrong Usage!")
        print("Correct Usage: python main.py /path/to/csv/file")
        return 0

    address_book = AddressBook(sys.argv[1])

    address_book.get_duplicate()



if __name__ == "__main__":
    main()