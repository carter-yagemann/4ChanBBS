from PIL import Image
import numpy as np
import urllib, cStringIO

def convert_image(img, x, y): 
    chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
 
    S = (x, y)
    img = np.sum( np.asarray( img.resize(S) ), axis=2)
    img -= img.min()
    img = (1.0 - img/img.max())*(chars.size-1)
 
    data = ( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )
    return data

def open_url(URL):
    try:
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img = Image.open(file)
        return img
    except:
        print('Error: Failed to open image at ', URL)
        return
