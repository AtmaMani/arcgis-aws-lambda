# ago_connect.py
from arcgis.gis import GIS
import requests

def create_gis_connection(client_id, client_secret):
    request_params = {'client_id':client_id,
                        'client_secret':client_secret,
                        'grant_type': 'client_credentials'}

    r = requests.post(url='https://www.arcgis.com/sharing/rest/oauth2/token/', 
                      params = request_params)
    token = r.json()['access_token']
    
    # create GIS instance
    gis = GIS(token=token)
    return gis