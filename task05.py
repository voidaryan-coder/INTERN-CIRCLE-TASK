import tkinter as tk
from tkinter import messagebox
import requests

# Enter your OpenWeather API key here
API_KEY = "YOUR_API_KEY_HERE"

GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


# Function to get weather information
def get_weather():

    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return

    if API_KEY == "YOUR_API_KEY_HERE":
        messagebox.showerror(
            "API Key Missing",
            "Please add your OpenWeather API key in the code."
        )
        return

    result_label.config(text="Fetching weather data...")
    root.update_idletasks()

    try:
        # Get city coordinates
        geo_params = {
            "q": city,
            "limit": 1,
            "appid": API_KEY
        }

        geo_response = requests.get(
            GEO_URL,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()
        locations = geo_response.json()

        if not locations:
            messagebox.showerror("Error", "City not found!")
            result_label.config(text="Enter another city.")
            return

        latitude = locations[0]["lat"]
        longitude = locations[0]["lon"]

        # Get current weather
        weather_params = {
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            WEATHER_URL,
            params=weather_params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        # Extract weather details
        city_name = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"].title()
        min_temp = data["main"]["temp_min"]
        max_temp = data["main"]["temp_max"]

        # Display weather information
        result = f"""
        Location: {city_name}, {country}

        Weather: {description}

        Temperature: {temperature:.1f} °C

        Feels Like: {feels_like:.1f} °C

        Minimum Temperature: {min_temp:.1f} °C

        Maximum Temperature: {max_temp:.1f} °C

        Humidity: {humidity} %

        Wind Speed: {wind_speed} m/s

        Pressure: {pressure} hPa
        """

        result_label.config(text=result)

    except requests.exceptions.HTTPError as error:
        result_label.config(text="Unable to fetch weather.")

        if response.status_code == 401:
            messagebox.showerror(
                "API Error",
                "Invalid API key or key not activated yet."
            )
        elif response.status_code == 404:
            messagebox.showerror("Error", "City not found!")
        else:
            messagebox.showerror("API Error", str(error))

    except requests.exceptions.RequestException:
        result_label.config(text="Connection failed.")
        messagebox.showerror(
            "Network Error",
            "Please check your internet connection."
        )

    except (KeyError, IndexError, ValueError):
        result_label.config(text="Unexpected API response.")
        messagebox.showerror(
            "Error",
            "Could not read the weather information."
        )


# Clear input and output
def clear_data():
    city_entry.delete(0, tk.END)
    result_label.config(text="Weather information will appear here.")


# Main window
root = tk.Tk()
root.title("Live Weather App")
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg="#d6eaf8")

# Heading
title = tk.Label(
    root,
    text="LIVE WEATHER APP",
    font=("Arial", 23, "bold"),
    bg="#d6eaf8",
    fg="#154360"
)
title.pack(pady=25)

subtitle = tk.Label(
    root,
    text="Check Current Weather of Any City",
    font=("Arial", 12),
    bg="#d6eaf8"
)
subtitle.pack(pady=5)

# City input
city_label = tk.Label(
    root,
    text="Enter City Name:",
    font=("Arial", 13, "bold"),
    bg="#d6eaf8"
)
city_label.pack(pady=15)

city_entry = tk.Entry(
    root,
    font=("Arial", 15),
    justify="center",
    width=25
)
city_entry.pack(ipady=8)

# Search button
search_button = tk.Button(
    root,
    text="GET WEATHER",
    font=("Arial", 13, "bold"),
    bg="#2874a6",
    fg="white",
    width=20,
    command=get_weather
)
search_button.pack(pady=15)

# Clear button
clear_button = tk.Button(
    root,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg="#e74c3c",
    fg="white",
    width=15,
    command=clear_data
)
clear_button.pack(pady=5)

# Weather result
result_label = tk.Label(
    root,
    text="Weather information will appear here.",
    font=("Arial", 12),
    bg="white",
    fg="#154360",
    justify="left",
    anchor="w",
    width=42,
    height=18,
    padx=15,
    pady=10
)
result_label.pack(pady=20)

# Start application
root.mainloop()