from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

import sys
import json
import requests
import layout
import base64
from PIL import Image
from io import BytesIO


ENRICO_DATASET_DIR = "../recommender/enrico"

def thumbnail(screenshot_id):
    img_file = '{}/{}.jpg'.format(ENRICO_DATASET_DIR, screenshot_id)
    img = Image.open(img_file)
    # The default screenshot size is 170x300, which is too large for the chatbot UI, so resize it by 50%.
    # Also use `thumbnail()` instead of `resize()` to avoid dealing with aspect ratios.
    siz = (85, 150)
    img.thumbnail(siz, Image.ANTIALIAS)
    return img


def str_image(img):
    # Create a base64 string so that we don't have to write images to disk.
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# reset all slot when a new command coming
class slots_reset(Action):

        def name(self) -> Text:
                return "slots_reset"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                print(tracker.latest_message)

                return [AllSlotsReset()]

class page_plus(Action):

        def name(self) -> Text:
                return "page_plus"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                if tracker.get_slot('page') == None:
                    slots = [SlotSet('page', 2),SlotSet('num', 5)]
                else:
                    p = tracker.get_slot('page')
                    slots = [SlotSet('page', p+1),SlotSet('num', 5)]

                return slots

class paginator_reset(Action):

        def name(self) -> Text:
                return "paginator_reset"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                slots = [SlotSet('page', None),SlotSet('num', None)]

                return slots

# query_form for the ui_search intents
class query_form(FormAction):
        """Example of a custom form action"""

        def name(self) -> Text:
                """Unique identifier of the form"""

                return "query_form"

        @staticmethod
        def required_slots(tracker: Tracker) -> List[Text]:
                """A list of required slots that the form has to fill"""
                return []

        def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
                """A dictionary to map required slots to
                        - an extracted entity
                        - intent: value pairs
                        - a whole message
                        or a list of them, where a first match will be picked"""

                return {
                        "app":
                                self.from_entity(
                                        entity="app", intent=["search_ui"]
                                ),
                        "design":
                                self.from_entity(
                                        entity="design", intent=["search_ui"]
                                ),
                        "filter":
                                self.from_entity(
                                        entity="filter", intent=["search_ui"]
                                ),
                        "asc":
                                self.from_entity(
                                        entity="asc", intent=["search_ui","sort"]
                                ),
                        "rating":
                                self.from_entity(
                                        entity="rating", intent=["search_ui"]
                                ),
                        "constrain":
                                self.from_entity(
                                        entity="constrain", intent=["search_ui"]
                                ),
                }


        # USED FOR DOCS: do not rename without updating in docs
        @staticmethod
        def asc_db() -> List[Text]:
                """Database of supported operation"""

                return [
                        "1",
                        "0"
                ]

        @staticmethod
        def filter_db() -> List[Text]:
                """Database of supported direction"""

                return [
                        "rating"
                ]


        @staticmethod
        def constrain_db() -> List[Text]:
                """Database of supported direction"""

                return [
                        "max",
                        "min"

                ]


        @staticmethod
        def is_float(string: Text) -> bool:
                """Check if a string is an integer"""

                try:
                        float(string)
                        return True
                except ValueError:
                        return False

        # USED FOR DOCS: do not rename without updating in docs
        def validate_asc(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate operation value."""

                if value.lower() in self.asc_db():
                        # validation succeeded, set the value of the "operation" slot to value
                        return {"asc": value}
                else:
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"asc": None}

        def validate_filter(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate operation value."""

                if value.lower() in self.filter_db():
                        # validation succeeded, set the value of the "operation" slot to value
                        return {"filter": value}
                else:
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"filter": None}

        def validate_constrain(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate operation value."""

                if value.lower() in self.constrain_db():
                        # validation succeeded, set the value of the "operation" slot to value
                        return {"constrain": value}
                else:
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"constrain": None}

        def validate_rating(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate operation value."""

                if is_float(value):
                        # validation succeeded, set the value of the "operation" slot to value
                        return {"rating": value}
                else:
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"rating": None}


        def submit(
                self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> List[Dict]:
                
                # post retrieval request to database
                url = 'http://127.0.0.1:9100/results'
                headers = {'Content-type': 'application/json'}

                # Get the query parameters from NLU.
                parameters = {}
                parameters['category'] = tracker.get_slot('app')
                parameters['design'] = tracker.get_slot('design')
                parameters['sort'] = tracker.get_slot('filter')
                parameters['asc'] = tracker.get_slot('asc')
                parameters['page'] = tracker.get_slot('page')
                parameters['num'] = tracker.get_slot('num')
                if tracker.get_slot('constrain') == "min":
                    parameters['min_rating'] = tracker.get_slot('rating')
                elif tracker.get_slot('constrain') == "max":
                    parameters['max_rating'] = tracker.get_slot('rating')

                print("Search based on:",parameters)
                r = requests.get(url, params = parameters)
                response = r.json()
                print("Response: ",response)

                if response.get('error'):
                        # Write a friendly message instead of forwarding the API error.
                        dispatcher.utter_message(text='Cannot find any design matching your description, sorry.')
                else:
                        # Remember the data, since the user has to choose one of them.
                        slots = [SlotSet('screenshot_id', response['data'])]

                        # Send default message to the bot
                        dispatcher.utter_message(text = "I found " +str(len(response['data'])) +''' screen designs for you. Say "show me more" to see more results.''')

                        # Send the thumbnails to the bot
                        suggestion_text = '<ol class="choices ml-0">'
                        for screenshot_id in response['data']:
                            img = thumbnail(screenshot_id)
                            suggestion_text += '<li><img alt="{}" src="data:image/png;base64, {}" /></li>'.format(screenshot_id, str_image(img))
                        suggestion_text += '</ol>'
                        dispatcher.utter_message(text = suggestion_text)

                        return slots

# query_form for the similar_ui intents
class similar_form(FormAction):
        """Example of a custom form action"""

        def name(self) -> Text:
                """Unique identifier of the form"""

                return "similar_form"

        @staticmethod
        def required_slots(tracker: Tracker) -> List[Text]:
                """A list of required slots that the form has to fill"""
                return ["choice"]

        def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
                """A dictionary to map required slots to
                        - an extracted entity
                        - intent: value pairs
                        - a whole message
                        or a list of them, where a first match will be picked"""

                return {
                        "choice":
                                self.from_entity(
                                        entity="asc", intent=["similar_ui","option"]
                                ),
                }


        def submit(
                self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> List[Dict]:
                
                # post retrieval request to database
                url = 'http://127.0.0.1:9100/info'
                headers = {'Content-type': 'application/json'}

                # Get the query parameters from NLU.
                parameters = {}
                screenshot_id = tracker.get_slot('screenshot_id')
                parameters['screen_id'] = screenshot_id[int(tracker.get_slot('choice'))]
                parameters['prop'] = 'title'

                print("Search based on:",parameters)
                r = requests.get(url, params = parameters)
                response = r.json()
                print("Response: ",response)

                if response.get('error') :
                        # Write a friendly message instead of forwarding the API error.
                        dispatcher.utter_message(text='Cannot find any design matching your description, sorry.')
                else:

                        # Send default message to the bot
                        dispatcher.utter_message(text = '''The similar UI is not available. Show you the title of the app instead. '''+response['data'])

                        return []