##### Imports #####
from __future__ import print_function
import MandelBrot as MandelBrot
import os.path
import uuid
import time

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials


"""
The main program for creating the slides
"""

##### Constants #####
SCOPES = ['https://www.googleapis.com/auth/presentations']
PRESENTATION_ID = "1mgGhGO_qwuOOW2I86mG2h2ymKsm9yFHDCCj8m1HSA4E"
CREDS = None



##### Additional Function #####
# Lambdas
gen_uiid = lambda: str(uuid.uuid4()) # generates random string id
element_size = lambda size: {'magnitude': size * 72, 'unit': 'PT'} # creates size dict from inch

# Funcs
def shape_dict(PAGE_ID: str, SHAPE_ID: str, shape_type: str, size: (float, float), position: (float, float)):
    return {
        'createShape': {
            'objectId': SHAPE_ID,
            'shapeType': shape_type,
            'elementProperties': {
                'pageObjectId': PAGE_ID,
                'size': {
                    'width': element_size(size[0]),
                    'height': element_size(size[1])
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': position[0] * 72,
                    'translateY': position[1] * 72,
                    'unit': 'PT'
                }
            }
        }
    }

# TODO: 
    # Add complex number text
    # Add complex number coloring according to iterations
        # To this by: creating a gradient function
def shape_dict_arr(dimension: int):
    # This set up is not optimal as it is for future additions
    shapes = []
    texts = []
    for i in range(dimension):
        for j in range(dimension):
            size_x = 10/dimension
            size_y = 5.63/dimension
            shape_id = gen_uiid()
            
            shape = shape_dict(PAGE_ID, shape_id, "RECTANGLE", (size_x, size_y), (i * size_x, j * size_y))
            shapes.append(shape)
            
            texts.append({'insertText': {'objectId': shape_id, 'text': f"({j}, {i})"}})
            
    return shapes, texts

# Request Thread Optimization


##### Main Function #####
if __name__ == '__main__':
    
    ##### Credential init #####
    if os.path.exists('token.json'):
        CREDS = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not CREDS or not CREDS.valid:
        if CREDS and CREDS.expired and CREDS.refresh_token:
            CREDS.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            CREDS = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(CREDS.to_json())
    
    
    ##### Editing Presentation #####
    try:
        service = build(serviceName='slides', version='v1', credentials=CREDS)
        
        # Constants
        PAGE_ID = gen_uiid()

        shapes, texts = shape_dict_arr(7)
        
        slide_requests = [
            {
                ##### Slide Creation #####
                'createSlide': {
                    'objectId': PAGE_ID,
                }
            }
            ##### Adding Elements for Slides ##### 
        ]
        
        ##### Execute Slide Creation Request #####
        response = service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body={'requests': slide_requests}).execute()
        
        for request in shapes:
            response = service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body={'requests': request}).execute()
            time.sleep(1)
            
        for request in texts:
            response = service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body={'requests': request}).execute()
            time.sleep(1)
        
    except HttpError as error:
        print(f"An error has occurred: {error}")
        print("Slides not created as a result of the error")
    