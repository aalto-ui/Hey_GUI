# CUI recommender API

The API is RESTful and JSON-based.
The server is running in port 9001 by default:
```
~$ python3 server.py

 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:9100/ (Press CTRL+C to quit)
```

To check if the API is up and running you can send the following request from your CLI:
```
~$ curl 'http://127.0.0.1:9100/'
{"alive":true,"code":200}
```

## Endpoints

As described in the paper, we have two group of user queries:

* First group: Retrieve info about a particular app/design

  - Show similar UIs
  - Add a comment to the UI
  - Highlight a component of the UI (e.g. highlight the search bar)
  - Enquire about privacy information of an app (e.g. does this app use the camera?)

* Second group: Retrieve more than one app/design

  - Show UIs with some particular features (search bar)
  - Show UIs of particular category (entertainment)
  - Show UIs that serve a particular purpose (e.g. login)
  - Show UIs that have certain privacy features(e.g. show apps which use the microphone)
  - Show UIs of applications filtered by average user rating or number of downloads (e.g. show UIs with rating above 4.0)

### First group of queries

The endpoint for the first group of queries is `/info`.
The `screen_id` param is required.

| Request example                | Retrieved result                               |
|---                             |---                                             |
| /info?screen_id=100            | All info of the app having the UI with ID 100  |
| /info?screen_id=100&prop=title | App title of the app having the UI with ID 100 |

The `prop` param can be one of these:
- app_id
- category
- content_rating
- current_version
- description
- description_html
- developer
- developer_address
- developer_email
- developer_id
- developer_url
- editors_choice
- free
- iap
- iap_range
- icon
- installs
- interactive_elements
- price
- recent_changes
- required_android_version
- reviews
- score
- screenshots
- size
- title
- updated
- url
- video

Examples for the query `/info?screen_id=10183&prop=<some value>`

| Prop value               | Result                                   |
|---                       |---                                       |
| app_id                   | "com.aetn.lifetime.watch"                |
| category                 | ["ENTERTAINMENT"]                        |
| content_rating           | ["Teen"]                                 |
| current_version          | "3.3.1"                                  |
| description              | "Watch hours of ..."                     |
| description_html         | "Watch <b>hours</b> of ..."              |
| developer                | "A&E Television Networks Mobile"         |
| developer_address        | "235 E 45th Street\nNew York, NY 10017"  |
| developer_email          | "watchapps@aenetworks.com"               |
| developer_id             | "A%26E+Television+Networks+Mobile"       |
| developer_url            | "http://www.mylifetime.com"              |
| editors_choice           | false                                    |
| free                     | true                                     |
| iap                      | false                                    |
| iap_range                | null                                     |
| icon                     | "https://lh3.googleusercontent..."       |
| installs                 | "5,000,000+"                             |
| interactive_elements     | null                                     |
| price                    | "0"                                      |
| recent_changes           | null                                     |
| required_android_version | "4.4 and up"                             |
| reviews                  | 43157                                    |
| score                    | "4.1"                                    |
| screenshots              | ["https://lh3.google...", ...]           |
| size                     | "19M"                                    |
| title                    | "Lifetime - Watch Full ..."              |
| updated                  | "June 18, 2020"                          |
| url                      | "https://play.google.com/..."            |
| video                    | null

### Second group of queries

The endpoint for the second group of queries is `/results`. No query param is required.

| Request example            | Retrieved result                     |
|---                         |---                                   |
| /results                   | ALL UIs in the database              |
| /results?screen_id=10000   | UIs similar to the one with ID 10000 |
| /results?category=news     | UIs from the news category           |
| /results?design=login      | UIs with a login design              |

Both `category` and `design` can be combined:
```
/results?category=news&design=login # retrieve news apps with a login design
```

Results can be sorted by `rating`, `num_ratings`, `num_downloads`, and `date`.
If no `sortby` param is provided, results are magically sorted.
```
/results?design=login&sortby=rating # retrieve top ranked login designs
```

The default sorting method is **descending** (from higher to lower),
but ascending sort can be set with the `asc` param:
```
/results?design=login&sortby=rating&asc=1 # retrieve the lowest ranked login designs
```

Pagination is useful when there are a lot of results and we want to inspect them in smaller groups.
```
/results?design=login&num=10 # retrieve the first 10 login designs
/results?design=login&num=10&page=2 # retrieve the second group of 10 results
```
