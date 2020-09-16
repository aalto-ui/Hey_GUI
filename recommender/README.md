# Design/App recommender

This module allows requesting mobile apps based on some criteria;
e.g. similarity, top-rated apps or num. downloads (based on Rico), and design topic (based on Enrico).

## Setup

```sh
~$ pip3 install flask
~$ python3 server.py
  ...
 * Running on http://127.0.0.1:9100/ (Press CTRL+C to quit)
```

## API endpoint examples

Retrieve 3 top-rated examples of Beauty apps:
```sh
~$ curl 'http://127.0.0.1:9100/apps?category=beauty'
["43948","43947","4066"]
```

Retrieve 5 top-rated examples of login screens:
```sh
~$ curl 'http://127.0.0.1:9100/designs?topic=login&num=5'
["36126","47338","59514","1622","51137"]
```

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
