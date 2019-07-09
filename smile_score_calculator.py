import numpy as np
import os
# from PIL import Image
# from PIL import ImageFont
# from PIL import ImageDraw 
import requests 
import json
import secret.API_KEY as API_KEY
from enum import Enum

class Likelihood(Enum):
    UNKNOWN = 0
    VERY_UNLIKELY = 1
    UNLIKELY = 2
    POSSIBLE = 3
    LIKELY = 4
    VERY_LIKELY = 5

class SmileScoreCalculator:

    def __init__(self, image_uri):
        self.image_uri = image_uri
        self.vision_info = None
        self.smile_score = None

    def request_vision_api(self):
        
        API_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate?key=%s" % API_KEY
        post_data = {
          "requests": [
            {
              "features": [
                {
                  "maxResults": 10,
                  "type": "FACE_DETECTION"
                }
              ],
              "image": {
                "source": {
                  "imageUri": self.image_uri
                }
              }
            }
          ]
        }
        post_data_json = json.dumps(post_data)
        r = requests.post(url = API_ENDPOINT, data = post_data_json) 
        response_data = json.loads(r.text) # Returns a dictionary
        self.vision_info = response_data

    def calculate_smile(self):
        face = self.vision_info['responses'][0]['faceAnnotations'][0]      
        moodboard = (
                    Likelihood[str(face['joyLikelihood'])].value, 
                    Likelihood[str(face['sorrowLikelihood'])].value, 
                    Likelihood[str(face['angerLikelihood'])].value, 
                    Likelihood[str(face['surpriseLikelihood'])].value)
        MOODS = ['happy','sorrow','angered','surprised']
        a = np.array([face['landmarks'][10]['position']['x'], face['landmarks'][10]['position']['y'], face['landmarks'][10]['position']['z']])
        b = np.array([face['landmarks'][12]['position']['x'], face['landmarks'][12]['position']['y'], face['landmarks'][12]['position']['z']])
        c = np.array([face['landmarks'][11]['position']['x'], face['landmarks'][11]['position']['y'], face['landmarks'][11]['position']['z']])
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        angle = np.degrees(angle)
        if moodboard[0] == 5:
            print("You are really happy, your smile score is " + str(220-angle))
            caption = "You are really happy!\n Your smile score is " + str(220-angle)
        elif moodboard[0] == 4:
            print("Your are quite happy, your smile score is " + str(210-angle))
            caption = "Your are quite happy\n Your smile score is " + str(210-angle)
        elif moodboard[0] == 3:
            print("Your maybe smiling, score is " + str(200-angle))
            caption = "Your maybe smiling\n Smile score is " + str(200-angle)
        else:
            print(np.argmax(moodboard))
            print(moodboard)
            print("Are you smiling?\n You are more likely to be " + MOODS[np.argmax(moodboard)])
            caption = "Are you smiling?\n You are more likely to be " + MOODS[np.argmax(moodboard)]
        print(self.smile_score)
        return caption


if __name__ == '__main__':
    ssc = SmileScoreCalculator("https://storage.googleapis.com/user_yiling/IMG_8370.jpg")
    ssc.request_vision_api()
    ssc.calculate_smile()