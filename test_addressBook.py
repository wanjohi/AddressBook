import pytest
import random
import string
import csv
from addressBook import AddressBook


@pytest.fixture(scope="module")
def new_address_book():
    """
    Set up a data for our test suite. For now, I'm simply using the actual data.
    :return:
    """
    return AddressBook("MOCK_DATA.csv")


def test_valid_csv():
    """
    Make sure only a valid csv file is allow
    :return:
    """
    with pytest.raises(ValueError):
        AddressBook('blahblah')

def test_name_validator(new_address_book):
    """
    Make sure the name validator only allow alpha numeric
    :return:
    """
    assert new_address_book.name_validator("onlylettersinthis")

    assert not new_address_book.name_validator("letters and spaces")

    assert not new_address_book.name_validator("letterswithdigits111")

    assert not new_address_book.name_validator("letterswithpunctuation.")

    assert not new_address_book.name_validator("special-name")

    assert not new_address_book.name_validator("")

    # Test max 256 characters
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=300))
    assert not new_address_book.name_validator(random_string)

def test_email_validator(new_address_book):
    """
    Make sure the email validator only allows valid emails
    :return:
    """

    assert new_address_book.email_validator("test@test.com")

    assert not new_address_book.email_validator("@test.com")

    assert not new_address_book.email_validator("test@")

    assert not new_address_book.email_validator("test@test")

    assert not new_address_book.email_validator("test@test.com.")

def test_postal_validator(new_address_book):
    """
    Make sure the postal validator only allows canadian postal codes
    :param new_address_book:
    :return:
    """

    assert new_address_book.postal_validator("1VN 4GN")

    assert not new_address_book.postal_validator("1VN4 4GN")

    assert not new_address_book.postal_validator("1VN 4GNE")

    assert not new_address_book.postal_validator("1V 4GN")

    assert not new_address_book.postal_validator("1VN 4N")

    assert not new_address_book.postal_validator("")

    assert not new_address_book.postal_validator("1VN44GN")

def test_database_import(new_address_book):
    """
    Make sure data is getting into our sql database by looping through our Mock data and making sure it's in the db
    :param new_address_book:
    :return:
    """

    with open("MOCK_DATA.csv", newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')

        skip_first_row = True

        for row in reader:
            if skip_first_row:
                skip_first_row = False;
                continue

            new_address_book.cursor.execute("SELECT * FROM contacts WHERE first_name=? AND last_name=?", (row[0],row[1],))
            print(row[0],row[1])
            assert new_address_book.cursor.fetchone()

def test_duplicate_finder(new_address_book, capsys):
    """
    Make sure all our mock data is listed when duplicates are requested
    :param new_address_book:
    :return:
    """
    new_address_book.get_duplicates()

    captured = capsys.readouterr()

    assert "Maximum match count: 9" in captured.out

