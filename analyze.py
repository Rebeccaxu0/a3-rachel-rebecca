import csv
import json
from collections import defaultdict, Counter

# CITY_COORDS = {
#     "London":       {"lat": 51.5074,  "lon": -0.1278},
#     "Rome":         {"lat": 41.9028,  "lon": 12.4964},
#     "Helsinki":     {"lat": 60.1699,  "lon": 24.9384},
#     "Antwerp":      {"lat": 51.2600,  "lon": 4.4028},
#     "Beijing":      {"lat": 39.9042,  "lon": 116.4074},
#     "Tokyo":        {"lat": 35.6762,  "lon": 139.6503},
#     "Amsterdam":    {"lat": 52.3676,  "lon": 4.9041},
#     "Montreal":     {"lat": 45.5017,  "lon": -73.5673},
#     "Mexico":       {"lat": 19.4326,  "lon": -99.1332},  # Mexico City
#     "Sydney":       {"lat": -33.8688, "lon": 151.2093},
#     "Barcelona":    {"lat": 41.3874,  "lon": 2.1686},
#     "Atlanta":      {"lat": 33.7490,  "lon": -84.3880},
#     "St Louis":     {"lat": 38.6270,  "lon": -90.1994},
#     "Munich":       {"lat": 48.1351,  "lon": 11.5820},
#     "Stockholm":    {"lat": 59.3293,  "lon": 18.0686},
#     "Moscow":       {"lat": 55.7558,  "lon": 37.6173},
#     "Paris":        {"lat": 48.8566,  "lon": 2.3522},
#     "Athens":       {"lat": 37.9838,  "lon": 23.7275},
#     "Seoul":        {"lat": 37.5665,  "lon": 126.9780},
#     "Los Angeles":  {"lat": 34.0522,  "lon": -118.2437},
#     "Berlin":       {"lat": 52.5200,  "lon": 13.4050},
#     "Melbourne / Stockholm": { "lat": -37.8136, "lon": 144.9631 }
# }

# city_years = defaultdict(set)

# with open("summer.csv", newline="", encoding="utf-8") as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         city = row["City"]
#         year = row["Year"]
#         city_years[city].add(year)

# output = []

# for city, years in city_years.items():
#     coords = CITY_COORDS.get(city, {"lat": None, "lon": None})
#     output.append({
#         "city": city,
#         "years": sorted(list(years)),
#         "lat": coords["lat"],
#         "lon": coords["lon"]
#     })


# with open("centroids.json", "w", encoding="utf-8") as f:
#     json.dump(output, f, indent=4)


def build_years_json(csv_path, outfile):
    # Dictionary: country → year → medal counts
    years = defaultdict(lambda: defaultdict(lambda: {
        "country": None,
        "sport": None,
        "bronze": 0,
        "silver": 0,
        "gold": 0
    }))

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            year = int(row["Year"].strip())
            country = row["Country"].strip()
            sport = row["Sport"].strip()
            medal = row["Medal"].strip().lower()

            # Skip invalid medals
            if medal not in ("gold", "silver", "bronze"):
                continue
            
            key = (country, sport)

            entry = years[year][key]
            entry["country"] = country
            entry["sport"] = sport
            entry[medal] += 1

    # Convert to country → list of yearly dicts
    final = {}
    for year, entries in years.items():
        final[year] = list(entries.values())

    # Write JSON
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4)

if __name__ == "__main__":
    build_years_json("summer.csv", "years.json")

def build_countries_json(csv_path, outfile):
    countries = defaultdict(lambda: defaultdict(lambda: {
        "year": None,
        "sport": None,
        "bronze": 0,
        "silver": 0,
        "gold": 0
    }))

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            year = int(row["Year"].strip())
            country = row["Country"].strip()
            sport = row["Sport"].strip()
            medal = row["Medal"].strip().lower()

            # Skip invalid medals
            if medal not in ("gold", "silver", "bronze"):
                continue
            
            key = (year, sport)

            entry = countries[country][key]
            entry["year"] = year
            entry["sport"] = sport
            entry[medal] += 1

    # Convert to country → list of yearly dicts
    final = {}
    for country, entries in countries.items():
        final[country] = list(entries.values())

    # Write JSON
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4)

if __name__ == "__main__":
    build_countries_json("summer.csv", "countries.json")


def build_events_json(csv_path, outfile):
    # Dictionary: country → year → medal counts
    events = defaultdict(lambda: defaultdict(lambda: {
        "year": None,
        "country": None,
        "bronze": 0,
        "silver": 0,
        "gold": 0
    }))

    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            year = int(row["Year"].strip())
            country = row["Country"].strip()
            sport = row["Sport"].strip()
            medal = row["Medal"].strip().lower()

            # Skip invalid medals
            if medal not in ("gold", "silver", "bronze"):
                continue

            key = (year, country) 
            entry = events[sport][key]
            entry["year"] = year
            entry["country"] = country
            entry[medal] += 1

    # Convert inner defaultdicts to lists
    final = {}
    for event, entries in events.items():
        final[event] = list(entries.values())

    # Write JSON
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4)

if __name__ == "__main__":
    build_events_json("summer.csv", "events.json")


INPUT_CSV = "summer.csv"
OUTPUT_JSON = "athletes.json"

def build_athlete_medal_json(csv_file=INPUT_CSV, outfile=OUTPUT_JSON):
    # Structure:
    # athletes[athlete][(sport, year, country)] = {sport, year, country, bronze, silver, gold}
    athletes = defaultdict(lambda: defaultdict(lambda: {
        "sport": None,
        "year": None,
        "country": None,
        "bronze": 0,
        "silver": 0,
        "gold": 0
    }))

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            athlete = row["Athlete"].strip()
            if "," in athlete:
                last, first_middle = athlete.split(",", 1)
                first = first_middle.strip().split()[0]  # take only first name
                first = first.capitalize()  # capitalize first letter of first name
                last = last.strip().capitalize()  # capitalize first letter of last name
                athlete = f"{first} {last}"
            else:
                athlete = athlete
            sport = row["Sport"].strip()
            year = int(row["Year"])
            country = row["Country"].strip()
            medal = row["Medal"].strip().lower()

            # Skip if no medal
            if medal not in ("gold", "silver", "bronze"):
                continue

            key = (sport, year, country)  # Unique per athlete

            entry = athletes[athlete][key]

            # Fill descriptive fields once
            entry["sport"] = sport
            entry["year"] = year
            entry["country"] = country

            # Increment medal
            entry[medal] += 1

    # Convert inner defaultdicts to lists
    final = {}
    for athlete, entries in athletes.items():
        final[athlete] = list(entries.values())

    # Write JSON
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4)

    print(f"Created {outfile} with {len(final)} athletes.")


if __name__ == "__main__":
    build_athlete_medal_json()