# Uses python 3

import sys
import urllib
from . import Response
from .Response import *


class APIService:
    """ This constructs a new instance of the APIService module. 'application_id' is the unique identifier for your
     application - for api requests, this is your "api key" ... for OpenApp request, this is your "private key".
     'end_point' is required and must point to the url you wish to target; ie: enterprise or developer.
     E.g. api_service = ApiService.new('ABC123MYAPIKEY', 'https://developer.majestic.com/api_command'); 
    """

    def __init__(self, application_id, end_point):
        self.application_id = application_id
        self.end_point = end_point

    def execute_command(self, name, parameters):
        """ 
        This method will execute the specified command as an api request.
        
        :parameter: name (str) the name of the command you wish to execute, e.g. GetIndexItemInfo
        :parameter: parameters (dict (str)) is a hash containing the command parameters.
        """
        parameters['app_api_key'] = self.application_id
        parameters['cmd'] = name
        return self.execute_request(parameters)

    def execute_openapp_request(self, command_name, parameters, access_token):
        """ 
        This will execute the specified command as an OpenApp request.
        
        :parameter: command_name (str) the name of the command you wish to execute, e.g. GetIndexItemInfo
        :parameter: parameters (dict (str)) is a hash containing the command parameters.
        :parameter: access_token (str) the token provided by the user to access resources.
        """
        parameters['accesstoken'] = access_token
        parameters['cmd'] = command_name
        parameters['privatekey'] = self.application_id
        return self.execute_request(parameters)

    def execute_request(self, parameters, timeout=10):
        """ 
        This will execute the specified command as an python.urllib request.

        :parameter: command_name (str) the name of the command you wish to execute, e.g. GetIndexItemInfo
        :parameter: parameters (dict (str)) is a hash containing the command parameters.
        :parameter: timeout (str) default time (10 s) to wait before triggering a timeout error.
        """

        data = urllib.parse.urlencode(parameters)
        binary_data = data.encode('ascii')
        request = urllib.request.Request(self.end_point, data=binary_data)
        response = urllib.request.urlopen(request, timeout=timeout)

        try:
            return Response(response)
        except Exception as e:
            print("An exception occurred during API connection: {}".format(e))
            return Response(None, 'ConnectionError', sys.exc_info()[0])
        finally:
            response.close()
