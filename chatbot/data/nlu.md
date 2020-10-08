## intent:option
- [first](choice)
- [second](choice)
- [third](choice)
- the [first](choice) one
- the [second](choice) one
- the [third](choice) one
- [fourth](choice)
- [fifth](choice)
- [sixth](choice)
- the [fourth](choice) one
- the [fifth](choice) one
- the [sixth](choice) one
- [1](choice)
- [2](choice)
- [3](choice)
- [4](choice)
- [5](choice)
- [6](choice)
- [one](choice)
- [two](choice)
- [three](choice)
- [four](choice)
- [five](choice)
- [six](choice)

## intent:show_more
- show me more
- give me more results
- show me more designs
- give me more examples
- can you show more results
- can you find more examples
- find me more interfaces
- can you give me more applications
- can you show me more UIs

## intent:similar_ui
- which are the best alternatives for the app [2](choice)
- can I search similar app of [1](choice)
- search for similar apps like [3](choice)
- show me UI like the design [two](choice)
- show me applications with similar target audience with [4](choice)
- what is the most similar UI to the UI [one](choice)
- are there similar apps to interface [three](choice)
- give me some design options like [5](choice)
- Show me more like the [first](choice) one
- can You find a UI like the [second](choice) one
- show examples similar to the [third](choice) design
- can You find a UIs similar to the [fourth](choice)


## intent:search_ui
- What are the [most](asc) [popular](filter) apps at the moment
- What are the [most](asc) [popular](filter) [finance](app) apps at the moment
- What are the [most](asc) [popular](filter) [list](design) pages at the moment
- Show me the app with the [best](asc) [rating](filter)
- Show me the app with the [best](asc) [rating](filter) for [business](app) app
- Show me the app with the [best](asc) [rating](filter) for [menu](design) page
- Show me the [most](asc) [popular](filter) apps ordered by average [rating](filter)
- Show me the [most](asc) [popular](filter) [comics](app) apps ordered by average [rating](filter)
- Show me the [most](asc) [popular](filter) [profile](design) apps ordered by average [rating](filter)
- Find me a [art](app) app with a rating [better than](constrain) [4.5](rating)
- Find me a [calculator](design) app with a rating [worse than](constrain) [4.0](rating)
- Find me a [vehicles](app) app with a rating [more than](constrain) [3](rating)
- Find me a [editor](design) app with a rating [less than](constrain) [3.5](rating)
- Find me a [communication](app) app with a rating [over](constrain) [3.0](rating)
- Find me a [login](design) app with a rating [above](constrain) [4](rating)
- Find me a [entertainment](app) app with a rating [below](constrain) [4.2](rating)
- Find me a [food](design) app with a rating [under](constrain) [4.5](rating)
- Find me a [fitness](app) app with a rating [higher than](constrain) [3.5](rating)
- Find me a [form](design) app with a rating [lower than](constrain) [5](rating)
- show me ui's with [highest](asc) [rating](filter)
- show me [audio](app) ui's with [highest](asc) [rating](filter)
- show me [search](design) ui's with [highest](asc) [rating](filter)
- Which app has the [highest](asc) [score](filter)
- Which [house](app) app has the [highest](asc) [score](filter)
- Which app has the [lowest](asc) [score](filter)
- Which [maps](design) app has the [lowest](filter) [score](filter)?
- What's the [most](asc) [popular](filter) app?
- What's the [most](asc) [popular](filter) [travel](app) app?
- What's the [most](asc) [popular](filter) [tutorial](design) page?
- Show me UI's for [business](app)
- Can you show me the UI of [education](app) mobile application?
- show me [art](app) apps
- find me [design](app) apps
- Show me UI relating to [food](app)
- show me [auto](app) applications
- find me [vehicles](app) applications
- could you show me [beauty](app) applications
- can you show me [books](app) apps
- can you show me [reference](app) apps
- can you show me [business](app) apps
- can you show me [category](app) apps
- can you find me [comics](app) apps
- can you find me [communication](app) apps
- find me [dating](app) applications
- can you show me [education](app) applications
- show me [entertainment](app) applications
- can you show me [events](app) applications
- can you show me [finance](app) applications
- can you show me [food](app) apps
- find me [drink](app) apps
- find [health](app) apps
- can you show [fitness](app) apps
- find [house](app) applications
- find [home](app) applications
- can you find [lifestyle](app) applications
- can you find a [maps](app) apps
- please show [navigation](app) apps
- please show [medical](app) apps
- please show [music](app) apps
- show me [audio](app) apps
- find me [news](app) apps
- can you find me [magazines](app) applications
- find me [parenting](app) applications
- give me ideas of a [shopping](app) applications
- can you show me [social](app) applications
- can you show me [sports](app) applications
- find me [travel](app) apps
- how can I design a [local](app) apps
- find me [video](app) applications
- give me ideas of a [players](app) applications
- show me [editors](app) applications
- can you show me [weather](app) apps
- find me [bare](design) pages
- find me [calculator](design) pages
- how can I design an [camera](design) pages
- find me [chat](design) pages
- can you find me [editor](design) pages
- can you show me [form](design) interfaces
- can you show me [gallery](design) interfaces
- give me ideas of [list](design) pages
- can you show me [login](design) pages
- find me [maps](design) pages
- show [mediaplayer](design) pages
- find me [menu](design) pages
- find me [modal](design) pages
- can you find me [news](design) interfaces
- can you show me [profile](design) interfaces
- show [search](design) interfaces
- give me ideas of [settings](design) pages
- can you show me [terms](design) pages
- can you find me [topic](design) interfaces
- find me [tutorial](design) pages

## intent:sort
- Sort UIs by average [rating](filter)
- Filter them by [popularity](filter)
- Filter them by star [rating](filter)
- Filter them by [rating](filter)
- order them by average [rating](filter)
- sort UI by [popularity](filter)
- can you sort UI by [popularity](filter)
- can you order UI by [popularity](filter)
- can you sort UI by average [rating](filter)


## intent:clear_memory
- clear my search
- clear my query
- clear my selection
- clear my filters

## intent:help
- help
- help me
- show me the help menu
- what can you do

## regex:rating
- [0-9]{1,}.?[0-9]?

## synonym:1
- first
- one

## synonym:2
- second
- two

## synonym:3
- third
- three

## synonym:4
- four
- fourth

## synonym:5
- five
- fifth

## synonym:6
- six
- sixth

## synonym:rating
- score
- popularity
- popular

## synonym:0
- highest
- most
- best

## synonym:1
- lowest
- least

## synonym:min
- better than
- more than
- over
- above
- higher than

## synonym:max
- worse than
- less than
- below
- under
- lower than


## lookup:app
  data/lookup_tables/app_category.txt

## lookup:design
  data/lookup_tables/design_topic.txt
