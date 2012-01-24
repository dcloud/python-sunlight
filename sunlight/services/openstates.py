# Copyright (C) 2012, Paul Tagliamonte <paultag@sunlightfoundation.com>          
#                                                                                
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in  
# the Software without restriction, including without limitation the rights to   
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies  
# of the Software, and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:                                       
#                                                                                
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.                                
#                                                                                
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
# SOFTWARE.

import sunlight.service
import json

module_name = "openstates"
service_url = "http://openstates.org/api/v1"

class OpenStates(sunlight.service.Service):
    """
    Bindings into the OpenStates project

    API Ref:            http://openstates.org/api/
    About the project:  http://openstates.org/
    """

    def metadata(self, **kwargs):
        """
        Get basic information on a given state.
        """
        return self.get( "metadata", **kwargs )

    def bills(self, **kwargs):
        """
        Get information on a state-level bill
        """
        return self.get( "bills", **kwargs )

    def legislators(self, **kwargs):
        """
        Get information on a state-level legislator
        """
        return self.get( "legislators", **kwargs )

    def committees(self, **kwargs):
        """
        Get information on a state-level committee
        """
        return self.get( "committees", **kwargs )

    def events(self, **kwargs):
        """
        Get information on an event coming up soon (such as a public hearining, 
        or bill vote)
        """
        return self.get( "events" **kwargs )

    def get_url( self, obj, apikey, **kwargs ):
        ret = "%s/%s?apikey=%s" % (
            service_url,
            obj,
            apikey
        )
        for arg in kwargs:
            ret += "&%s=%s" % ( arg, kwargs[arg] )
        return ret

    def decode_response( self, response ):
        return json.loads( response )

    def handle_bad_http_code( self, code ):
        messages = {
            400 : "Error with your request. Perhaps too many results?",
            404 : "Object doesn't exist."
        }
        try:
            return messages[code]
        except KeyError as e:
            return "Unknown error code!!! Recieved a %s from the server." % (
                str( code )
            )
