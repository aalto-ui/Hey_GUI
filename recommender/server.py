#!/usr/bin/env python
# coding: utf-8

import sys
import json
import os
from random import shuffle
from datetime import datetime
from operator import itemgetter
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

msg = {
    100: 'No input data provided',
    101: 'File not found',
    102: 'File is empty',
    103: 'Property not found in file',
    200: 'OK',
    400: 'No results'
}


def find_by_ui(screen_id, objs=None):
    if objs is None:
        objs = app_categories[:]
    filtered = [] # TODO
    return filtered


def find_by_category(name, objs=None):
    if objs is None:
        objs = app_categories[:]
    # Some categories are multi-word, e.g. "art & design", "music & audio", etc.
    # so let's search for substrings.
    filtered = [row for row in objs if name in row['category']]
    return filtered


def find_by_design(name, objs=None):
    if objs is None:
        objs = app_categories[:]
    # All design topics are single-word, e.g. "login", "camera", etc.
    # so let's do an exact search.
    filtered = [row for row in objs if row['design'] == name]
    return filtered


def ranker(objs, sortby=None, desc=True):
    if not sortby:
        fn = lambda k: ['rating', 'num_ratings', 'num_downloads']
    elif sortby.startswith('rand'):
        shuffle(objs)
        return objs
    else:
        fn = itemgetter(sortby)
    candidates = sorted(objs, key=fn, reverse=desc)
    return candidates


def ranger(objs, props_dic):
    filtered = objs[:]
    for key, rango in props_dic.items():
        lo, hi = rango
        for i, obj in enumerate(filtered):
            if key not in obj:
                continue
            if (lo is not None and obj[key] < lo) \
            or (hi is not None and obj[key] > hi):
                filtered.pop(i)
    return filtered


def paginator(values, page=1, num=1):
    pages = [values[i:i+num] for i in range(0, len(values), num)]
    index = page - 1
    return pages[index] if index >= 0 and index < len(pages) else []


def response(data=None, err_code=None):
    if not err_code:
        return jsonify({'data': data, 'code': 200})

    return jsonify({'error': msg[err_code], 'code': err_code})


@app.route("/", methods=['GET', 'POST'])
def check():
    return response('Up and running!')


@app.route("/info", methods=['GET'])
def get_app():
    # Parse query params.
    screen_id = request.args.get('screen_id', None)
    prop = request.args.get('prop', None)

    if not screen_id:
        return response(err_code=100)

    filepath = './enrico/metadata/{}.json'.format(screen_id)
    if not os.path.exists(filepath):
        return response(err_code=101)

    with open(filepath) as f:
        metadata = json.load(f)

    if not metadata:
        return response(err_code=102)

    if not prop:
        return response(data=metadata)

    if prop not in metadata:
        return response(err_code=103)

    return response(data=metadata[prop])


@app.route("/results", methods=['GET'])
def get_results():
    curr_ts = datetime.now().timestamp()
    # Parse query params.
    screen_id = request.args.get('screen_id', None)
    category = request.args.get('category', '').lower()
    design = request.args.get('design', '').lower()
    min_rating = float(request.args.get('min_rating', 0.))
    max_rating = float(request.args.get('max_rating', 5.))
    min_num_ratings = int(request.args.get('min_num_ratings', 0))
    max_num_ratings = int(request.args.get('max_num_ratings', 1e10))
    min_num_downloads = int(request.args.get('min_num_downloads', 0))
    max_num_downloads = int(request.args.get('max_num_downloads', 1e10))
    min_date = float(request.args.get('min_date', 0.))
    max_date = float(request.args.get('max_date', curr_ts))
    num_results = int(request.args.get('num', 5))
    num_page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort', None)
    sort_asc = request.args.get('asc', False)

    results = find(category=category, design=design, screen_id=screen_id,
                  rating_range=(min_rating, max_rating),
                  num_ratings_range=(min_num_ratings, max_num_ratings),
                  num_downloads_range=(min_num_downloads, max_num_downloads),
                  date_range=(min_date, max_date),
                  num=num_results, page=num_page, sort=sort_by, desc=not sort_asc)

    if not results:
        return response(err_code=400)

    return response(data=results)


def find(category=None, design=None, screen_id=None,
         rating_range=(0, 5),
         num_ratings_range=(0, None),
         num_downloads_range=(0, None),
         date_range=(0, None),
         num=1, page=1, sort=None, desc=True):
    # By default will return all UIs.
    objs = app_categories[:]

    if category:
        objs = find_by_category(category, objs)

    if design:
        objs = find_by_design(design, objs)

    if screen_id:
        objs = find_by_ui(screen_id, objs)

    if not objs:
        return False

    objs = ranker(objs, sort, desc)
    objs = ranger(objs, {
        'rating': rating_range,
        'num_ratings': num_ratings_range,
        'num_downloads': num_downloads_range,
        'date': date_range,
    })

    # We must return IDs.
    ids = [o['screen_id'] for o in objs]
    ids = paginator(ids, page, num)

    return ids


# NEW: We now have a proper database.
with open('cuidb.json') as f:
    app_categories = json.load(f)

if __name__ == "__main__":
    app.run(port=9100)
