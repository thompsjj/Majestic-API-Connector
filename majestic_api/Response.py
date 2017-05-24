# Response.py
# uses python 3


from xml.sax import handler
from xml.sax import make_parser
from . import DataTable
from .DataTable import *


class Response:
    """ 
    Constructs a new instance of the Response module. 
    The 'code' and 'error_message' parameters will default to None if not provided. 
    """

    def __init__(self, response, code=None, error_message=None):
        self.attributes = {}
        self.params = {}
        self.tables = {}

        if response is not None:

            handler = Handler(self)
            parser = make_parser()
            parser.setContentHandler(handler)
            # print response.read()
            parser.parse(response)

        if (code is not None) and (error_message is not None):

            self.attributes['Code'] = code
            self.attributes['ErrorMessage'] = error_message
            self.attributes['FullError'] = error_message

    def is_ok(self):
        """ Indicates whether the response is ok """

        return self.get_code() in {'OK', 'QueuedForProcessing'}

    def get_code(self):
        """ 
        Returns the Response's message code - 'OK' represents predicted state, all else represents an error. 
        :returns: code (str)
        """
        return self.attributes['Code']

    def get_error_message(self):
        """ 
        Returns the error message(if present) from the Response
        :returns: error message (str)
        """
        return self.attributes['ErrorMessage']

    def get_full_error(self):
        """ 
        Returns the full error message(if present) from the Response
        :returns: error message (str
        """

        return self.attributes['FullError']

    def get_param_for_name(self, name):
        """
        Returns a specific parameter from the Response's parameters.
        :parameter: name (str)
        """

        if name in self.params:
            return self.params[name]
        return None

    def get_table_for_name(self, name):
        """ 
        Returns a specific DataTable object from the Response's data tables.
        :parameter: name (str)
        """

        if name in self.tables:
            return self.tables[name]
        return DataTable()


class Handler(handler.ContentHandler):
    """ Constructs a SAX handler for Majestic SEO's API data """

    def __init__(self, response):
        handler.ContentHandler.__init__(self)
        self.response = response
        self.data_table = None
        self.is_row = False
        self.row = ''

    def startElement(self, name, attrs):
        """ Overload: Parses the start element
         :parameter: name (str)
         :parameter: attrs (object)
         """

        if name == 'Result':

            for attr_name in attrs.getNames():
                self.response.attributes[attr_name] = attrs.getValue(attr_name)

        if name == 'GlobalVars':

            for attr_name in attrs.getNames():
                self.response.params[attr_name] = attrs.getValue(attr_name)

        if name == 'DataTable':

            self.data_table = DataTable()
            self.data_table.set_table_name(attrs.getValue('Name'))
            self.data_table.set_table_headers(attrs.getValue('Headers'))
            for attr_name in attrs.getNames():

                if ('Name' != attr_name) and ('Headers' != attr_name):

                    self.data_table.set_table_params(attr_name, attrs.getValue(attr_name))
            self.response.tables[self.data_table.name] = self.data_table

        if name == 'Row':

            self.is_row = True

    def characters(self, chrs):
        """ Parses the data within the elements
        
         :parameter: chrs (str)
         """

        if self.is_row:

            self.row += chrs

    def endElement(self, name):

        """ Parses the end element 
        
        :parameter: chrs (name)
        """

        if 'Row' == name:

            self.data_table.set_table_row(self.row)
            self.is_row = False
            self.row = ''