import csv
import re
from collections import defaultdict


class GeoExtraction:
    def __init__(self):
        file_name = "./GeoExtraction/us_cities_states_counties.csv"
        file_name = "./GeoExtraction/canada_cities.csv"
        self.cities, self.states_abbrev, self.states_full, self.counties, self.city_aliases = list(), list(), list(), list(), list()
        with open(file_name) as file:
            file = csv.reader(file)
            next(file)  # skip the header
            for row in file:
                if len(row) > 1:
                    row = [', '.join(row)]

                city, state_abbrev, state_full, county, city_alias = row[0].split("|")
                self.cities.append(city)
                self.states_abbrev.append(state_abbrev)
                self.states_full.append(state_full)
                self.counties.append(county)
                self.city_aliases.append(city_alias)

    def extract_location(self, s):
        location = defaultdict(set)

        for city in self.cities:
            pattern1 = "(?i)[\s\W]+" + city + "$"
            pattern2 = "(?i)^" + city + "$"
            pattern3 = "(?i)^" + city + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + city + "[\s\W]+"
            if re.search(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, s):
                location["city"].add(city)

        for state in self.states_full:
            pattern1 = "(?i)[\s\W]+" + state + "$"
            pattern2 = "(?i)^" + state + "$"
            pattern3 = "(?i)^" + state + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + state + "[\s\W]+"
            if re.search(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, s):
                location["state"].add(state)

        for i, state in enumerate(self.states_abbrev):
            pattern1 = "(?i)[\s\W]+" + state + "$"
            pattern2 = "(?i)^" + state + "$"
            pattern3 = "(?i)^" + state + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + state + "[\s\W]+"
            if re.search(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, s):
                location["state"].add(self.states_full[i])

        for county in self.counties:
            pattern1 = "(?i)[\s\W]+" + county + "$"
            pattern2 = "(?i)^" + county + "$"
            pattern3 = "(?i)^" + county + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + county + "[\s\W]+"
            if re.search(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, s):
                location["county"].add(county)

        for i, city in enumerate(self.city_aliases):
            pattern1 = "(?i)[\s\W]+" + city + "$"
            pattern2 = "(?i)^" + city + "$"
            pattern3 = "(?i)^" + city + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + city + "[\s\W]+"
            if re.search(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, s):
                location["city"].add(self.cities[i])

        if location:
            return location
        return None

    def remove_location(self, s):
        for city in self.cities:
            pattern1 = "(?i)[\s\W]+" + city + "$"
            pattern2 = "(?i)^" + city + "$"
            pattern3 = "(?i)^" + city + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + city + "[\s\W]+"
            s = re.sub(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, " ", s)

        for state in self.states_full:
            pattern1 = "(?i)[\s\W]+" + state + "$"
            pattern2 = "(?i)^" + state + "$"
            pattern3 = "(?i)^" + state + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + state + "[\s\W]+"
            s = re.sub(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, " ", s)

        for state in self.states_abbrev:
            pattern1 = "(?i)[\s\W]+" + state + "$"
            pattern2 = "(?i)^" + state + "$"
            pattern3 = "(?i)^" + state + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + state + "[\s\W]+"
            s = re.sub(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, " ", s)

        for county in self.counties:
            pattern1 = "(?i)[\s\W]+" + county + "$"
            pattern2 = "(?i)^" + county + "$"
            pattern3 = "(?i)^" + county + "[\s\W]+"
            pattern4 = "(?i)[\s\W]+" + county + "[\s\W]+"
            s = re.sub(pattern1 + "|" + pattern2 + "|" + pattern3 + "|" + pattern4, " ", s)

        return s







