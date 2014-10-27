from PIL import Image
import urllib, cStringIO

def convert_image(img, x, y): 
    color = ' .,:;irsXA253hMHGS#9B&@'
 
    img = img.resize((x, y))
    pixel = img.load()

    string = ""    
    for h in xrange(y):
        for w in xrange(x):
            rgb = pixel[w, h]
            string += color[int(sum(rgb) / 3.0 / 256.0 * 23)]
        string += "\n"

    #S = (x, y)
    #img = np.sum( np.asarray( img.resize(S) ), axis=2)
    #img -= img.min()
    #img = (1.0 - img/img.max())*(chars.size-1)
 
    #data = ( "\n".join( ("".join(r) for r in chars[img.astype(int)]) ) )
    return string

def open_url(URL):
    try:
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img = Image.open(file)
        return img
    except:
        print('Error: Failed to open image at ', URL)
        return
