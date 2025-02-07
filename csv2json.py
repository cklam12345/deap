import sys
import csv
import json

def csv_to_json(csv_file, json_file):
  """
  This function converts a CSV file to a JSON file.

  Args:
      csv_file: The path to the CSV file.
      json_file: The path to the output JSON file.
  """
  try:
    # Open the CSV file for reading
    with open(csv_file, 'r') as csvfile:
      # Create a CSV reader object
      reader = csv.DictReader(csvfile)

      # Initialize an empty list to store data
      data = []

      # Read each row from the CSV file
      for row in reader:
        # Append the row (dictionary) to the data list
        data.append(row)

    # Open the JSON file for writing
    with open(json_file, 'w') as jsonfile:
      # Write the data list (converted to JSON format) to the file
      json.dump(data, jsonfile, indent=4)

  except FileNotFoundError:
    print(f"Error: CSV file '{csv_file}' not found.")

  except Exception as e:
    print(f"Error converting CSV to JSON: {e}")

# Get the CSV file path from the command line argument (assuming it's the first argument)
csv_file = sys.argv[1]

# Define the output JSON file name (you can change this)
json_file = "inventory.json"

# Call the csv_to_json function
csv_to_json(csv_file, json_file)

print(f"CSV file '{csv_file}' converted to JSON file '{json_file}'.")

