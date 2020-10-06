# Design/App recommender

This module allows requesting mobile apps based on some criteria;
e.g. similarity, top-rated apps or num. downloads (based on Rico), and design topic (based on Enrico).

## Setup

Download some Enrico dataset file first.

```sh
~$ mkdir enrico
~$ cd enrico
~$ wget http://userinterfaces.aalto.fi/enrico/resources/metadata.zip
~$ wget http://userinterfaces.aalto.fi/enrico/resources/screenshots.zip
~$ unzip -q metadata.zip
~$ unzip -q screenshots.zip
```

Then install and run the API server.

```sh
~$ pip3 install flask
~$ python3 server.py
  ...
 * Running on http://127.0.0.1:9100/ (Press CTRL+C to quit)
```

## API documentation

See [this file](documentation.md)

## App categories

* Art, Design
* Auto, Vehicles
* Beauty
* Books, Reference
* Business
* Category
* Comics
* Communication
* Dating
* Education
* Entertainment
* Events
* Finance
* Food, Drink
* Health, Fitness
* House, Home
* Lifestyle
* Maps, Navigation
* Medical
* Music, Audio
* News, Magazines
* Parenting
* Shopping
* Social
* Sports
* Travel, Local
* Video, Players, Editors
* Weather

## Design topics

* Bare
* Calculator
* Camera
* Chat
* Editor
* Form
* Gallery
* List
* Login
* Maps
* Mediaplayer
* Menu
* Modal
* News
* Other
* Profile
* Search
* Settings
* Terms
* Topic
* Tutorial
