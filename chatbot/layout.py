#!/usr/bin/env python3
# coding: utf-8

'''
Provides functions to handle layout definitions, typically from JSON files.

External dependencies, to be installed e.g. via pip:
- Pillow v4
- numpy v1.15

Author: Luis A. Leiva <luis.leiva@aalto.fi>
'''

import sys
import os
import json
import math
import random
import numpy as np
from PIL import Image, ImageDraw


# This constant determines the output image size.
# TODO: It's more convenient to work with `IMAGE_SHAPE`,
# in order to avoid having to specify in different parts of the code
# whether the image was grayscaled (1 channel) or not (3 channels).
IMAGE_SIZE = (200, 200)


def memoize(f):
    memo = {}
    def helper(x):
        h = str(x.__repr__)
        if h not in memo:
            memo[h] = f(x)
        return memo[h]
    return helper


def update_element(elem):
    '''
    Recompute standard properties.
    '''
    elem['x'] = elem['x0']
    elem['y'] = elem['y0']
    elem['width'] = elem['x1'] - elem['x0']
    elem['height'] = elem['y1'] - elem['y0']


def scale_layout(layout, factor=1.0):
    '''
    Scale layout by a given factor.
    '''
    for elem in layout:
        elem['x0'] *= factor
        elem['y0'] *= factor
        elem['x1'] *= factor
        elem['y1'] *= factor
        update_element(elem)
    return layout


def crop_layout(layout):
    '''
    Remove whitespace around layout.
    '''
    xmin, ymin, xmax, ymax = measure_layout(layout)
    for elem in layout:
        elem['x0'] -= xmin
        elem['y0'] -= ymin
        elem['x1'] -= xmin
        elem['y1'] -= ymin
        update_element(elem)
    return layout


def center_layout(layout):
    '''
    Given a layout positioned at (0,0), move all elements to the center of the canvas.
    '''
    xmin, ymin, xmax, ymax = measure_layout(layout)
    # We need the effective area of the canvas.
    for elem in layout:
        elem['x0'] += xmax/2
        elem['y0'] += ymax/2
        elem['x1'] += xmax/2
        elem['y1'] += ymax/2
        update_element(elem)
    return layout


def measure_layout(layout):
    '''
    Return the largest bounding box (xmin, ymin, xmax, ymax) in the layout.
    '''
    layout = ensure_layout_format(layout)

    x0s = [elem['x0'] for elem in layout]
    y0s = [elem['y0'] for elem in layout]
    x1s = [elem['x1'] for elem in layout]
    y1s = [elem['y1'] for elem in layout]

    return min(x0s), min(y0s), max(x1s), max(y1s)


def min_element_size(layout):
    '''
    Compute the minimum size (either width or height) of all layout elements.
    This function comes in handy to warn about elements being too small,
    which can be an issue when training CNNs.
    '''
    layout = ensure_layout_format(layout)

    xmin, ymin, xmax, ymax = measure_layout(layout)
    return min(xmin, ymin)


def create_image(layout, resize=True, grayscale=False, fill_color=None, stroke_color=None):
    '''
    Return a PIL image from given layout, which can then e.g. be exported to file or use as raw vector.
    If `fill_color="random"` a different (random) color is applied to each element.
    If `fill_color="random.uniq"` the same (random) color is applied to all elements.
    '''
    layout = ensure_layout_format(layout)

    if fill_color == 'random.uniq':
        fill_color = random_color()

    xmin, ymin, xmax, ymax = measure_layout(layout)
    min_size = (round(xmax-xmin), round(ymax-ymin))
    image = Image.new('RGB', min_size, (255,255,255))
    drawa = ImageDraw.Draw(image)
    for elem in layout:
        bounds = [
            elem['x0'],
            elem['y0'],
            elem['x1'],
            elem['y1'],
        ]
        color = elem['color'] if 'color' in elem else 'gray'
        if fill_color is not None:
            color = fill_color
            if fill_color == 'random':
                color = random_color()
        drawa.rectangle(bounds, fill=color, outline=stroke_color)
    if resize:
        image = image.resize(IMAGE_SIZE, Image.ANTIALIAS)
    if grayscale:
        image = image.convert('L')
    return image


def load(layout):
    '''
    Load layout from string, json file, or dict.
    '''
    # Accept any reasonable format:
    # - stringified json
    # - json file
    # - json object
    if isinstance(layout, str):
        if os.path.isfile(layout):
            with open(layout) as f:
                layout = f.read()
        layout = json.loads(layout)
    return ensure_layout_format(layout)


@memoize
def ensure_layout_format(layout):
    # In principle we can have more than one layout per JSON file,
    # but assume by now that there's only one.
    if 'layouts' in layout:
        layout = layout['layouts'][0]['elements']
    # If an AIM-compliant layout is given, unpack the elements.
    if 'elements' in layout:
        layout = layout['elements']
    # Both Niraj and Morteza use a wrapper (`elementData`) property, so "unpack" it.
    if 'elementData' in layout:
        layout = layout['elementData']

    # Previously, a layout was a dictionary of `{key:element}` entries.
    # Currently, a layout is a list of objects, i.e. `[{elem}, ...]`.
    if isinstance(layout, dict):
        layout = [ensure_element_format(elem) for _, elem in layout.items()]
    elif isinstance(layout, list):
        layout = [ensure_element_format(elem) for elem in layout]
    else:
        raise ValueError('Unsupported layout format: {}'.format(type(layout)))

    return layout


@memoize
def ensure_element_format(elem):
    '''
    Ensure element format (properties and values).
    '''
    if not isinstance(elem, dict):
        raise ValueError('Unsupported element type: {}'.format(type(elem)))

    if 'x0' not in elem:
        # Revise old/new layout format.
        if 'x_position' in elem:
            x, y = elem['x_position'], elem['y_position']
        elif 'x' in elem:
            x, y = elem['x'], elem['y']
        else:
            raise ValueError('Wrong element format or missing properties.')
        # Note: PIL requires actual bounding box coords.
        w, h = elem['width'], elem['height']
        elem.update({
            'x0': x,
            'y0': y,
            'x1': x + w,
            'y1': y + h,
        })

    return elem


def random_color():
    '''
    Generate a random hex color in HTML format.
    '''
    r = lambda: random.randint(0, 255)
    return '#{:02x}{:02x}{:02x}'.format(r(), r(), r())


if __name__== '__main__':
    layout_file = sys.argv[1]
    dat = load(layout_file)
    img = create_image(dat, resize=False)
#    # This is just for testing purposes.
#    img.save('out.png', 'PNG')

    # Another option is to use base64 encoding:
    import base64
    from io import BytesIO
    buffered = BytesIO()
    img.save(buffered, format='PNG')
    img_str = base64.b64encode(buffered.getvalue())
    print(img_str)
