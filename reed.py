#author : Saad HAJARI 
#mail : saadhaajri10@gmail.com

import requests
from lxml import html, etree
import csv
import json  # Import json for JSON output
import config  # Import your config file
from datetime import datetime  # Import datetime for unique filenames

# API for exchange rates
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/"
BASE_CURRENCY = "GBP"  # Assume salaries are initially in GBP

def fetch_exchange_rates(base_currency=BASE_CURRENCY):
    """
    Fetches the exchange rates from the API.
    """
    try:
        response = requests.get(f"{EXCHANGE_RATE_API_URL}{base_currency}")
        response.raise_for_status()  # Check for request errors
        return response.json().get("rates")
    except requests.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    """
    Converts an amount from one currency to another using the given rates.
    """
    if to_currency is None or from_currency == to_currency or not rates:
        return amount  # No conversion needed if target currency is None, same currency, or no rates available

    # Convert from the source currency to the base currency (e.g., GBP)
    base_amount = amount / rates[from_currency]

    # Convert from base currency to target currency
    converted_amount = base_amount * rates[to_currency]
    return round(converted_amount, 2)


def extract_and_convert_salary(salary_text, rates):
    """
    Extracts salary from a text string, handles ranges, and converts them to the target currency.
    """
    salary_converted = salary_text  # Default to original if not convertible
    try:
        if 'per annum' in salary_text:
            # Remove currency symbol, 'per annum', and commas
            salary_text = salary_text.replace('£', '').replace(',', '').replace(' per annum', '')

            # Check if it's a range (e.g., '£65,000 - £74,000')
            if ' - ' in salary_text:
                salary_range = salary_text.split(' - ')
                salary_from = float(salary_range[0])
                salary_to = float(salary_range[1])

                # Convert both salary_from and salary_to if target currency is set
                if config.target_currency:
                    salary_from_converted = convert_currency(salary_from, BASE_CURRENCY, config.target_currency, rates)
                    salary_to_converted = convert_currency(salary_to, BASE_CURRENCY, config.target_currency, rates)
                    salary_converted = f"{config.target_currency} {salary_from_converted} - {salary_to_converted}"
                else:
                    salary_converted = f"£{salary_from} - £{salary_to}"
            else:
                # Convert single salary value if target currency is set
                salary_value = float(salary_text)
                if config.target_currency:
                    salary_converted = f"{config.target_currency} {convert_currency(salary_value, BASE_CURRENCY, config.target_currency, rates)}"
                else:
                    salary_converted = f"£{salary_value}"

    except (ValueError, IndexError):
        print(f"Skipping salary conversion for: {salary_text}")

    return salary_converted

