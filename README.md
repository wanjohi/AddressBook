#Statistical Analysis Test Code

##Usage
To run this program, please run the commands below:
```
source venv/bin/activate
python addressBook.py /path/to/csv/file
```

## Test Usage
To execute the pytest attached with program, please run the commands below:
```
source venv/bin/activate
pytest
```
The unit tests use an attach MOCK_DATA.csv file.

##Additional Notes
It was not clear on whether the program should filter for all data points in the csv, or the data points listed in
the example i.e only `first_name` and `last_name`. So I made the code modular. The method `get_duplicates` in
`class AddressBook` can be modified to find duplicates for the fields you want. Simply comment out the 
`sql_fields` that you don't want to filter for.

