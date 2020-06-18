# reverse_geocode_ip.py
import requests
import os

def reverse_geocode(ip, api_key):
    request_url = f'http://api.ipstack.com/{ip}'
    r = requests.get(request_url, params={'access_key':api_key})
    
    return r.json()