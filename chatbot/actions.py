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

# clear the canvas
class clear_canvas_submit(Action):

        def name(self) -> Text:
                return "clear_canvas_submit"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                json_command = {"intent": "clear_canvas"}
                dispatcher.utter_message(json_message = json.dumps(json_command, sort_keys=False))


# recommender design examples
class recommender_designs_post(Action):

        def name(self) -> Text:
                return "recommender_designs_post"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                url = 'http://127.0.0.1:9100/designs'
                headers = {'Content-type': 'application/json'}

                # TODO: Get the (topic) entity from NLU.
                state = tracker.get_slot('design_topic')

                r = requests.get(url, params={'topic':state})
                response = r.json()

                if response.get('error'):
                        # Write a friendly message instead of forwarding the API error.
                        dispatcher.utter_message(text='Cannot find any design matching your description, sorry.')
                else:
                        dispatcher.utter_message(text = "Here you have some screen designs. Which one do you prefer? Say 1, 2, etc.")

                        suggestion_text = '<ol class="choices ml-0">'
                        for screenshot_id in response['data']:
                            img = thumbnail(screenshot_id)
                            suggestion_text += '<li><img alt="{}" src="data:image/png;base64, {}" /></li>'.format(screenshot_id, str_image(img))
                        suggestion_text += '</ol>'
                        dispatcher.utter_message(text = suggestion_text)

                        # Remember the data, since the user has to choose one of them.
                        slots = []
                        for i, screenshot_id in enumerate(response['data']):
                            name = "thumbnail_{}".format(i+1)
                            json_file = '{}/{}.json'.format(ENRICO_DATASET_DIR, screenshot_id)
                            with open(json_file) as f:
                                content = json.load(f)
                            slots.append(SlotSet(name, content))
                        return slots


# recommender app examples
class recommender_apps_post(Action):

        def name(self) -> Text:
                return "recommender_apps_post"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                url = 'http://127.0.0.1:9100/apps'
                headers = {'Content-type': 'application/json'}

                # TODO: Get the (topic) entity from NLU.
                state = tracker.get_slot('app_category')

                r = requests.get(url, params={'category':state})
                response = r.json()

                print("intent: ",tracker.get_slot('form_intent')," app_category: ",state)

                if response.get('error'):
                        # Write a friendly message instead of forwarding the API error.
                        dispatcher.utter_message(text='Cannot find any app matching your description, sorry.')
                else:
                        dispatcher.utter_message(text = "Here you have some app designs. Which one do you prefer? Say 1, 2, etc.")

                        suggestion_text = '<ol class="choices ml-0">'
                        for screenshot_id in response['data']:
                            img = thumbnail(screenshot_id)
                            suggestion_text += '<li><img alt="{}" src="data:image/png;base64, {}" /></li>'.format(screenshot_id, str_image(img))
                        suggestion_text += '</ol>'
                        dispatcher.utter_message(text = suggestion_text)

                        # Remember the data, since the user has to choose one of them.
                        slots = []
                        for i, screenshot_id in enumerate(response['data']):
                            name = "thumbnail_{}".format(i+1)
                            json_file = '{}/{}.json'.format(ENRICO_DATASET_DIR, screenshot_id)
                            with open(json_file) as f:
                                content = json.load(f)
                            slots.append(SlotSet(name, content))
                        return slots


# suggest design examples
class suggest_post(Action):

        def name(self) -> Text:
                return "suggest_post"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                url = 'http://127.0.0.1:9000/suggest'
                headers = {'Content-type': 'application/json'}

                state = tracker.current_state()
                # Read the last user event, since it has the latest layout.
                user_events = [e for e in state['events'] if e['event'] == 'user']
                metadata = user_events[-1]['metadata']

                r = requests.post(url, json = metadata)
                response = r.json()

                if response.get('error'):
                        # Write a friendly message instead of forwarding the API error.
                        dispatcher.utter_message(text='Cannot find any related designs, sorry.')
                else:
                        dispatcher.utter_message(text = "Here you have some designs. Which one do you prefer? Say 1, 2, etc.")

                        suggestion_text = '<ol class="choices ml-0">'
                        for candidate in response['layouts']:
                            dat = layout.load(candidate)
                            img = layout.create_image(dat, resize=False)
                            suggestion_text += '<li><img src="data:image/png;base64, {}" /></li>'.format(str_image(img))
                        suggestion_text += '</ol>'
                        dispatcher.utter_message(text = suggestion_text)

                        #dispatcher.utter_message(json_message = json.dumps(json_command, sort_keys=False))
                        #dispatcher.utter_message(text = "wrong in layout output")

                        # Remember the layouts, since the user has to choose one of them.
                        slots = []
                        for i, candidate in enumerate(response['layouts']):
                            name = "thumbnail_{}".format(i+1)
                            slots.append(SlotSet(name, candidate))
                        return slots


