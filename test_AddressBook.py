import pytest
import random
import string
from AddressBook import AddressBook

def test_valid_csv():
    """
    Make sure only a valid csv file is allow
    :return:
    """
    with pytest.raises(ValueError):
        AddressBook('blahblah')

def test_name_validator():
    """
    Make sure the name validator only allow alpha numeric
    :return:
    """
    assert AddressBook.name_validator("onlylettersinthis")

    # Test no spaces
    with pytest.raises(ValueError):
        AddressBook.name_validator("letters and spaces")

    # Test no digits
    with pytest.raises(ValueError):
        AddressBook.name_validator("letterswithdigits111")

    # Test no punctuations
    with pytest.raises(ValueError):
        AddressBook.name_validator("letterswithpunctuation.")

    # Test max 256 characters
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=300))
    with pytest.raises(ValueError):
        AddressBook.name_validator(random_string)

def test_email_validator():
    """
    Make sure the email validator only allows valid emails
    :return:
    """

    assert AddressBook.email_validator("test@test.com")

    with pytest.raises(ValueError):
        AddressBook.email_validator("@test.com")

    with pytest.raises(ValueError):
        AddressBook.email_validator("test@")

    with pytest.raises(ValueError):
        AddressBook.email_validator("test@test")

    with pytest.raises(ValueError):
        AddressBook.email_validator("test@test.com.com")