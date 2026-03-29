"""
payload for opers
"""

def localoperator(country_ids=None):
    return {
        "col1" : "value1",
        "col2" : "value2",
        "col3" : {
            "col3col1" : 5,
            "col3col2" : "value32"
        },
        "country" : {
            "countryId" : country_ids['rus_id'],
            "countryName" : "Russia"
        }
    }

def oper_praqe(country_ids=None):
    return {
        "col1": "value1",
        "col2": "value2",
        "col3": {
            "col3col1": 5,
            "col3col2": "value32"
        },
        "country": {
            "countryId": country_ids['mld_id'],
            "countryName": "Moldova"
        }
    }