# optimizer stuff
class optimizer_post(Action):

        def name(self) -> Text:
                return "optimizer_post"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                url = 'http://127.0.0.1:9000/refine'
                headers = {'Content-type': 'application/json'}

                state = tracker.current_state()
                # Read the last user event, since it has the latest layout.
                user_events = [e for e in state['events'] if e['event'] == 'user']
                metadata = user_events[-1]['metadata']

                r = requests.post(url, json = metadata)
                response = r.json()

                if response.get('error'):
                        # Write a friendly message instead of forwarding the API error.
                        dispatcher.utter_message(text='Cannot optimize this design, sorry.')
                else:
                        # Unpack layout.
                        result = response['layouts'][0]
                        json_command = {"intent": "optimize", "result": result}
                        dispatcher.utter_message(json_message = json.dumps(json_command, sort_keys=False))

                return []

# reset all slot when a new command coming
class slots_reset(Action):

        def name(self) -> Text:
                return "slots_reset"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                print(tracker.latest_message)

                return [AllSlotsReset()]


class intent_save(Action):

        def name(self) -> Text:
                return "intent_save"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                form_intent = tracker.latest_message['intent'].get('name')
                return [SlotSet("form_intent", form_intent),SlotSet("choice", None)]

class item_extraction(Action):

        def name(self) -> Text:
                return "item_extraction"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

                slots = []
                items = tracker.get_slot('items')

                if items is not None:
                        slots.append(SlotSet("component",items[0]))
                        if len(items) > 1:
                                slots.append(SlotSet("anchor",items[1]))

                return slots


