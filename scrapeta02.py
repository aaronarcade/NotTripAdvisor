"""
Scrape Trip Advisor
"""
from bs4 import BeautifulSoup
import os
import re
import requests
import sys

base_url = "https://www.tripadvisor.com/"

def get_html(rel_url):
    """Get the HTML text for f"{base_url}{rel_url}". Caches text in local file
    named rel_url, returns that text if file exists.
    """
    print("Fetching", f"{base_url}{rel_url}")
    if os.path.isfile(rel_url):
        html_text = open(rel_url).read()
        return html_text
    else:
        resp = requests.get(f"{base_url}{rel_url}")
        fout = open(rel_url, "wt")
        fout.write(resp.text)
        return resp.text

def extract_attraction_urls(rel_url):
    """Extract the attraction links from the TripAdvisor page listing
    attractions for the location indicated in rel_url
    """
    html_text = get_html(rel_url)
    soup = BeautifulSoup(html_text, 'html.parser')
    attraction_elems = soup.find_all("div",
                                     attrs={"class": "attraction_element"})
    attraction_urls = []
    for e in attraction_elems:
        url = e.find("div", attrs={"class": "listing_title"}).find("a").get("href")
        attraction_urls.append(url)
    return attraction_urls

def extract_attraction_info(rel_url):
    """Extract attraction name, description (overview) and address for
    attraction at f"{base_url}{rel_url}"
    """
    # YOUR CODE HERE - dummy values so that code runs as-is.
    # Write the code to scrape these data from the TripAdvisor page for this
    # attraction
    name = "DUMMY_NAME"
    description = "DUMMY_DESCRIPTION"
    address = "DUMMY_ADDRESS"
    return name, description, address

def cache_transit(transit_station, transit_stations):
    """Takes a transit_station dict of the form returned by a Google
    Places API request and a dictionary cache of previously retrieved
    transit stations.

    If transit_station is already in the transit_stations dict, simply
    return the key that maps to the existing transit_station from the
    dict and the (unmodified) transit_stations dict.

    If the transit_station is not yet in the transit_stations dict,
    add transit_station to the dict with an integer key one greater
    than the greatest key already in the dict. Return the integer key
    and the transit_stations dict.
    """
    for k, v in transit_stations.items():
        # Use the Google place_id to match places
        if v["place_id"] == transit_station["place_id"]:
            return k, transit_stations
    # If we fall out of the loop, transit_station was not in transit_stations
    new_key = 1 if len(transit_stations) == 0 else max(transit_stations.keys()) + 1
    transit_stations[new_key] = transit_station
    return new_key, transit_stations

def nearest_transit(transit_stations, address):
    """Use the Google Maps API to get the nearest transit station to
    address.  If the nearest transit station is in the
    transit_stations dict, simply return the id of that transit
    station (which is a key of the transit_stations dict). If the
    nearest transit station is not in the dict, add the station to the
    dict and return its id. Ids are sequential ints starting at 1.
    """
    # YOUR CODE HERE - write the code to use the Google Places API to
    # get transit stations near an address.
    # Remember you'll have to geocode the address first.

    # Once you geocode the address and request nearest transit station
    # (see homework description), you'll get a result with a list of
    # transit stations -- each transit station is in a dict. Assign
    # the first transit station (which is the nearest one) to the
    # variable nearest_transit (replace the dummy assignment below)
    nearest_transit = {
        'id': '9734ec111dac8c7a6dc3f2679f9071709520bbba',
        'name': 'Tour Eiffel',
        'place_id': 'ChIJ64R9a-Jv5kcR-BW0JxItLhI',
        'types': ['bus_station',
                  'transit_station',
                  'point_of_interest',
                  'establishment'],
        'vicinity': 'France'}

    return cache_transit(nearest_transit, transit_stations)

def sql_attraction_smt(name, description, address, transit_id):
    """Return a str containing an SQL insert statement that inserts
    the data passed to this function into a table named attraction.
    """
    # YOUR CODE HERE
    return f"DUMMY INSERT with {name}, {description}, {address}, {transit_id}"

def sql_transit_stmt(id, station):
    """Return a str containing an SQL insert statement that inserts
    the data passed to this function into a table named transit.
    """
    # YOUR CODE HERE
    return (f"DUMMY INSERT with " +
            f"{id}, {station['name']}, {station['types'][0]}, {station['place_id']}")

if __name__=="__main__":
    attractions_per_location = 3
    location_urls = [
        "Attractions-g187147-Activities-Paris_Ile_de_France.html"
        # Add additional destination cities of your choosing
    ]
    transit_stations = {}
    transit_stmts, att_stmts = "", ""
    for loc in location_urls:
        attraction_urls = extract_attraction_urls(loc)
        for att in attraction_urls[:3]:
            name, description, address = extract_attraction_info(att)
            transit_id, transit_stations = nearest_transit(transit_stations, address)
            att_stmts +=sql_attraction_smt(name, description,address,transit_id)
            att_stmts += "\n"
    for id, station in transit_stations.items():
        transit_stmts += sql_transit_stmt(id, station) + "\n"
    db_data_script = "use trip_planner;\n\n"+transit_stmts+"\n"+att_stmts+"\n"
    fout = open("attraction-data.sql", "wt")
    fout.write(db_data_script)
