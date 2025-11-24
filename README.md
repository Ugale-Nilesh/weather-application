Weather App

A simple and visually appealing desktop weather application built with Python's Tkinter library. This app allows you to enter any city name and get real-time current weather conditions along with a 7-day forecast, using the free Open-Meteo API — no API key needed!



Features

- Clean, user-friendly interface with a modern dark blue theme.
- Search by city name using a text entry box with "Enter" key or Search button.
- Displays current weather including temperature (°C), humidity, wind speed, and descriptive weather conditions.
- Shows a 7-day weather forecast with daily highs, lows, weather descriptions, and precipitation amounts.
- Responsive UI that loads weather data in the background without freezing.
- Helpful status messages guide you through the search process.
- Graceful error handling for invalid city names or network issues.



How it Works

1. You type a city name and press Enter or click the Search button.
2. The app uses the Open-Meteo geocoding API to convert the city name to geographic coordinates (latitude and longitude).
3. These coordinates are then used to fetch current weather and 7-day forecast data from the Open-Meteo forecast API.
4. Weather codes from the API are translated into human-readable descriptions such as "Clear", "Rain", "Snow", etc.
5. All data is dynamically displayed in the GUI, updating the current weather and forecast sections.
6. The app runs API requests on a background thread, keeping the interface smooth and responsive.


 
 Technologies Used

- Python 3 with Tkinter for graphical user interface (GUI)
- `requests` library for making HTTP requests to APIs
- `threading` to avoid GUI freezing during data fetching
- `datetime` for formatting date in the forecast
- Open-Meteo free weather APIs for geocoding and weather data


 
 Installation and Usage

1. Make sure Python 3 is installed on your system.
2. Install required packages if not already installed:

   pip install requests pillow

3. Save the Python script to a file, e.g., `weather_app.py`.
4. Run the script:
   
   python weather_app.py

6. In the application window, type a city name and press Enter or the Search button.
7. View the current weather and 7-day forecast displayed beautifully.


 Notes

- The app uses Open-Meteo’s public API endpoints, which do not require an API key but are intended for personal and non-commercial use.
- The weather condition descriptions cover common weather codes; some rare codes may show as code numbers.
- Included `Pillow` imports are for potential extensions such as weather icons but are not currently utilized.
- Error messages appear if the city is not found or network errors occur, ensuring clarity for the user.