def fetch_job_details(job_title, location, page_number, filters, root, json_jobs, rates):
    # Loop over each keyword and fetch results for each one
    for keyword in filters["keywords"]:
        # Construct the base URL dynamically using the job_title, keyword, and location
        base_url = f"https://www.reed.co.uk/jobs/{keyword.replace(' ', '-').lower()}-jobs-in-{location}"
        url = f'{base_url}?pageno={page_number}'

        # Add filters to the URL if specified
        if filters["salary_from"] is not None:
            url += f'&salaryFrom={filters["salary_from"]}'
        if filters["salary_to"] is not None:
            url += f'&salaryTo={filters["salary_to"]}'
        if filters["date_created_offset"] is not None:
            url += f'&dateCreatedOffSet={filters["date_created_offset"]}'
        if filters["proximity"] is not None:
            url += f'&proximity={filters["proximity"]}'
        if filters["easy_apply"]:
            url += '&isEasyApply=true'
        if filters.get("max_applicants") is not None:
            url += f'&maxApplicants={filters["max_applicants"]}'

        # Log the generated URL to a .txt file
        with open(f"generated_urls_{datetime.now().strftime('%Y-%m-%d')}.txt", 'a') as file:
            file.write(url + "\n")

        # Sending the request to get the page content
        response = requests.get(url)
        tree = html.fromstring(response.content)

        # XPath expressions for extracting different details
        job_title_xpath = "//button[@class='job-card_jobTitleBtn__block__ZeEY5 btn btn-link']/text()"
        salary_xpath = "//li[contains(text(),'per annum')]/text()"
        location_xpath = "//li[contains(@data-qa, 'job-card-location')]/text()"
        company_xpath = "//a[contains(@class, 'gtmJobListingPostedBy')]/text()"
        description_xpath = "//div[@class='job-card_jobResultDescription__GaA48']/p/text()"
        easy_apply_xpath = "//label[contains(@class, 'index-module_label__easyApply__RxLXy')]"
        contract_type_xpath = "//li[contains(text(),'Permanent') or contains(text(),'Contract')]/text()"

        # Extracting the job listings
        job_titles = tree.xpath(job_title_xpath)
        salaries = tree.xpath(salary_xpath)
        locations = tree.xpath(location_xpath)
        companies = tree.xpath(company_xpath)
        descriptions = tree.xpath(description_xpath)
        contract_types = tree.xpath(contract_type_xpath)
        easy_apply_list = tree.xpath(easy_apply_xpath)
        

        # Loop through all job listings on the page
        for i in range(len(job_titles)):
            job_title_text = job_titles[i].strip() if i < len(job_titles) else 'Not Found'
            salary_text = salaries[i].strip() if i < len(salaries) else 'Not Found'
            location = locations[i].strip() if i < len(locations) else 'Not Found'
            company = companies[i].strip() if i < len(companies) else 'Not Found'
            description = descriptions[i].strip() if i < len(descriptions) else 'Not Found'
            contract_type = contract_types[i].strip() if i < len(contract_types) else 'Not Found'
            easy_apply = "Yes" if easy_apply_list and i < len(easy_apply_list) else "No"
            

            # Convert the salary to the target currency if applicable
            salary_converted = extract_and_convert_salary(salary_text, rates)

            # Append to JSON job list
            json_jobs.append({
                "Job Title": job_title_text,
                "Salary": salary_converted,
                "Location": location,
                "Company": company,
                "Description": description,
                "Contract Type": contract_type,
                "Easy Apply": easy_apply
                
            })

            # Create dictionary for CSV and XML
            job_elem = etree.SubElement(root, "job")
            etree.SubElement(job_elem, "title").text = job_title_text
            etree.SubElement(job_elem, "salary").text = salary_converted
            etree.SubElement(job_elem, "location").text = location
            etree.SubElement(job_elem, "company").text = company
            etree.SubElement(job_elem, "description").text = description
            etree.SubElement(job_elem, "contract_type").text = contract_type
            etree.SubElement(job_elem, "easy_apply").text = easy_apply
            print("-" * 40)

# Main scraping function
def scrape_jobs(locations, filters, pages_to_scrape=1):
    root = etree.Element("jobs")  # Root element for XML (initialized only once)
    json_jobs = []  # List to store jobs in JSON format
    rates = fetch_exchange_rates()  # Fetch exchange rates only once

    # Loop through each location in the list of locations
    for location in locations:
        print(f"Scraping jobs for location: {location}")

        # Loop through pages correctly
        for page in range(1, pages_to_scrape + 1):
            print(f"Scraping page {page} for location {location}...")
            fetch_job_details("", location, page, filters, root, json_jobs, rates)

    # Generate the filename with today's date
    today = datetime.now().strftime('%Y-%m-%d')

    # Save to CSV after collecting data
    with open(f"job_listings_{today}.csv", mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Writing header if the file is empty
            writer.writerow(["Job Title", "Salary", "Location", "Company", "Description","Contract" ,"Easy Apply"])


        # Writing rows from the root (which contains all job elements)
        for job_elem in root:

            writer.writerow([ 
            job_elem.find("title").text if job_elem.find("title") is not None else 'N/A',
            job_elem.find("salary").text if job_elem.find("salary") is not None else 'N/A',
            job_elem.find("location").text if job_elem.find("location") is not None else 'N/A',
            job_elem.find("company").text if job_elem.find("company") is not None else 'N/A',
            job_elem.find("description").text if job_elem.find("description") is not None else 'N/A',
            job_elem.find("contract_type").text if job_elem.find("contract_type") is not None else 'N/A',
            job_elem.find("easy_apply").text if job_elem.find("easy_apply") is not None else 'N/A'
        ])

    # Save to XML after collecting data
    tree = etree.ElementTree(root)
    with open(f"job_listings_{today}.xml", mode='wb') as file:
        tree.write(file, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    # Save to JSON after collecting data
    with open(f"job_listings_{today}.json", mode='w', encoding='utf-8') as file:
        json.dump(json_jobs, file, indent=4)

    print(f"Scraping completed and saved to files.")

# Example usage with specific filters and keywords from config.py
scrape_jobs(
    locations=config.location,  # Locations list from config.py
    filters=config.filters,  # Filters from config.py
    pages_to_scrape=3  # Scrape 3 pages for each location
)
