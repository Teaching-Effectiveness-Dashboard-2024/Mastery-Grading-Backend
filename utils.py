from canvasapi import Canvas

def GetCanvasUser(api_token):
    API_URL = "https://sjsu.instructure.com/"
    return Canvas(API_URL, api_token)
