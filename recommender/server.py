#!/usr/bin/env python
# coding: utf-8

import sys
import json
import csv
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


def normalize(obj):
    obj['category'] = obj['category'].lower()
    obj['rating'] = float(obj['rating'])
    obj['num_ratings'] = int(obj['num_ratings'])
    obj['num_downloads'] = parse_downloads(obj['num_downloads'])
    obj['date'] = parse_date(obj['date'])
    return obj


def parse_downloads(s):
    # Format is like " 1,000,000 - 5,000,000 "
    lo, hi = s.strip().split(' - ')
    lo = lo.replace(',', '')
    lo = int(lo)
    hi = hi.replace(',', '')
    hi = int(hi)
    return (lo + hi) // 2


def parse_date(s, fmt='%B %d, %Y'):
    dt = datetime.strptime(s, fmt)
    return datetime.timestamp(dt)


def find_by_ui(screen_id, objs=None):
    if objs is None:
        objs = app_categories[:]
    filtered = [] # TODO
    return filtered


def find_by_category(name, objs=None):
    if objs is None:
        objs = app_categories[:]
    filtered = [row for row in objs if row['category'] == name]
    return filtered


def find_by_design(name, objs=None):
    if objs is None:
        objs = app_categories[:]
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


def paginator(values, page=1, num=1):
    pages = [values[i:i+num] for i in range(0, len(values), num)]
    index = page - 1
    return pages[index] if index >= 0 and index < len(pages) else []


@app.route("/", methods=['GET', 'POST'])
def check():
    return jsonify({'alive': True, 'code': 200})


@app.route("/info", methods=['GET'])
def get_app():
    # Parse query params.
    screen_id = request.args.get('screen_id', None)
    prop = request.args.get('prop', None)

    if not screen_id:
        return jsonify({'error': msg[100], 'code': 100})

    filepath = './enrico/metadata/{}.json'.format(screen_id)
    if not os.path.exists(filepath):
        return jsonify({'error': msg[101], 'code': 101})

    with open(filepath) as f:
        metadata = json.load(f)

    if not metadata:
        return jsonify({'error': msg[102], 'code': 102})

    if not prop:
        return jsonify({'data': metadata, 'code': 200})

    if prop not in metadata:
        return jsonify({'error': msg[103], 'code': 103})

    return jsonify({'data': metadata[prop], 'code': 200})


@app.route("/results", methods=['GET'])
def get_results():
    # Parse query params.
    screen_id = request.args.get('screen_id', None)
    category = request.args.get('category', '').lower()
    design = request.args.get('design', '').lower()
    num_results = int(request.args.get('num', 3))
    num_page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort', None)
    sort_asc = request.args.get('asc', False)

    results = find(category=category, design=design, screen_id=screen_id,
                  num=num_results, page=num_page, sort=sort_by, desc=not sort_asc)

    if not results:
        return jsonify({'error': msg[400], 'code': 400})

    return jsonify({'data': results, 'code': 200})


def find(category=None, design=None, screen_id=None, num=1, page=1, sort=None, desc=True):
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

    # We must return IDs.
    ids = [o['screen_id'] for o in objs]
    ids = paginator(ids, page, num)

    return ids


# Load basic datasets. TODO: Use a proper database.
with open('enrico-topics.csv') as csvfile:
    col_names = ['screen_id', 'design']
    design_topics = list(csv.DictReader(csvfile, delimiter=',', fieldnames=col_names))
    design_topics.pop(0)

# Map IDs to topics.
design_dict = {}
for row in design_topics:
    design_dict[row['screen_id']] = row['design']

# Merge with app details dataset.
with open('enrico-app_details.csv') as csvfile:
    col_names = ['screen_id', 'pkg_name', 'app_name', 'category', 'rating', 'num_ratings', 'num_downloads', 'date', 'icon_url']
    app_categories = list(csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=col_names))
    app_categories.pop(0)

    # Some Rico screenshots have no associated app details, so ignore them.
    for i, row in enumerate(app_categories):
        if not row['app_name']:
            app_categories.pop(i)
            continue
        if row['screen_id'] in design_dict:
            row['design'] = design_dict[row['screen_id']]

# Finally normalize data.
app_categories = [normalize(dict(row)) for row in app_categories if 'design' in row]

if __name__ == "__main__":
    app.run(port=9100)
