import requests
from datetime import datetime
from Util_Functions import (
    wind_degree_to_direction,
    unix_timestamp_to_localtime,
    convert_temperature,
)


def fetch_weather(api_key, latitude, longitude):
    """
    Function to fetch weather data from OpenWeatherMap One Call API.

    Parameters:
    api_key (str): API key.
    latitude (float): Latitude of the location.
    longitude (float): Longitude of the location.

    Returns:
    dict: The JSON response as a dictionary.
    """
    try:
        # Construct the API link with the provided API key, latitude, and longitude
        complete_api_link = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&exclude=minutely,hourly,alerts&appid={api_key}"

        # Sending GET request to OpenWeatherMap API
        response = requests.get(complete_api_link)

        # Parsing the JSON response
        api_data = response.json()

        # Returning the fetched weather data
        return api_data

    # Handling exceptions related to request errors
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None


def write_to_file(weather_data, temperature_unit):
    """
    Function to write weather information to a text file.

    Parameters:
    weather_data (dict): The JSON API response dictionary.
    temperature_unit (str): 'C' for Celsius, 'F' for Fahrenheit.
    """

    try:
        # Opening the file "weatherinfo.txt" in write mode
        with open("weatherinfo.txt", "w+") as f:
            # Getting the current date and time
            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

            # Writing header information to the file
            f.write("-------------------------------------------------------------\n")
            f.write(f"Weather Stats for Latitude: {weather_data['lat']}, Longitude: {weather_data['lon']} | {date_time}\n")
            f.write("-------------------------------------------------------------\n")

            # Writing current weather information
            current = weather_data.get("current", {})
            if current:
                # Writing temperature
                f.write(
                    "\tCurrent temperature is : "
                    + convert_temperature(current.get("temp", 0), temperature_unit)
                    + "\n"
                )
                # Writing weather description
                if "weather" in current and current["weather"]:
                    f.write(
                        "\tCurrent weather desc   : "
                        + current["weather"][0]["description"]
                        + "\n"
                    )
                # Writing humidity
                f.write(f"\tCurrent Humidity       : {current.get('humidity', 'N/A')} %\n")
                # Writing wind speed
                f.write(f"\tCurrent wind speed     : {current.get('wind_speed', 'N/A')} km/h\n")
                # Writing wind direction
                if "wind_deg" in current:
                    f.write(
                        "\tCurrent wind direction : "
                        + wind_degree_to_direction(current["wind_deg"])
                        + " \n"
                    )

            # Writing daily weather information
            daily = weather_data.get("daily", [])
            if daily:
                f.write("\nDaily Forecast:\n")
                for day in daily[:7]:  # Writing forecast for the next 7 days
                    dt = datetime.fromtimestamp(day["dt"]).strftime("%A, %d %b %Y")
                    temp = day["temp"]
                    f.write(f"{dt}:\n")
                    f.write(
                        f"\tDay Temp: {convert_temperature(temp['day'], temperature_unit)}\n"
                    )
                    f.write(
                        f"\tNight Temp: {convert_temperature(temp['night'], temperature_unit)}\n"
                    )
                    if "weather" in day and day["weather"]:
                        f.write(f"\tDescription: {day['weather'][0]['description']}\n")

        print("Weather information written to weatherinfo.txt")

    except IOError as e:
        print("Error writing to file:", e)


def main():
    """
    Main function.
    """
    # Printing welcome messages and instructions
    print("Welcome to the Weather Information App!")
    print("You need an API key to access weather data from OpenWeatherMap.")
    print(
        "You can obtain your API key by signing up at https://home.openweathermap.org/users/sign_up"
    )

    # Prompting the user to input API key, latitude, longitude, and temperature unit
    api_key = input("Please enter your OpenWeatherMap API key: ")
    latitude = input("Enter the latitude: ")
    longitude = input("Enter the longitude: ")
    temperature_unit = input(
        "Enter the temperature unit. 'C' for Celsius and 'F' for Fahrenheit: "
    )

    if not (temperature_unit.upper() == "C" or temperature_unit.upper() == "F"):
        print("Temperature unit must either be 'C' or 'F'.")
        return

    # Fetching weather data using the provided API key, latitude, and longitude
    weather_data = fetch_weather(api_key, latitude, longitude)

    # Checking if weather data was successfully fetched
    if weather_data:
        if "cod" in weather_data and weather_data["cod"] != 200:
            print(f"Error: {weather_data.get('message', 'Unknown error')}")
            return

        # Writing weather information to file
        write_to_file(weather_data, temperature_unit)

        # Printing confirmation
        print("Weather data fetched and written to file successfully.")
    else:
        print("Failed to fetch weather data. Please check your input and try again.")


# Ensuring the main function is executed when the script is run
if __name__ == "__main__":
    main()
