import pandas as pd
import requests
import json

# Read the CSV file into a DataFrame
df = pd.read_csv('Details.csv')

# Create an empty list to store the extracted rates
rates = []

# Create an empty dictionary to store the captured JSON
json_data = {}

# Iterate through the rows of the DataFrame
for _, row in df.iterrows():
    # Extract data from each row
    hotels_id = row['hotels_id']
    check_in = row['check-in']
    check_out = row['check-out']

    # Create the URL of the backend GET request the website is making to get the details for rooms (got this from inspecting the network traffic of the website during page reload)
    url = f"https://www.qantas.com/hotels/api/ui/properties/{hotels_id}/availability?checkIn={check_in}&checkOut={check_out}&adults=2&children=0&infants=0&payWith=cash"
    print(f"Constructed URL: {url}")

    # Define the headers, including the 'Referer'
    headers = {
        'Referer': url  # Add the Referer header
    }

    # Send an HTTP GET request with the specified headers for the Referer
    response = requests.get(url, headers=headers)


    if response.status_code == 200:

        # Parse the JSON content
        json_data = response.json()

        # Iterate over each room type to extract the room rates from the JSON data
        for room_type in json_data['roomTypes']:
            # Iterate over each offer within the room type
            for offer in room_type.get('offers', []):
                # Extract the desired information from the JSON file and create a rate dictionary
                rate = {
                    "Room_name": room_type.get("name"),
                    "Rate_name": offer.get("name"),
                    "Number_of_Guests": room_type.get("maxOccupantCount"),
                    "Cancellation_Policy": offer.get("cancellationPolicy", {}).get("description"),
                    "Price": offer.get("charges", {}).get("total", {}).get("amount"),
                    "Top_Deal": offer.get("promotion") is not None and offer.get("promotion").get("name", "") == "Top Deal",
                    "Currency": offer.get("charges", {}).get("total", {}).get("currency")
                }
                # Add the rate to the list of rates and convert it to JSON
                rates.append(json.dumps(rate))
                print(json.dumps(rate, indent=2, sort_keys=True))

    else:
        print(f"Error: Unable to fetch data. Status code {response.status_code}")