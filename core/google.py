from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        #print('validate google================================')
        try:
            #print('google try==========1=====')
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                #print('google try==========2=====',idinfo)
                return idinfo
            

        except:
            #print('google except========3=======')
            return "The token is either invalid or has expired"