import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg') 

def parseFile():
    with open('big.dem') as heights:
        li = heights.readlines()
        for i in range(len(li)):
            li[i] = list(map(float, li[i][:-2].split()))
        #Znormalizowanie wysokości
        arr = np.array(li[1:])
        arr = arr - np.amin(arr)
        arr = arr / np.amax(arr)
        return arr, li[0][0], li[0][1], li[0][2]

def hsv2rgb(h, s, v):
    if (s == 0):
        return (v, v, v)
    else:
        h *= 360
        hi = np.floor(h / 60)
        f = (h / 60) - hi
        p = (v * (1 - s))
        q = (v * (1 - (s * f)))
        t = (v * (1 - (s * (1 - f))))
        if (hi == 1):
            return ((q, v, p))
        elif (hi == 2):
            return ((p, v, t))
        elif (hi == 3):
            return ((p, q, v))
        elif (hi == 4):
            return ((t, p, v))
        elif (hi == 5):
            return ((v, p, q))
        else:
            return ((v, t, p))

def gradient_hsv(h, s, v):
    return hsv2rgb(1-((h*0.32)+0.68), s, v)

def generateMap(width, height, coords):
    #Ustawienie kierunku światła
    lightDir = np.array([12.6,19.8,-60.4])
    #Znormalizowanie kierunku światła
    lightDir = lightDir / np.linalg.norm(lightDir)
    img = np.zeros((height, width, 3))
    for i in range(height):
        for j in range(width):
            if (j+1 < width and i+1 < height):
                #Oblicz wektory do sąsiednich punktów
                vecA = np.array((j, i+1, coords[i+1,j])) - np.array((j, i, coords[i,j]))
                vecB = np.array((j+1, i, coords[i,j+1])) - np.array((j, i, coords[i,j]))
                #Oblicz normalną do punktu
                normal = np.cross(vecA, vecB)
                normal = normal / np.linalg.norm(normal)
                #Znajdź kąt między normalną a kierunkiem światła
                angle = np.arccos(np.dot(normal, lightDir))
                angle = np.degrees(angle)
                angle = int(angle) / 10
                angle /= 9.
                if (angle < 0.23):
                    img[i,j] = np.array(gradient_hsv(coords[i,j], 1, 0.8))
                elif (angle < 0.233 and angle >= 0.23):
                    img[i,j] = np.array(gradient_hsv(coords[i,j], 0.9, 0.85))
                elif (angle < 0.236 and angle >= 0.233):
                    img[i,j] = np.array(gradient_hsv(coords[i,j], 0.8, 0.9))
                elif (angle >= 0.236 and angle < 0.26):
                    img[i,j] = np.array(gradient_hsv(coords[i,j], 0.7, 0.95))
                else:  
                    img[i,j] = np.array(gradient_hsv(coords[i,j], 0, 1))
            else:
                img[i,j] = np.array(gradient_hsv(coords[i,j], 1, 0.7))
    img = np.flipud(img)
    return img
    

if __name__ == '__main__':
    mapParams = [0,0,0]
    coords, mapParams[0], mapParams[1], mapParams[2] = parseFile()
    img = generateMap(int(mapParams[0]), int(mapParams[1]), coords)
    fig, ax = plt.subplots()
    r = 1./(mapParams[2]/100.)
    ax.imshow(img, extent=(0, img.shape[1]/r, 0, img.shape[0]/r))
    ax.invert_yaxis()
    ax.tick_params(direction='in')
    ax.set_xticks(range(0,3750,750))
    ax.set_yticks(range(0,3750,750))
    fig.savefig('my-map.pdf')
    