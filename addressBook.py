import sys
import os.path
import sqlite3
import csv
import re

class AddressBook:
    """
    This class handles connections to sqllite, and all commands to necessary for the address book
    """
    def __init__(self, csv_file_path):

        # Make sure the file exists
        if not os.path.isfile(csv_file_path):
            raise ValueError("CSV file does not exist!")

        # RAM based db
        self.init_db()

        # Parse csv file
        self.csv_file_parsing(csv_file_path)



    def init_db(self):
        """
        This method initializes a in memory sqllite database and create a table to hold our data
        :return: None
        """
        self.sqldb = sqlite3.connect(":memory:")
        self.cursor = self.sqldb.cursor()

        # Create table
        self.cursor.execute('''CREATE TABLE contacts
             (first_name text, 
             last_name text,
             company_name text,
             address text, 
             city text,
             province text,
             postal text,
             email text, 
             phone1 text, 
             phone2 text,
             web text)''')

        self.sqldb.commit()



    def csv_file_parsing(self,csv_file_path):
        """
        This method parses the csv file provided and stores it in the sqllite database
        :param csv_file_path: PATH to csv file
        :return: None
        """

        number_of_records = 0
        first_row = True
        header_row = None

        with open(csv_file_path, newline='') as csv_file:
            address_reader = csv.reader(csv_file, delimiter=',')

            for row in address_reader:
                # Collect header names
                if first_row:
                    first_row = False
                    header_row = row
                    continue

                # Loop through each row and parse out the contacts
                if self.contact_parser(header_row, row):
                    number_of_records +=1
                else:
                    print("Invalid or Duplicate data Found! Rejected Row:")
                    print(row, "\n", "\n")

            print("Number of users successfully imported:", number_of_records)



    def contact_parser(self, header_row, row):
        """
        This function takes a csv row and turns into into a contact
        :param header_row: header names
        :param row: contact details
        :return: None
        """
        contact = {}
        for index, value in enumerate(row):
            if header_row[index] == "first_name" or header_row[index] == "last_name":
                if not self.name_validator(value):
                    # Invalid name
                    return False

                contact.update({header_row[index]: value})

            elif header_row[index] == "email":
                if not self.email_validator(value):
                    # Invalid email
                    return False

                contact.update({header_row[index]: value})

            elif header_row[index] == "postal":
                if not self.postal_validator(value):
                    # Invalid postal code
                    return False

                contact.update({header_row[index]: value})

            else:
                # All other data points without special validator
                if len(value) > 256:
                    # Too many characters
                    return False

                contact.update({header_row[index]: value})

        # Insert into database
        self.cursor.execute('INSERT INTO contacts (first_name, last_name,company_name, address,'
                            ' city,province, postal, phone1, phone2, email, web) VALUES (?,?,?,?,?,?,?,?,?,?,?);',
                            (contact['first_name'], contact['last_name'], contact['company_name'], contact['address'],
                             contact['city'], contact['province'], contact['postal'], contact['phone1'],
                             contact['phone2'], contact['email'], contact['web'],))
        self.sqldb.commit()

        return True



    def name_validator(self, str):
        """
        Validate the name string, raise error if invalid, else return True
        :param str: String to test
        :return: Boolean
        """
        # Length limit and alphanumeric checker
        if len(str) > 256 or len(str) < 1 or not str.isalpha():
            return False

        # Valid name
        return True



    def email_validator(self, str):
        """
        Validate the email string, raise error if invalid, else return True
        :param str: String to test
        :return: Boolean
        """
        # Length limit checker
        if len(str) > 256 or len(str) < 1:
            return False

        # Valid email checker
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9_-]+\.[a-zA-Z]+$", str):
            return False

        # Check if email is in database
        sql_email_check = 'SELECT email FROM contacts WHERE email = \'' + str + '\''
        self.cursor.execute(sql_email_check)

        if self.cursor.fetchone():
            return False

        # Valid email
        return True


    def postal_validator(self,str):
        """
        Validate the postal code
        :param str: String to test
        :return: Boolean
        """
        # Valid postal code checker
        if not re.match(r"^[a-zA-Z0-9]{3} [a-zA-Z0-9]{3}$", str):
            return False

        # Valid postal code
        return True



    def get_duplicates(self):
        """
        This function performs an SQL select of duplicate data from each column then combines the results, orders them
        in descending order and takes the first result.
        Because I could not ask what specific fields to find duplicates for, the function has been written to allow
        changing what columns we can search duplicates for. Simply comment out the 'sql_fields' you dont want to find
        duplicates for.
        :return: SQL result
        """

        sql_fields = []

        # Duplicate first_name
        sql_fields.append('SELECT first_name as value, COUNT(*) as count, \'first_name\' as column FROM contacts GROUP BY' \
                         '  first_name HAVING COUNT(*) > 1')

        # Duplicate last_name
        sql_fields.append('SELECT last_name as value, COUNT(*) as count, \'last_name\' as column FROM contacts GROUP BY' \
                        '  last_name HAVING COUNT(*) > 1')

        # Duplicate company_name
        sql_fields.append('SELECT company_name as value, COUNT(*) as count, \'company_name\' as column FROM contacts ' \
                           'GROUP BY  company_name HAVING COUNT(*) > 1')

        # Duplicate address
        sql_fields.append('SELECT address as value, COUNT(*) as count, \'address\' as column FROM contacts ' \
                           'GROUP BY  address HAVING COUNT(*) > 1')

        # Duplicate city
        sql_fields.append('SELECT city as value, COUNT(*) as count, \'city\' as column FROM contacts ' \
                           'GROUP BY  city HAVING COUNT(*) > 1')

        # Duplicate province
        sql_fields.append('SELECT province as value, COUNT(*) as count, \'province\' as column FROM contacts ' \
                           'GROUP BY  province HAVING COUNT(*) > 1')

        # Duplicate postal
        sql_fields.append('SELECT postal as value, COUNT(*) as count, \'postal\' as column FROM contacts ' \
                           'GROUP BY  postal HAVING COUNT(*) > 1')

        # Duplicate phone 1
        sql_fields.append('SELECT phone1 as value, COUNT(*) as count, \'phone1\' as column FROM contacts ' \
                           'GROUP BY  phone1 HAVING COUNT(*) > 1')

        # Duplicate phone 2
        sql_fields.append('SELECT phone2 as value, COUNT(*) as count, \'phone2\' as column FROM contacts ' \
                           'GROUP BY  phone2 HAVING COUNT(*) > 1')

        # Duplicate email
        sql_fields.append('SELECT email as value, COUNT(*) as count, \'email\' as column FROM contacts ' \
                           'GROUP BY  email HAVING COUNT(*) > 1')

        # Duplicate web
        sql_fields.append('SELECT web as value, COUNT(*) as count, \'web\' as column FROM contacts ' \
                           'GROUP BY  web HAVING COUNT(*) > 1')

        # Atleast one field has to be in the final sql statement
        sql = sql_fields[0]

        # Add all the other fields that havent been commented out
        for sql_field in sql_fields[1:]:
            sql = sql + ' UNION ' + sql_field

        # Get the highest count value
        sql = 'SELECT * FROM (' + sql +') ORDER BY count DESC LIMIT 1'

        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        print("Maximum match count:", result[1])

        # Get all the contacts that are part of the max group
        group_sql = 'SELECT last_name, first_name, email FROM contacts WHERE ' + result[2] + '=\'' + result[0] + '\''

        for row in self.cursor.execute(group_sql):
            print(row[0],',',row[1],'at', row[2])







def main():
    if len(sys.argv) != 2:
        print("Wrong Usage!")
        print("Correct Usage: python main.py /path/to/csv/file")
        return 0

    address_book = AddressBook(sys.argv[1])

    address_book.get_duplicates()



if __name__ == "__main__":
    main()