class shortcut_submit(Action):

        def name(self) -> Text:
                return "shortcut_submit"

        def run(self, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                operation = tracker.get_slot('operation')
                dispatcher.utter_message(json_message = json.dumps({"intent":"shortcut","operation":operation},sort_keys=False))
                return []

# suggest_form for the main intents
class suggest_form(FormAction):
        """Example of a custom form action"""

        def name(self) -> Text:
                """Unique identifier of the form"""

                return "suggest_form"

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
                                        entity="choice", intent=["option"]
                                ),
                }


        # USED FOR DOCS: do not rename without updating in docs
        @staticmethod
        def choice_db() -> List[Text]:
                """Database of supported operation"""

                return [
                        "1",
                        "2",
                        "3"
                ]


        # USED FOR DOCS: do not rename without updating in docs
        def validate_choice(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate operation value."""

                if value.lower() in self.choice_db():
                        # validation succeeded, set the value of the "operation" slot to value
                        return {"choice": value}
                else:
                        dispatcher.utter_message(template="utter_wrong_choice")
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"choice": None}

        def submit(
                self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> List[Dict]:
                """Define what the form has to do
                        after all required slots are filled"""
                choice = tracker.get_slot('choice')
                json_command = {'intent': tracker.get_slot('form_intent'), 'choice': choice, 'result': tracker.get_slot('thumbnail_'+ choice)}
                # utter submit template
                dispatcher.utter_message(json_message = json.dumps(json_command,sort_keys=False))
                dispatcher.utter_message(text = "Design no.{} is adopted, then.".format(choice))
                return []


# command_form for the main intents
class command_form(FormAction):
        """Example of a custom form action"""

        def name(self) -> Text:
                """Unique identifier of the form"""

                return "command_form"

        @staticmethod
        def required_slots(tracker: Tracker) -> List[Text]:
                """A list of required slots that the form has to fill"""
                if tracker.get_slot('form_intent') == "object":
                        if tracker.get_slot('anchor') != None :
                                return ["operation", "component","direction","anchor"]
                        elif tracker.get_slot('operation') == "move" :
                                return ["operation", "component","direction"]
                        elif tracker.get_slot('operation') == "align":
                                return ["operation","direction"]
                        elif tracker.get_slot('operation') == "deselect":
                                return ["operation"]
                        else:
                                return ["operation", "component"]
                else:
                        if tracker.get_slot('distance') != None:
                            return ["dimension"]
                        else:
                            return ["comparison"]

        def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
                """A dictionary to map required slots to
                        - an extracted entity
                        - intent: value pairs
                        - a whole message
                        or a list of them, where a first match will be picked"""

                return {
                        "anchor":
                                self.from_entity(
                                        entity="component", intent=["chitchat"]
                                ),
                        "operation":
                                self.from_entity(
                                        entity="operation", intent=["chitchat"]
                                ),
                        "component":
                                self.from_entity(
                                        entity="component", intent=["chitchat"]
                                ),
                        "direction":
                                self.from_entity(
                                        entity="direction", intent=["chitchat"]
                                ),
                        "comparison":
                                self.from_entity(
                                        entity="direction", intent=["chitchat"]
                                ),
                }


        # USED FOR DOCS: do not rename without updating in docs
        @staticmethod
        def operation_db() -> List[Text]:
                """Database of supported operation"""

                return [
                        "add",
                        "move",
                        "select",
                        "delete",
                        "align",
                        "deselect"
                ]

        @staticmethod
        def direction_db() -> List[Text]:
                """Database of supported direction"""

                return [
                        "left",
                        "right",
                        "top",
                        "bottom",
                        "top left",
                        "top right",
                        "bottom left",
                        "bottom right",
                        "center"
                ]


        @staticmethod
        def comparison_db() -> List[Text]:
                """Database of supported direction"""

                return [
                        "same high",
                        "same",
                        "same wide",
                        "bigger",
                        "smaller",
                        "wider",
                        "taller",
                        "narrower",
                        "shorter"
                ]

        @staticmethod
        def dimension_db() -> List[Text]:
                """Database of supported direction"""

                return [
                        "height",
                        "size",
                        "width",

                ]

        @staticmethod
        def component_db() -> List[Text]:
                """Database of supported component"""

                return [
                        "advertisement",
                        "background image",
                        "bottom navigation",
                        "button bar",
                        "card",
                        "checkbox",
                        "drawer panel",
                        "multi-tab",
                        "number stepper",
                        "on/off switch",
                        "pager indicator",
                        "radio button",
                        "slider",
                        "text button",
                        "toolbar",
                        "video",
                        "web view",
                        "list item",
                        "map view",
                        "canvas",
                        "it",
                        "them",
                        "date picker",
                        "image",
                        "picture",
                        "text",
                        "title",
                        "paragraph",
                        "input",
                        "modal",
                        "all",
                        "none"
                ]

        @staticmethod
        def is_int(string: Text) -> bool:
                """Check if a string is an integer"""

                try:
                        int(string)
                        return True
                except ValueError:
                        return False

        # USED FOR DOCS: do not rename without updating in docs
        def validate_operation(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate operation value."""

                if value.lower() in self.operation_db():
                        # validation succeeded, set the value of the "operation" slot to value
                        return {"operation": value}
                else:
                        dispatcher.utter_message(template="utter_wrong_operation")
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"operation": None}

        def validate_component(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate component value."""
                if tracker.get_slot('requested_slot') == "component" or tracker.get_slot('requested_slot') == None:
                        if value.lower() in self.component_db():
                                # validation succeeded, set the value of the "component" slot to value
                                return {"component": value}
                        else:
                                dispatcher.utter_message(template="utter_wrong_component")
                                # validation failed, set this slot to None, meaning the
                                # user will be asked for the slot again
                                return {"component": None}
                else:
                        return {"component": None}

        def validate_direction(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate component value."""

                if value.lower() in self.direction_db():
                        # validation succeeded, set the value of the "direction" slot to value
                        return {"direction": value}
                else:
                        dispatcher.utter_message(template="utter_wrong_direction")
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"direction": None}

        def validate_comparison(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate component value."""

                if value.lower() in self.comparison_db():
                        # validation succeeded, set the value of the "direction" slot to value
                        return {"comparison": value}
                else:
                        dispatcher.utter_message(template="utter_wrong_comparison")
                        # validation failed, set this slot to None, meaning the
                        # user will be asked for the slot again
                        return {"comparison": None}

        def validate_anchor(
                self,
                value: Text,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
                """Validate component value."""

                if tracker.get_slot('requested_slot') == "anchor" or tracker.get_slot('requested_slot') == None:
                        if value.lower() in self.component_db():
                                # validation succeeded, set the value of the "component" slot to value
                                return {"anchor": value}
                        else:
                                dispatcher.utter_message(template="utter_wrong_anchor")
                                # validation failed, set this slot to None, meaning the
                                # user will be asked for the slot again
                                return {"anchor": None}
                else:
                        return {"anchor": None}


        def submit(
                self,
                dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any],
        ) -> List[Dict]:
                """Define what the form has to do
                        after all required slots are filled"""
                json_command = {}
                json_command['intent'] = tracker.get_slot('form_intent')
                json_command['operation'] = tracker.get_slot('operation')
                json_command['component'] = tracker.get_slot('component')
                json_command['direction'] = tracker.get_slot('direction')
                json_command['anchor'] = tracker.get_slot('anchor')
                json_command['comparison'] = tracker.get_slot('comparison')
                json_command['dimension'] = tracker.get_slot('dimension')
                json_command['distance'] = tracker.get_slot('distance')
                json_command['unit'] = tracker.get_slot('unit')
                # utter submit template
                dispatcher.utter_message(json_message = json.dumps(json_command,sort_keys=False))
                return []
