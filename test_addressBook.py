import pytest
import random
import string
from addressBook import AddressBook


@pytest.fixture(scope="module")
def new_address_book():
    """
    Set up a data for our test suite. For now, I'm simply using the actual data.
    :return:
    """
    return AddressBook("ca-500.csv")


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

    # Test no spaces
    assert not new_address_book.name_validator("letters and spaces")

    # Test no digits
    assert not new_address_book.name_validator("letterswithdigits111")

    # Test no punctuations
    assert not new_address_book.name_validator("letterswithpunctuation.")

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
