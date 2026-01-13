import json
import unittest
import datetime

# -------------------------------------------------
# Load input JSON files and expected output
# -------------------------------------------------
# data-1.json  -> telemetry format 1
# data-2.json  -> telemetry format 2
# data-result.json -> unified expected output

with open("./data-1.json", "r", encoding="utf8") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r", encoding="utf8") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r", encoding="utf8") as f:
    jsonExpectedResult = json.load(f)


# -------------------------------------------------
# Convert telemetry data from Format 1
# -------------------------------------------------
def convertFromFormat1(jsonObject):
    """
    Format 1 characteristics:
    - Location is a single string separated by '/'
    - Timestamp is already in milliseconds
    - Device details are at top level
    """

    # Split location string into individual parts
    # Example: "Japan/Tokyo/Area-1/Factory-2/Section-A"
    location_parts = jsonObject["location"].split("/")

    # Create unified output structure
    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],

        # Timestamp already matches required format (milliseconds)
        "timestamp": jsonObject["timestamp"],

        # Map location values after splitting
        "location": {
            "country": location_parts[0],
            "city": location_parts[1],
            "area": location_parts[2],
            "factory": location_parts[3],
            "section": location_parts[4]
        },

        # Rename fields to match unified format
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# -------------------------------------------------
# Convert telemetry data from Format 2
# -------------------------------------------------
def convertFromFormat2(jsonObject):
    """
    Format 2 characteristics:
    - Timestamp is in ISO 8601 string format
    - Device details are nested inside 'device'
    - Location fields are already separated
    """

    # Convert ISO timestamp to datetime object
    date_obj = datetime.datetime.strptime(
        jsonObject["timestamp"],
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    # Convert datetime to milliseconds since Unix epoch
    timestamp_in_ms = int(
        (date_obj - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
    )

    # Create unified output structure
    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp_in_ms,

        # Location data already matches required structure
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },

        # Data section already matches expected format
        "data": jsonObject["data"]
    }

    return result


# -------------------------------------------------
# Main function to detect format and convert
# -------------------------------------------------
def main(jsonObject):
    """
    Determines the input data format and converts it
    to the unified telemetry structure
    """

    # If 'device' key exists, it is Format 2
    # Otherwise, it is Format 1
    if jsonObject.get("device"):
        return convertFromFormat2(jsonObject)

    return convertFromFormat1(jsonObject)


# -------------------------------------------------
# Unit Tests (provided by the task)
# -------------------------------------------------
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        # Basic sanity check
        self.assertEqual(jsonExpectedResult, jsonExpectedResult)

    def test_dataType1(self):
        # Validate conversion from Format 1
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult,
                         "Conversion from Format 1 failed")

    def test_dataType2(self):
        # Validate conversion from Format 2
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult,
                         "Conversion from Format 2 failed")


# Run tests
if __name__ == "__main__":
    unittest.main()
