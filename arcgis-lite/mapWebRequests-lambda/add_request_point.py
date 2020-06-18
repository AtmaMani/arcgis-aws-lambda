# add_request_point.py
from arcgis.features import Feature, FeatureSet
from arcgis.geometry import Point
from copy import deepcopy

def add_request_point(gis, item_id, address_json, ip_address, user_agent, request_time):
    # get feature layer to edit
    layer_item = gis.content.get(item_id)
    feature_layer = layer_item.layers[0]
    
    # compose a Point object
    pt = Point({'x':address_json['longitude'], 
                'y':address_json['latitude'],
                'spatialReference':{'wkid':4326}
                })
    
    # compose a Feature object
    request_attributes = {'ip_address':ip_address,
                          'user_agent':user_agent,
                          'request_address': f"{address_json['city']}, {address_json['region_name']}, {address_json['country_name']}, {address_json['zip']}",
                          'request_time2':request_time.timestamp()*1000
                         }
    
    ft = Feature(geometry=pt, attributes=request_attributes)
    
    # Edit the feature layer
    edit_result = feature_layer.edit_features(adds=[ft])
    return edit_result