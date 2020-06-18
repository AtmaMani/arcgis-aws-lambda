import json
import os
from ago_connect import create_gis_connection
from reverse_geocode_ip import reverse_geocode
from add_request_point import add_request_point
import requests
from datetime import datetime

def lambda_handler(event, context):
    # get GIS instance
    gis = create_gis_connection(client_id = os.environ['client_id'], 
                                client_secret = os.environ['client_secret'])
    print('Connected to AGO')
    
    # reverse geocode IP Address
    ip_address = event['requestContext']['http']['sourceIp']
    user_agent = event['requestContext']['http']['userAgent']
    request_time = datetime.now()
    address_json = reverse_geocode(ip_address, api_key=os.environ['ipstack_key'])
    print('Reverse geocoded IP')
    
    # edit the feature layer
    item_id = os.environ['ago_item_id']
    edit_result = add_request_point(gis, item_id, address_json, ip_address, user_agent, request_time)
    print(edit_result)
    
    return_html = '<html><head>Lambda to ArcGIS Map - Success</head>' \
                    '<body><p>Thank you for running the lambda function. This is an example of running the ArcGIS API for Python on 3rd party clouds such as AWS</p>' \
                    f'<p>Your IP-address is {ip_address}</p>' \
                    '<p>Below is a map of all similar requests to this lambda function</p>' \
                    '<p>If this does not render well, you can visit it here: <a href="https://arcg.is/vibPe">https://arcg.is/vibPe</a> </p>' \
                    '<style>.embed-container {position: relative; padding-bottom: 80%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><iframe width="500" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="Lambda requests on a map" src="//geosaurus.maps.arcgis.com/apps/Embed/index.html?webmap=8df836df4d544067b715c296608beea4&extent=-135.3586,-45.4831,85.4226,69.1509&home=true&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=dark"></iframe></div>' \
                    '</body></html>'
    
    return {
        'statusCode': 200,
        # 'body': json.dumps('Map url: https://arcg.is/1SLSqe')
        'body':return_html,
        'headers':{'Content-Type':'text/html'}
    }
