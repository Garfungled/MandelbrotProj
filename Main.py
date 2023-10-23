##### Imports #####
from __future__ import print_function
import MandelBrot as MandelBrot
from decimal import Decimal as D
import os.path
import uuid
import time
import math

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

# TODO:
    # Add Shape property request for color and text autosize
    # Possibly use shape placeholder? No idea
        # Create one shape and one shape property request, then make each shape request a placeholder request of the first one?
        # Possibly half request time?
        # Also need property state to be set to inherit for the placeholders?
def shape_request(PAGE_ID: str, SHAPE_ID: str, shape_type: str, size: (float, float), position: (float, float)):
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

def shape_prop_request(SHAPE_ID: str, color: (int, int, int), alpha: float):
    return {
        'updateShapeProperties': {
            'objectId': SHAPE_ID,
            'shapeProperties': {
                'shapeBackgroundFill':{
                    'solidFill':{
                        'color':{
                            'rgbColor':{
                                'red': color[0],
                                'green': color[1],
                                'blue': color[2]
                            },
                        },
                        'alpha': alpha
                    }        
                },
            },
            'fields': "shapeBackgroundFill.solidFill.color"
        }
    }

# TODO: 
    #̶ A̶d̶d̶ c̶o̶m̶p̶l̶e̶x̶ n̶u̶m̶b̶e̶r̶ t̶e̶x̶t̶
    # Add complex number coloring according to iterations
        # To this by: creating a gradient function
def shape_request_arr(dimension: int, complex_numbers, with_text: bool, color: (int, int, int), color_alpha: float):
    # Request Arrays
    shapes = []
    shape_props = []
    texts = []
    
    
    for i in range(dimension):
        for j in range(dimension):
            complex_number = complex_numbers[j][i]
            complex_number_string = str(complex_number.real) + ("+" if complex_number.imag >= 0 else "") + str(complex_number.imag) + "i"
            size_x = 10/dimension
            size_y = 5.63/dimension
            shape_id = gen_uiid()
            
            shape = shape_request(PAGE_ID, shape_id, "RECTANGLE", (size_x, size_y), (i * size_x, j * size_y))
            shape_prop = shape_prop_request(shape_id, color, color_alpha)
            shapes.append(shape)
            shape_props.append(shape_prop)
            
            if with_text:
                texts.append({'insertText': {'objectId': shape_id, 'text': complex_number_string}})
            
    return shapes, shape_props, texts


##### Main Function #####
if __name__ == '__main__':
    ##### Inputs #####
    complex_dimension = int(input("Input a dimension for the square (must be a single integer greater than or equal to 1): "))
    step = D(input("Input a step for the Mandelbrot function (positive real number): "))
    max_iterations = int(input("Input a max iteration for the Mandelbrot function (a positive integer): "))
    
    shape_dimension = math.ceil(complex_dimension/step) * 2 + math.ceil(complex_dimension/step) % 2
    
    ##### Credential init #####
    print("Creating Credentials...")
    
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

        # Mandelbrot implementation
        print("Creating Mandelbrot set...")
        complex_nums, iterations, magnitudes = MandelBrot.getMandelSet(complex_dimension, step, max_iterations) 
        
        shapes, shape_props, texts = shape_request_arr(shape_dimension, complex_nums, False, (0, 0, 1), 1)
        
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
        # TODO:
            # Make it more effective
                # Find a way to bypass the google api request limit
                # Increase quota?
                # Make the requests inexpensive
                    # Expensive read requests are 60 per minute while inexpensive are 600
        """About the time.sleep: 
            Google API requesting is limited to 60 per minute, this includes body requests, meaning I can't split the whole request into
            smaller sizes of requests. So in order to work around this, there is a second wait between each request. This is really bad
            and inefficient however. This means a grid of size 100 will take about 166 minutes, or 2.7 hours. And thats just creating the grid, 
            we also need to create the texts for each grid, so that doubles it, taking about 5.4 hours total. 
                I'll see what I can do to try and make it more effective.
        """
        
        print("Adding google slide...")
        response = service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body={'requests': slide_requests}).execute()
        print("\tSlide Request Done!")
        time.sleep(1)
        
        print("Adding shapes, their properties, and texts...")
        requests = shapes + shape_props + texts
        for request in requests:
            response = service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body={'requests': request}).execute()
            time.sleep(1)
            print(f"\tRequest {requests.index(request) + 1} done!")
            
        print("Done!")
        
    except HttpError as error:
        print(f"An error has occurred: {error}")
        print("Slides not created as a result of the error")
    