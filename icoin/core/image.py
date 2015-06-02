from io import BytesIO
from PIL import Image
from icoin.util.homer import HOME

#TODO: memoize
def get_image(amount):
    filename = "{}/icoin/static/images/money/{}.png".format(HOME, amount)
    image = Image.open(filename)
    output = BytesIO()
    image.save(output, "PNG")
    output.seek(0)
    return output
    
