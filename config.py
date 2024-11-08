
# Location for job search
location = ["London", "Manchester"]  # Example locations
  
# Filters for job search
filters = {
    "salary_from":10000 ,        # Minimum salary or None
    "salary_to": 80000,          # Maximum salary or None
    "date_created_offset": "lasttwoweeks",  # Options: "today", "lastthreedays", "lastweek", "lasttwoweeks", or None
    "proximity": None,            # Proximity in miles (e.g., 30 miles from the location)
    "easy_apply": True,          # Whether to filter for easy apply jobs
    "max_applicants": None,       # Maximum applicants filter (optional) or None
    "keywords": ["ETL developer","Data engineer"]
         
}

target_currency = "MAD" # Options : Your Local Currency like EUR - CHF - MAD  ...... or NONE ---> Pound
