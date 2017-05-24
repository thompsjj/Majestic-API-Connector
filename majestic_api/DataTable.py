# uses python 3

import re


class DataTable:
    """ This constructs a new instance of the DataTable module. The DataTable stores a parsing of the data. Row 0
     contains the headers. """

    def __init__(self):
        self.name = ''
        self.headers = []
        self.params = {}
        self.rows = []

    def set_table_name(self, name):

        """ Set table's name.
         :parameter: name (str)
         """

        self.name = name

    def set_table_headers(self, headers):

        """ Set table's headers.    
         :parameter: headers (str)
         """

        self.headers = self.__split(headers)

    def set_table_params(self, name, value):

        """ Set table's parameters.
         
         :parameter: name (str)
         :parameter: value (str)
         """

        self.params[name] = value

    def set_table_row(self, row):

        """ Set table's rows. Stores in an indexed hash.
         :parameter: row (str)  
         """

        rows_hash = {}
        elements = self.__split(row)
        for index, element in enumerate(elements):
            if element is ' ':
                element = ''
            rows_hash[self.headers[index]] = element;
        self.rows.append(rows_hash)

    def __split(self, value):

        """ Set table's rows. Stores in an indexed hash.
         :parameter: value (str)
         :returns: array (list)
         """

        regex = re.compile('(?<!\|)\|(?!\|)')
        array = regex.split(value)

        for index, item in enumerate(array):
            array[index] = item.replace('||', '|')
        return array

    def get_param_for_name(self, name):

        """ Returns a table's parameter for a given name.
         :parameter: name (str)
         :returns: value (str)
         """

        if name in self.params:

            return self.params[name]
        return None

    def get_row_count(self):
        """ Returns the number of rows in the table
         :returns: len rows (int)
         """

        return len(self.rows)