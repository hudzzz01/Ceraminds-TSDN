import matplotlib.pyplot as plt
import cv2
import myLevenshtein

def bacaGambar(imgPath):
    print("membaca text dari gambar")
    try:
        from PIL import Image, ImageEnhance, ImageDraw
    except ImportError:
        import Image, ImageEnhance, ImageDraw
    
    img_file = ""+imgPath
    img = Image.open(img_file)
    #img.show()

    from pylab import rcParams
    # import numpy library
    import numpy as np

    # define the path
    path = img_file

    # read the image
    img = cv2.imread(path, 0)

    # histogram equalization
    equ = cv2.equalizeHist(img)
    # Gaussian blur
    blur = cv2.GaussianBlur(equ, (5, 5), 1)
    # manual thresholding
    th2 = 85 # this threshold might vary!
    equ[equ>=th2] = 255
    equ[equ<th2]  = 0

    #cv2.imshow('Equalized Image', equ)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    import easyocr
    reader = easyocr.Reader(['id','en'])

    bounds = reader.readtext(img)
    text = []
    for i in range(len(bounds)):
        text.append(bounds[i][-2])

    #print(text)

    rcParams['figure.figsize'] = 8, 16
    output = reader.readtext(equ)
    
    

    for i in range(len(output)):
        print(output[i][-2])
        
    #print(output)
    found = False
    smilar = myLevenshtein.cekSmilar(text)
    #masuke levenstein
    if len(smilar) > 1 :
        found = True
    
    return {
        'found': found,
        'text-smilar-data-pribadi' : smilar,
        'box' : output
    }


