import sys
from PIL import Image
import numpy as np

def convert_image(img, x, y): 
    chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
 
    if len(sys.argv) < 1:
        print( 'Error: Missing Arguments' )
        return

    WCF = 7/4
 
    S = (x, y)
    img = np.sum( np.asarray( img.resize(S) ), axis=2)
    img -= img.min()
    img = (1.0 - img/img.max())*(chars.size-1)
 
    data = ( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )
    return data
