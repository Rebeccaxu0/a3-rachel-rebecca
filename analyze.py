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


# def build_medals_json(csv_path, output_path):
#     # Dictionary of years → country → medal count
#     medals_by_year = defaultdict(lambda: defaultdict(int))

#     # Dictionary for total medals across all years
#     total_medals = defaultdict(int)

#     with open(csv_path, newline='', encoding="utf-8") as f:
#         reader = csv.DictReader(f)

#         for row in reader:
#             year = row["Year"].strip()
#             country = row["Country"].strip()
#             medal = row["Medal"].strip()

#             # Only count rows that actually have a medal
#             if medal not in ("Gold", "Silver", "Bronze"):
#                 continue

#             # Update counts
#             medals_by_year[year][country] += 1
#             total_medals[country] += 1

#     # Convert nested dicts → target JSON format
#     output = {}

#     # Year-by-year
#     for year, country_counts in medals_by_year.items():
#         output[year] = [
#             {"country": country, "medals": count}
#             for country, count in sorted(country_counts.items(), key=lambda x: -x[1])
#         ]

#     # Add all-years totals
#     output["all_years"] = [
#         {"country": country, "medals": count}
#         for country, count in sorted(total_medals.items(), key=lambda x: -x[1])
#     ]

#     # Save JSON
#     with open(output_path, "w", encoding="utf-8") as out:
#         json.dump(output, out, indent=2)

#     print(f"Successfully created {output_path}")


# if __name__ == "__main__":
#     build_medals_json("summer.csv", "medals.json")


# CSV_FILE = "summer.csv"
# OUTPUT_JSON = "events.json"

# def load_csv(csv_file):
#     """
#     Load CSV data into a list of dictionaries.
#     """
#     data = []
#     with open(csv_file, newline='', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             if row['Medal']:  # Only include rows with medals
#                 data.append({
#                     "Year": int(row['Year']),
#                     "Country": row['Country'],
#                     "Event": row['Discipline']
#                 })
#     return data

# def aggregate_medals(data):
#     """
#     Aggregate number of medals per event, per year, per country.
#     Returns a dict like:
#     {
#         "100m Men": [
#             {"year": 2020, "country": "USA", "medals": 2},
#             {"year": 2016, "country": "GBR", "medals": 1},
#         ],
#         ...
#     }
#     """
#     agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
#     for row in data:
#         event = row['Event']
#         year = row['Year']
#         country = row['Country']
#         agg[event][year][country] += 1

#     result = {}
#     for event, years in agg.items():
#         result[event] = []
#         for year, countries in years.items():
#             for country, medals in countries.items():
#                 result[event].append({
#                     "year": year,
#                     "country": country,
#                     "medals": medals
#                 })
#     return result

# def save_json(data, output_file):
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)

# if __name__ == "__main__":
#     data = load_csv(CSV_FILE)
#     aggregated_data = aggregate_medals(data)
#     save_json(aggregated_data, OUTPUT_JSON)


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
            sport = row["Discipline"].strip()
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
