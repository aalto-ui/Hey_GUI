## object/happy path
* object OR scale
  - intent_save
  - item_extraction
  - command_form
  - form{"name": "command_form"}
  - form{"name": null}
  - utter_done
  - slots_reset

## object/unhappy path I
* object OR scale
  - intent_save
  - item_extraction
  - command_form
  - form{"name": "command_form"}
* chitchat
  - command_form
  - form{"name": null}
  - utter_done
  - slots_reset

## object/unhappy path II
* object OR scale
  - intent_save
  - item_extraction
  - command_form
  - form{"name": "command_form"}
* chitchat
  - command_form
* chitchat
  - command_form
  - form{"name": null}
  - utter_done
  - slots_reset

## object/angry path I
* object OR scale
  - intent_save
  - item_extraction
  - command_form
  - form{"name": "command_form"}
* deny
  - form{"name": null}
  - utter_sorry
  - slots_reset

## shortcut command
* shortcut
  - shortcut_submit
  - utter_done
  - slots_reset

## optimization command
* optimize
  - optimizer_post
  - utter_done
  - slots_reset

## suggest command happy path
* suggest
  - intent_save
  - suggest_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}

## suggest command alternative path I
* suggest
  - intent_save
  - suggest_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}
* option
  - suggest_form
  - form{"name": "suggest_form"}
  - form{"name": null}

## suggest command alternative path II
* suggest
  - intent_save
  - suggest_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}
* option
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}

## suggest command unhappy path I
* suggest
  - intent_save
  - suggest_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
* option
  - suggest_form
  - form{"name": null}

## suggest command angry path I
* suggest
  - intent_save
  - suggest_post
  - suggest_form
  - form{"name": "suggest_form"}
* deny
  - form{"name": null}
  - utter_sorry
  - slots_reset

## recommend designs happy path
* recommend_topic
  - intent_save
  - recommender_designs_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}

## recommend designs alternative path II
* recommend_topic
  - intent_save
  - recommender_designs_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}
* option
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}

## recommend designs deny path I
* recommend_topic
  - intent_save
  - recommender_designs_post
  - suggest_form
  - form{"name": "suggest_form"}
* deny
  - form{"name": null}
  - utter_sorry

## recommend apps happy path
* recommend_category
  - intent_save
  - recommender_apps_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}

## recommend apps alternative path II
* recommend_category
  - intent_save
  - recommender_apps_post
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}
* option
  - suggest_form
  - form{"name": "suggest_form"}
* option
  - suggest_form
  - form{"name": null}

## recommend apps angry path
* recommend_category
  - intent_save
  - recommender_apps_post
  - suggest_form
  - form{"name": "suggest_form"}
* deny
  - form{"name": null}
  - utter_sorry

## help
* help
  - utter_help

## greet
* greet
  - utter_welcome

## clear_canvas
* clear_canvas
  - clear_canvas_submit
  - utter_done

## component_challenge
* component_challenge
  - utter_component_challenge
