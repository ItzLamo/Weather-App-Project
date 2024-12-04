import requests
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import tkinter as tk
from tkinter import ttk, messagebox

# Function to get weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        # Fetch location data
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if not location:
            messagebox.showerror("Error", "City not found!")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
        local_time = datetime.now(pytz.timezone(result))
        time_label.config(text=f"Local Time: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Fetch weather data
        api_key = "0892995a54fe5c53bb52525aeb7d3bf2"
        base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        weather_data = response.json()

        if weather_data.get("cod") != 200:
            messagebox.showerror("Error", weather_data.get("message", "API error"))
            return

        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        wind_speed = weather_data["wind"]["speed"]
        description = weather_data["weather"][0]["description"]

        # Update GUI with weather details
        temp_label.config(text=f"Temperature: {temperature}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("500x500")
root.resizable(False, False)
root.config(bg="#87CEEB")  # Light sky blue background

# Title
title_label = tk.Label(root, text="Weather of the city", font=("Helvetica", 24, "bold"), bg="#87CEEB", fg="white")
title_label.pack(pady=10)

# Entry for city
city_entry = tk.Entry(root, font=("Helvetica", 16), justify="center", bd=2, relief="solid")
city_entry.pack(pady=5)
city_entry.insert(0, "Enter the city name")

# Search button
search_button = tk.Button(root, text="Get Weather", font=("Helvetica", 14), bg="#4682B4", fg="white", 
                           command=get_weather)
search_button.pack(pady=10)

# Weather details
frame = tk.Frame(root, bg="#87CEEB")
frame.pack(pady=10)

time_label = tk.Label(frame, text="Local Time: --:--", font=("Helvetica", 14), bg="#87CEEB", fg="white")
time_label.grid(row=0, column=0, columnspan=2, pady=5)

temp_label = tk.Label(frame, text="Temperature: --°C", font=("Helvetica", 14), bg="#87CEEB", fg="white")
temp_label.grid(row=3, column=0, columnspan=2, pady=5)

humidity_label = tk.Label(frame, text="Humidity: --%", font=("Helvetica", 14), bg="#87CEEB", fg="white")
humidity_label.grid(row=4, column=0, columnspan=2, pady=5)

pressure_label = tk.Label(frame, text="Pressure: ---- hPa", font=("Helvetica", 14), bg="#87CEEB", fg="white")
pressure_label.grid(row=5, column=0, columnspan=2, pady=5)

wind_label = tk.Label(frame, text="Wind Speed: -- m/s", font=("Helvetica", 14), bg="#87CEEB", fg="white")
wind_label.grid(row=6, column=0, columnspan=2, pady=5)

# Footer
footer_label = tk.Label(root, text="Created by Hassan Ahmed, for the Hack Club", font=("Helvetica", 12), bg="#87CEEB", fg="white")
footer_label.pack(pady=20)

# Start the GUI loop
root.mainloop()
