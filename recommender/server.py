#!/usr/bin/env python
# coding: utf-8

import sys
import json
import csv
from random import shuffle
from operator import itemgetter
from flask import Flask, request, jsonify


app = Flask(__name__)
msg = {
    'ERR_NO_INPUT': 'No input data provided (code: E100)',
    'ERR_NO_RESULT': 'No result (code: E200)'
}


with open('enrico-app_details.csv') as csvfile:
    col_names = ['image_id', 'pkg_name', 'app_name', 'category', 'avg_rating', 'num_ratings', 'est_downloads', 'date', 'icon_url']
    app_categories = list(csv.DictReader(csvfile, delimiter=',', quotechar='"', fieldnames=col_names))
    app_categories.pop(0)

    # Some Rico screenshots have no associated app details, so ignore them.
    for i, row in enumerate(app_categories):
        if not row['app_name']:
            app_categories.pop(i)
            continue

# Normalize values were available, e.g. lowercase category, cast numbers, etc.
def review(obj):
    obj['category'] = obj['category'].lower()
    obj['avg_rating'] = float(obj['avg_rating'])
    obj['num_ratings'] = int(obj['num_ratings'])
    obj['est_downloads'] = obj['est_downloads'].strip()
    return obj

app_categories = [review(row) for row in app_categories]


with open('enrico-topics.csv') as csvfile:
    col_names = ['image_id', 'topic']
    design_topics = list(csv.DictReader(csvfile, delimiter=',', fieldnames=col_names))
    design_topics.pop(0)


def rank_ids(obj_list, sortby=None, desc=True):
    # NB: `sortby` should be 'avg_rating', 'num_ratings', or 'date'.
    if not sortby or sortby.startswith('rand'):
        shuffle(obj_list)
        return [entry['image_id'] for entry in obj_list]

    # Use descending sort by default, i.e. from highest to lowest values.
    candidates = sorted(obj_list, key=itemgetter(sortby), reverse=desc)
    return [entry['image_id'] for entry in candidates]


def find_apps(category=None, num=2, sortby=None):
    if not category:
        # Pick candidates at random from any category.
        filtered_apps = app_categories[:]
        shuffle(filtered_apps)
    else:
        # Filter apps by category.
        filtered_apps = [row for row in app_categories if category in row['category']]

    if not filtered_apps:
        return None

    return rank_ids(filtered_apps, sortby)[:num]


def find_designs(topic=None, num=2, sortby=None):
    if not topic:
        # Pick candidates at random.
        filtered_ids = [design['image_id'] for design in design_topics]
        shuffle(filtered_ids)
    else:
        # Filter designs by category.
        filtered_ids = [design['image_id'] for design in design_topics if topic in design['topic']]

    if not filtered_ids:
        return None

    # The Enrico file doesn't have metadata, so get that info from the apps dataset.
    filtered_topics = [row for row in app_categories for image_id in filtered_ids if row['image_id'] == image_id]

    return rank_ids(filtered_topics, sortby)[:num]


def find_similar(layout, num=1):
    # TODO: Implement this method.
    # We should load all JSONs into memory (e.g. kd-tree) to speed up computations.
    return None


@app.route("/", methods=['GET', 'POST'])
def check():
    return jsonify({'alive': True, 'error': None})


@app.route("/apps", methods=['GET'])
def get_apps():
    category = request.args.get('category', '').lower()
    num_results = request.args.get('num', 3)
    sort_by = request.args.get('sort', None)

    result = find_apps(category, num=int(num_results), sortby=sort_by)
    if not result:
        return jsonify({'error': msg['ERR_NO_RESULT']})
    return jsonify({'data': result})


@app.route("/designs", methods=['GET'])
def get_designs():
    topic = request.args.get('topic', '').lower()
    num_results = request.args.get('num', 3)
    sort_by = request.args.get('sort', None)

    result = find_designs(topic, num=int(num_results), sortby=sort_by)
    if not result:
        return jsonify({'error': msg['ERR_NO_RESULT']})
    return jsonify({'data': result})


@app.route("/similar", methods=['POST'])
def post_similar():
    content = request.json
    if content is None:
        return jsonify({'error': msg['ERR_NO_INPUT']})

    result = find_similar(content)
    return jsonify({'data': result})


if __name__ == "__main__":
    app.run(port=9100)
