import numpy as np
import urllib.request 
import io  
from PIL import Image, ImageDraw

tweet_user_image = "https://pm1.narvii.com/6796/e227b6ba84cdc3772b24da658fe3561471ea6a91v2_00.jpg"

def crop_image(url):
    # Open the input image as numpy array, convert to RGB
    img=Image.open(io.BytesIO(urllib.request.urlopen(url).read())).convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    image = Image.fromarray(npImage)
    mode = image.mode
    size = image.size
    data = image.tobytes()
    return mode, size, data
