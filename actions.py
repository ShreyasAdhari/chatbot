from typing import Any, Text, Dict,Union, List ## Datatypes

from rasa_sdk import Action, Tracker  ##
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionReverted, FollowupAction


import re

import pymongo
from pymongo import MongoClient
from bson import ObjectId

database = "OnlineMarketplace"

client = MongoClient()
db = client[database]


class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        camera = tracker.get_slot('camera')
        ram = tracker.get_slot('RAM')
        battery = tracker.get_slot('battery')

        dispatcher.utter_message(text='Here are your search results')
        
        dispatcher.utter_message(text='The features you entered: ' + str(camera) + ", " + str(ram) + ", " + str(battery))
        return []
########################

class QuantityAddressForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "quantity_address_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["quantity"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {
        "quantity":[self.from_text()],
        }
    
    def validate_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            quantity = int(re.findall(r'[0-9]+',value)[0])
        except:
            quantity = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if quantity < 50 and quantity >= 0:
            return {"quantity":quantity}
        else:
            dispatcher.utter_message(template="utter_wrong_quantity")

            return {"quantity":None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        userid = (extract_metadata_from_tracker(tracker)['userid'])
        order_id = tracker.get_slot("order_id")
        quantity = tracker.get_slot("quantity")
        orders = db.orders.find({"userId":ObjectId(userid)})

        # for item in order.get("items"):

        #     if item["productId"] == product_id:
        #         pq = item["quantity"]
        #         item["quantity"] = quantity
        #         order["total"] = order["total"] + (quantity - pq)*item["price"]
        #         print(order)

        for order in orders:
            for item in order["items"]:

                if item.get("_id") == ObjectId(order_id):
                    pq = item["quantity"]
                    item["quantity"] = quantity
                    order["total"] = order["total"] + (quantity - pq)*item["price"]
                    db.orders.replace_one({"_id":ObjectId(order.get("_id"))},order)
                    print(order)
                    


                
                
                


        
        dispatcher.utter_message(text="Order Quantity Updated.")
        dispatcher.utter_message(template='utter_select_next')

        return [SlotSet("order_id",None),SlotSet("quantity",None)]





class ProductSearchForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "product_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        if tracker.get_slot('category') == 'phone':
            return ["ram","battery","camera","budget"]
        elif tracker.get_slot('category') == 'laptop':
            return ["ram","battery_backup","storage_capacity","budget"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""


        return {"ram":[self.from_text()],
        "camera":[self.from_text()],
        "battery":[self.from_text()],
        "budget":[self.from_text()],
        "battery_backup":[self.from_text()],
        "storage_capacity":[self.from_text()]
        }


    def validate_battery_backup(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            battery_backup_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_backup_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_backup_int < 50:
            return {"battery_backup":battery_backup_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery_backup")

            return {"battery_backup":None}

    def validate_storage_capacity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            storage_capacity_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            storage_capacity_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if storage_capacity_int < 2000:
            return {"storage_capacity":storage_capacity_int}
        else:
            dispatcher.utter_message(template="utter_wrong_storage_capacity")

            return {"storage_capacity":None}

    def validate_ram(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # 8 | Im looking for 8 GB | 8 GB RAM
        # Im looking for ram
        try:
            ram_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            ram_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if ram_int < 50:
            return {"ram":ram_int}
        else:
            dispatcher.utter_message(template="utter_wrong_ram")

            return {"ram":None}

    def validate_camera(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            camera_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            camera_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if camera_int < 150:
            return {"camera":camera_int}
        else:
            dispatcher.utter_message(template="utter_wrong_camera")

            return {"camera":None}

    def validate_budget(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        # i want the ram
        try:
            budget_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            budget_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if budget_int < 4000:
            return {"budget":budget_int}
        else:
            dispatcher.utter_message(template="utter_wrong_budget")

            return {"budget":None}

    def validate_battery(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""
        #4 GB RAM
        # 10 GB RAM --> integers/number from this -- 10
        #
        try:
            battery_int = int(re.findall(r'[0-9]+',value)[0])
        except:
            battery_int = 500000
        #Query the DB and check the max value, that way it can be dynamic
        if battery_int < 8000:
            return {"battery":battery_int}
        else:
            dispatcher.utter_message(template="utter_wrong_battery")

            return {"battery":None}


    
    # USED FOR DOCS: do not rename without updating in docs
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        if tracker.get_slot('category') == 'phone':
            dispatcher.utter_message(text="Please find your searched items here......... Phones..")

        elif tracker.get_slot('category') == 'laptop':
            dispatcher.utter_message(text="Please find your searched items here......... Laptops..")

        category = tracker.get_slot('category')
        # Open database connection

        ram = tracker.get_slot('ram')
        battery = tracker.get_slot('battery')
        battery_backup = tracker.get_slot('battery_backup')
        storage_capacity = tracker.get_slot('storage_capacity')
        camera = tracker.get_slot('camera')
        budget = tracker.get_slot('budget')

        # prepare a cursor object using cursor() method
        #product_name    product_url product_description image_url
        if category == 'phone':
            r = db.products.find({"subCategory":"phone"})
            products = []

            for p in r:
                
                d = p["information"]

        

                if (d["ram"] >= ram and d["battery"]>= battery and d["camera"]>= camera and d["price"]<= budget):
                    products.append(
                       (
                           d["product_url"],
                           d["image_url"],
                           d["title"]
                       )
                    )
                

        elif category == 'laptop':
            r = db.products.find({"subCategory":"laptop"})
            products = []

            for p in r:
                d = p["information"]

                if (d["ram"] >= ram and d["battery_backup"]>= battery_backup and d["storage"]>= storage_capacity and d["price"]<= budget):
                    products.append(
                       (
                           d["product_url"],
                           d["image_url"],
                           d["title"]
                       )
                    )

        if len(products) != 0:
            test_carousel = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
    
       {
                    "title": str(x[2]),
                    "subtitle": category,
                    "image_url": str(x[1]),
                    "buttons": [{
                        "title": "Buy Now",
                        "url": str(x[0]),
                        "type": "web_url"
                    }
                       
                    ]
                }
    

    for x in products
]
            }
        }
            dispatcher.utter_message(attachment=test_carousel)
        else:
            dispatcher.utter_message(text="Looks like there aren't any products that match your search.")
        dispatcher.utter_message(template='utter_select_next')

        return [SlotSet('ram',None),SlotSet('camera',None),SlotSet('battery_backup',None),\
        SlotSet('battery',None),SlotSet('storage_capacity',None),SlotSet('budget',None)]

class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_fallback")

        return []

class YourResidence(Action):

    def name(self) -> Text:
        return "action_your_residence"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        dispatcher.utter_message(template="utter_residence")

        return [UserUtteranceReverted(),FollowupAction(tracker.active_form.get('name'))]

def extract_metadata_from_tracker(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']

class OrderLookup(Action):

    def name(self) -> Text:
        return "action_order_lookup"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done
        userid = (extract_metadata_from_tracker(tracker)['userid'])
        
        orders = db.orders.find({"userId":ObjectId(userid)})

        order_list = []

        for order in orders:
            for item in order["items"]:
                    product_id  = item["productId"]
                    print(product_id)
                    product = db.products.find_one(ObjectId(product_id))
                    
                    order_list.append((str(item.get("_id")),product["productName"],product["information"]["image_url"]))
                    

        if len(order_list) !=0:
            test_carousel = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
    
       {
                    "title": str(x[0]),
                    "subtitle": str(x[1]),
                    "image_url": str(x[2]),
                    "buttons": [{
                        "title": f"Order Details",
                        "type":"postback",
                        "payload":f"/order_details{{\"order_id\":\"{str(x[0])}\"}}"
                    },
                    {
                        "title": f"Update Quantities",
                        "type":"postback",
                        "payload":f"/order_update_quantity{{\"order_id\":\"{str(x[0])}\"}}"
                    },
                    {
                        "title": f"Cancel Order",
                        "type":"postback",
                        "payload":f"/order_cancel{{\"order_id\":\"{str(x[0])}\"}}"
                    }
                       
                    ]
                }
    

    for x in order_list
]
            }
        }
            dispatcher.utter_message(attachment=test_carousel,text="Please Select Your Order.")
        
        else:
            dispatcher.utter_message(text="Looks like there aren't any orders here.")
            dispatcher.utter_message(template='utter_select_next')



        return []
    

    

# class ActionChangeQuantity(Action):

#     def name(self) -> Text:
#         return "action_update_quantity"

#     def run(self, dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         #Calling the DB
#         #calling an API
#         # do anything
#         #all caluculations are done
#         print("Ac")

#         userid = (extract_metadata_from_tracker(tracker)['userid'])
#         order_id = tracker.get_slot("order_id")
#         product_id = tracker.get_Slot("product_id")
#         quantity = tracker.get_slot("quantity")
        
#         order = db.orders.find({"userId":ObjectId(userid),"_id":ObjectId(order_id)})

#         for item in order:

#             if item["productId"] == product_id:
#                 pq = item["quantity"]
#                 item["quantity"] = quantity
#                 order["total"] = order["total"] + (quantity - pq)*item["price"]
        
#         dispatcher.utter_message(text="Order Quantity Updated.")
#         dispatcher.utter_message(template='utter_select_next')

class ActionDetails(Action):

    def name(self) -> Text:
        return "action_order_details"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Calling the DB
        #calling an API
        # do anything
        #all caluculations are done

        order_id = tracker.get_slot("order_id")
        userid = (extract_metadata_from_tracker(tracker)['userid'])

        orders = db.orders.find({"userId":ObjectId(userid)})

        flag = False

        for order in orders:

            for item in order["items"]:

                if item.get("_id") == ObjectId(order_id):

                    quantity = int (item["quantity"])
                    unit_price = int (item["price"])
                    product_name = item["productName"]
                    payment_mode = order["paymentType"]
                    address = order["mapAddress"]

                    flag = True
                    break

            if flag: break
        
        

        dispatcher.utter_message(text=f"Product Name : {product_name}")
        dispatcher.utter_message(text=f"Total Quantity : {quantity}")
        dispatcher.utter_message(text=f"Unit Price : {unit_price}")
        dispatcher.utter_message(text=f"Total Cost : {quantity * unit_price}")
        dispatcher.utter_message(text=f"Payment Mode : {payment_mode}")
        dispatcher.utter_message(text=f"Delivery Address : {address}")

        return []


class ActionDelete(Action):

    def name(self) -> Text:
        return "action_order_cancel"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        userid = (extract_metadata_from_tracker(tracker)['userid'])

        orders = db.orders.find({"userId":ObjectId(userid)})

        flag = False

        for order in orders:

            for item in order["items"]:

                if item.get("_id") == ObjectId(order_id):

                    order["total"] = int(order["total"]) - (int (item["quantity"]) * int(item["price"]))

                    order["items"].remove(item)
                    db.orders.replace_one({"_id":ObjectId(order.get("_id"))},order)
                    flag = True

                    if order["total"] == 0:
                        db.orders.delete_one(order)
                    break

            
            if flag : break
        
        dispatcher.utter_message(text="Order Cancelled Successfully.")
                








        









