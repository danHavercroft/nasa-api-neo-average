from numpy import average
import requests, statistics

if __name__ == "__main__":
    # Take inputs of the dates to check and API key
    start_date = input("Enter start date: ")
    end_date = input("Enter end date: ")
    api_key = input("Enter API key: ")

    # Make the request to the API
    api_request = requests.get("https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key={}".format(start_date, end_date, api_key))
    
    # Check response has a status code of 200
    if api_request.status_code != 200:
        print("There was an error fetching data from the API. See reason below: ")
        print(api_request.content)
    else:
        print("Data fetched from API successfully...")
        print()

    # Parse JSON to get the data
    data = api_request.json()

    # Get the total number of NEOs
    total_neos = data["element_count"]
    
    # Get a list of the days in the response
    days_to_parse = data["near_earth_objects"].keys()

    #Create empty list to store the average size of each NEO
    average_neo_sizes = []

    # Nested for loop to run through each of the days and each of the NEOs on that day
    for day in days_to_parse:
        day_neos = data["near_earth_objects"][day]
        
        for neo in day_neos:
            estimated_diameter_min = neo["estimated_diameter"]["meters"]["estimated_diameter_min"]
            estimated_diameter_max = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]

            # Average the size estimate
            average_estimated_diameter = (estimated_diameter_min + estimated_diameter_max) / 2

            # Add that size to the list of NEO sizes
            average_neo_sizes.append(average_estimated_diameter)

    # Summarise the data with an output
    print("There were a total of {} NEOs between {} and {}.".format(total_neos, start_date, end_date))
    print("The average size of an NEO between {} and {} was: {}".format(start_date, end_date, statistics.mean(average_neo_sizes)))