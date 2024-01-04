import numpy as np
import potrace
import cv2
from PIL import Image

import sys
import traceback

def get_contours(filename, nudge = .33):
    
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    median = max(10, min(245, np.median(gray)))
    lower = int(max(0, (1 - nudge) * median))
    upper = int(min(255, (1 + nudge) * median))
    filtered = cv2.bilateralFilter(gray, 5, 50, 50)
    edges = cv2.Canny(filtered, lower, upper, L2gradient = True)
    return edges[::-1]

def get_trace(data):
    
    data_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(data_rgb)

    bmp = potrace.Bitmap(im)
    bmp.invert()
    path = bmp.trace(2, potrace.POTRACE_TURNPOLICY_MINORITY, 1, True, 0.5)
    return path

def get_latex(filename):
    
    print('[DEBUG] parsing image...')
    latex = []
    path = get_trace(get_contours(filename))

    print(f'[DEBUG] {len(path.curves)} curves generated from image...')

    for curve in path.curves:
        
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0, y0 = start.x, start.y
            if segment.is_corner:
                x1, y1 = segment.c.x, segment.c.y
                x2, y2 = segment.end_point.x, segment.end_point.y
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1))
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2))
            else:
                x1, y1 = segment.c1.x, segment.c1.y
                x2, y2 = segment.c2.x, segment.c2.y
                x3, y3 = segment.end_point.x, segment.end_point.y
                latex.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            start = segment.end_point

    return latex

def get_expressions(filename):

    exprid = 0
    log = []
    with open('out-' + filename.split('.')[0] + '.txt', 'w') as f:
        for expr in get_latex(filename):

            exprid += 1
            log.append(expr)

        l = len(log)
        
        print('[DEBUG] writing txt file "out-' + filename.split('.')[0] + '.txt"')
        print(f'[DEBUG] {l} segments in total...')

        for i in range(l):
            log[i] = log[i].replace(' ', '').replace('.000000', '').replace('.500000', '.5').replace('.250000', '.25').replace('.125000', '.125')

            if i == l-1:
                f.write(log[i])
            else:
                f.write(log[i] + ',')


if __name__ == '__main__':

    try:
        file = input('enter image name: ')
        get_expressions(file)
        print('Success!')
        
    except cv2.error as e:
        print('Full error traceback:\n')
        traceback.print_exc()
        sys.exit(2)
