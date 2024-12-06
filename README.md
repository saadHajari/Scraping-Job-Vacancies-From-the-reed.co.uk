# Job Scraper

This project is a web scraper for extracting job listings from reed.co.uk platforms reed it's a platform like **LinkedIn**, **Indeed**, **Glassdoor** , **Monster**  and other job sites. It collects data such as job title, salary, location, company, description, contract type, and easy-apply status. The data can be exported to CSV, XML, and JSON formats. Additionally, the tool supports salary conversion into different currencies using live exchange rates. It can be integrated into a **jobs bot** or **automator** to streamline job applications or job tracking.


![reed_pink](https://github.com/user-attachments/assets/84891cb2-741d-463e-b985-b8b125af9d17)

---

## Features

- **Extract Job Listings**: Fetches job listings from platforms like **LinkedIn**, **Indeed**, and others, based on specified keywords and location.
- **Currency Conversion**: Converts salary values from GBP to a target currency using live rates from the Exchange Rate API.
- **Flexible Filtering**: Allows custom filters such as salary range, posting date, and easy-apply status.
- **Multiple Export Formats**: Saves extracted job data into **CSV**, **XML**, and **JSON** files.
- **URL Logging**: Logs generated URLs to a text file for reference and debugging.
- **Job Bot Integration**: Can be integrated with a **jobs bot** to automate job searching and application processes.
- **Automator Friendly**: Designed to be easily used in job automation pipelines, reducing the manual effort of tracking listings.

---

## Prerequisites

To set up the project, you’ll need:

- Python 3.6+
- Required libraries, which can be installed by running:

    ```bash
    pip install requests
    pip install lxml
    pip install configparser

    ```

- Configuration of the API and filters in `config.py`.

---

## Configuration

Edit the following parameters in `config.py`:

```python
# config.py

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

target_currency = None # Options : Your Local Currency like EUR - CHF - MAD  ...... or NONE ---> Pound
```
---

## Usage 
- To run the scraper, execute the main script:

```python
# reed.py 

python reed.py 
```

---
## This will:

- Fetch exchange rates.
- Scrape job details based on keywords and location.
- Convert salaries if a target currency is specified.
- Save job listings in **CSV**, **XML**, and **JSON** formats with a filename based on the current date.
- Optionally, automate job tracking or application processes using a **jobs bot**.

---
## Example Function Call:

- You can customize the main scrape_jobs function to scrape multiple pages and apply different filters:

```python
scrape_jobs(
    locations=config.location,  # Locations list from config.py
    filters=config.filters,  # Filters from config.py
    pages_to_scrape=3  # Scrape 3 pages for each location
)
```
---

## Output
The scraped data will be saved in the following formats:

- **job_listings_YYYY-MM-DD.csv**

- **job_listings_YYYY-MM-DD.xml**

- **job_listings_YYYY-MM-DD.json**


Each file will contain data on job listings, structured as per the export format.

**For Contact** : Send me an email in : **saadhajari10@gmail.com**

**You Can Buy Me a coffee Here** -----> **https://www.paypal.com/donate/?hosted_button_id=5URJR262Y77BQ**


| Feature Name                                           | Status   |
|--------------------------------------------------------|----------|
| Add Retry Logic for Network Requests                   | X        |
| Handle Pagination Automatically                        | X        |
| Enhanced Error Logging                                 | X        |
| Use Caching for Exchange Rates                         | X        |
| Additional Filters Based on Job Description or Contract Type | X        |
| Enhance Job Matching and Similarity Scoring            | X        |
| Add Job Post Date                                      | X        |
| Implement a Scheduler for Automatic Updates            | X        |
| Send Email Alerts for New Jobs                         | X        |
| Integrate Machine Learning to Predict Job Suitability  | X        |
| Search Information About the Company - his size .....  | X          |
| Link to a Database                                     | X          |
| Create a Dashboard with Filters                        | X          |
| Extract Job Listings                                   | ✅       |
| Currency Conversion                                    | ✅       |
| Flexible Filtering                                     | ✅       |
| Multiple Export Formats                                | ✅       |
| URL Logging                                            | ✅       |
| Job Bot Integration                                    | ✅       |
| Automator Friendly                                     | ✅       | 




