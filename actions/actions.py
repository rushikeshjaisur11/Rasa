# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from functools import reduce
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

covid_data = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')
covid_data.drop(['SlNo','District_Key'],axis=1,inplace = True)

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ActionAddNums(Action):

    def name(self) -> Text:
        return "action_add_nums"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        enitities = tracker.latest_message['entities']
        vals = ''
        for i in enitities:
            if(i['entity']=='numbers'):
                vals = i['value']
        if(',' in vals):
            vals = vals.split(',')
        else:
            vals = vals.split(' ')
        res = sum([int(i) for i in vals])    
        dispatcher.utter_message(text=f"{res}")

        return []

class ActionMultiplyNums(Action):

    def name(self) -> Text:
        return "action_multiply_nums"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        enitities = tracker.latest_message['entities']
        vals = ''
        for i in enitities:
            if(i['entity']=='numbers'):
                vals = i['value']
        if(',' in vals):
            vals = vals.split(',')
        else:
            vals = vals.split(' ')
        vals = [int(i) for i in vals]
        res = reduce(lambda x,y:x*y,vals)    
        dispatcher.utter_message(text=f"{res}")

        return []

class ActionGetCovidInfo(Action):

    def name(self) -> Text:
        return "action_get_covid"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        value = entities[0]['value']
        try:
            data = covid_data[covid_data['District']==value.title()]
            confirmed = data['Confirmed'].values[0]
            active = data['Active'].values[0]
            recovered = data['Recovered'].values[0]
            deceased = data['Deceased'].values[0]
            dispatcher.utter_message(text=f'Total Confirmed = {confirmed}\nTotal Active = {active}\nTotal Recovered = {recovered}\nTotal Deceased = {deceased}')
        except:
            dispatcher.utter_message(text=f'Data not found for District {value}')