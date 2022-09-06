import requests
from .auth_details import user_auth_details
from .endpoints import *


def update_image_data():
    image_list = []
    response_received = requests.get(parent_endpoint+image_list_endpoint, auth = user_auth_details)
    
    for image in response_received.json():
        resource_tuple = (image['name'], image['name'])
        image_list.append(resource_tuple)

    return image_list
        
def update_flavor_data():
    flavor_list = []
    response_received = requests.get(parent_endpoint+flavor_list_endpoint, auth = user_auth_details)

    for flavor in response_received.json():
        resource_tuple = (flavor['name'], flavor['name'])
        flavor_list.append(resource_tuple)
    
    return flavor_list
