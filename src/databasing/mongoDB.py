"""
NOTE: You may skip this section and it should be generally easy to follow.
      Much of the documentation is a work in progress.
NOTE: It may be beneficial to make assembly units arrays to maintain order.
references:
    JSON: https://www.slideshare.net/jfox015/json-22195683

## Decimal or float because precision of decimal points matters.
## Geo_points can reference neighbourhood to estimate location.
investment_details:

        - _id : mls or duproprio id

        - Price: Asking Price,
            - Breakdown of costs

                - repair: regression model based on year built,
                        expense data, net price, inspection reports.

                - transfer: regression model based on neighbourhood/geopoints,
                            size, and asking price.

                - interest: based on sales times of other properties & 
                            current interest rates

                - sunker: sum of repair + transfer

item_details:
        - _id : mls or duproprio id


"""

"""
01 - These are the templates of sections for assembler.
"""

header_properties = { 
    "_id": string,
    "address": address,
    "year_built": int,
    "land_size": int,  # Lot dimensions and land size (between websites)
    "building_type": string or null,
    "property_type": string
    }

address = {"house_num": string or int32,
           "street": string,
           "neighbourhood": string or null,
           "city": string,
           "region": string,
           "geo_points": [{"lng": int, "lat": int}]}]

price = {"net": int,
         "gross": decimal or float,
         "tax": decimal or float} # calculated gst/qst



# tvm_estimations built up and sent sent down to investment_details
# where 3 time strategies are provided as estimates.

estimations = {"estimated_cost": {"repair": decimal or float,
                                  "transfer": decimal or float,
                                  "intrest": decimal or float,
                                  "sunken": decimal or float},
              {"estimated_profit": {"net": decimal or float,
                                    "gross": decimal or float,
                                    "tax": decimal or float}

#  time value of money (tvm) strategies
tvm_estimations = {"short": estimations,
                   "medium": estimations,
                   "long": estimations}

investment_details = {
    "_id": string, primary_key,
    "price": price,
    "money_estimations": {
                          "short": tvm_estimations.short
                          "medium": tvm_estimations.medium
                          "long": tvm_estimations.long
                         }
}   

home_unique_features = {
    # Unique features
    "bedrooms": int,
    "bathrooms": int,
    "additional": [  # programmatic list of dictionaries from
                     # with unstructured features. Experimental data
                    ]
}

plex_unique_featurs = {
    # TO-DO
}

# Referenc template -- No idea
ref = { 
    "local_logic": foreign_key,
    "building_inspection": foreign_key,
    "investment": investment_details
}

weather = {  
    # https://openweathermap.org/api
}

local_logic = {
    # https://www.locallogic.co/
}

google_places = {
    # https://developers.google.com/places/web-service/get-api-key
}

"""
02 - Examples of an assembled opportunity document
"""
"""
To be built by unpacking templates with assembler.
Home is the example.
"""
property_details = {
    # Header - To be "header"
    "_id": string,
    "address": address,
    "year_built": int,
    "land_size": int,  # Lot dimensions and land size (between websites)
    "building_type": string or null,
    "property_type": string,
    # Ref Template
    "local_logic": foreign key,
    "building_inspection": foreign key,
    "investment": investment_details
    # Unique features
    "bedrooms": int,
    "bathrooms": int,
    "additional": [  # programmatic list of dictionaries from
                     # with unstructured features. Experimental data
                    ]
    }


building_inspection = {  "date": # standard list for trained inspectors
                                 # used for acquisition and maintenace evaluations
                       }

"""
06 - Person Informations
"""
name_contact = {
               "name": {"first": string,
                        "last": string}},
               "contact": {"phone": int,
                           "emergency": int,
                           "cosigners_affiliates": string or null,
                           "email": string},
               "gender": {"male": bool,
                          "female": bool,
                          "other": bool},
}


"""
Delinquency count of off-time payments
low = paid within 3 weeks,
med = paid within 5 weeks,
high = paid within 8 weeks.
"""

tenant = {
        "ethnecity": string or null,
        "payment": {"rent": decimal or float,
                    "deilinquencies": [
                        "low_count": int,
                        "med_count": int,
                        "high_count": int,
                                ]},
        "complaints": [{"date": string}],
        "DOB": {
            "year": int,
            "month": int,
            "day": int
        }
        "relations": {"residences": int,
                      "partners": int,
                      "children": int,
                      "roomates": int,
                      "pets": {"cat": {"long_hair": int,
                                       "short_no_hair": int},
                               "dog": {"large": int,
                                       "medium": int,
                                       "small", int}}}
        "lease": {
            "date": # location reference to digital copy of lease
        }
        "credit_report": {
            "date": # references to secure copy of report from credit service
        }
}


tennant_profiles = {"_id": int, primary_key,
                    # name_contact template
                    "name": {"first": string,
                                "last": string}},
                    # address template
                    "address": {"house_num": string or int32,
                                "street": string,
                                "apartment": string,
                                "neighbourhood": string or null,
                                "city": string,
                                "region": string,
                                "geo_points": [{"lng": int, "lat": int}]},
                    # custom to tenant template
                    "ethnecity": string,
                    "payment": {"rent": decimal or float,
                                "deilinquencies": [
                                    "low_count": int,
                                    "med_count": int,
                                    "high_count": int,
                                ]},
                    "complaints": [{"date": string}],
                    "DOB": {
                        "year": int,
                        "month": int,
                        "day": int
                    }
                    "relations": {"residences": int,
                                  "partners": int,
                                  "children": int,
                                  "roomates": int,
                                  "pets": {"cat": {"long_hair": int,
                                                   "short_no_hair": int},
                                           "dog": {"large": int,
                                                   "medium": int,
                                                   "small", int}}}
                    "lease": {
                        "date": # location reference to digital copy of lease
                    }
                    "credit_report": {
                        "date": # references to secure copy of report from credit service
                    }
                    }

"""
07- Associates templates
"""
"""
services_transactions include services with type
as key and avg_leng per workorder/transaction.
"""
services_transactions= {
    "services": [{string: int}, {string: int}],
    "transactions": {"date": date,
                     "invoices": {"date": string,  # location to seperate storage
                                  "notes": string,
                                  "amount": decimal or float
                                  "cost_breakdown": {"materials": decimal or float,
                                                     "labour": decimal or float}},
                     "total_trans": int}
}

# Examples shown both as fully built and insertion.

construction_subs = {
    "company_name": string,
    "contact": {"phone": int,
                "email": string,
                "affiliates": string},
    # services_transactions template
    "services": [{"contractor": 2}],
    "transactions": {"date": date,
                     "invoices": {"date": string, 
                                  "notes": string,
                                  "amount": decimal or float},
                     "total_trans": int}
}

"""
area_focus is a string for 
neighbourhood/region and current + avg number of listings.
"""
realators = {
    # header:
    # name_contact
    "brokerage": string,
    "listings_count": { 
                        "activity":[{"year": ["month"]},{"year": [as int or string]} ]
                        "count": int,
                        "ranking": int
    }
    "area_focus": [{string: {'current': int,
                             'average': int}]
    "ethnecity": string or null,
    # services_transactions template

}
}