import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
from datetime import datetime

from PIL import Image, ImageTk
from io import BytesIO


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e3a8a")

        self.setup_ui()

    def setup_ui(self):
        # main container
        main = tk.Frame(self.root, bg="#1e3a8a")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # title
        tk.Label(main, text="Weather App", font=("Helvetica", 32, "bold"),
                 bg="#1e3a8a", fg="white").pack(pady=(0, 20))

        # search bar
        search_frame = tk.Frame(main, bg="#1e3a8a")
        search_frame.pack(pady=10)

        self.city = tk.Entry(search_frame, font=("Arial", 14), width=30)
        self.city.pack(side="left", padx=5)
        self.city.bind("<Return>", lambda e: self.go())

        tk.Button(search_frame, text="Search", bg="#fbbf24", fg="black", font=("Arial", 12, "bold"),
                  command=self.go, cursor="hand2").pack(side="left", padx=5)

        # current weather card
        self.current_frame = tk.Frame(main, bg="#0f172a", relief="raised", bd=2)
        self.current_frame.pack(fill="both", expand=True, pady=15)

        # forecast row
        self.forecast_frame = tk.Frame(main, bg="#1e3a8a")
        self.forecast_frame.pack(fill="both", expand=True, pady=10)

        # status at the bottom
        self.status = tk.Label(main, text="type a city and hit enter", fg="#94a3b8", bg="#1e3a8a")
        self.status.pack(pady=5)

    def go(self):
        city = self.city.get().strip()
        if not city:
            messagebox.showwarning("oops", "gotta type something dude")
            return

        self.status.config(text="looking up...")
        threading.Thread(target=self.fetch_stuff, args=(city,), daemon=True).start()

    def fetch_stuff(self, city):
        try:
            # step 1: find lat/lon
            geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                               params={"name": city, "count": 1}).json()

            if not geo.get("results"):
                self.root.after(0, lambda: messagebox.showerror("nah", f"can't find {city}"))
                self.root.after(0, lambda: self.status.config(text="not found bro"))
                return

            loc = geo["results"][0]
            lat, lon = loc["latitude"], loc["longitude"]
            name = loc.get("name", "") + ", " + loc.get("country", "")

            # step 2: actual weather
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto"
            }
            data = requests.get(url, params=params).json()

            # show it
            self.root.after(0, self.show_current, name, data["current"])
            self.root.after(0, self.show_forecast, data["daily"])
            self.root.after(0, lambda: self.status.config(text=f"{name} • just now"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("rip", f"something died:\n{e}"))

    def describe(self, code):
        # lazy dictionary because who has time for all 100 codes
        weather = {
            0: "Clear", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 51: "Light drizzle", 53: "Drizzle", 61: "Rain", 63: "Rain", 65: "Heavy rain",
            71: "Snow", 73: "Snow", 80: "Showers", 95: "Thunderstorm"
        }
        return weather.get(code, f"Code {code}")

    def show_current(self, location, cur):
        for widget in self.current_frame.winfo_children():
            widget.destroy()

        tk.Label(self.current_frame, text=location, font=("Arial", 20, "bold"),
                 bg="#0f172a", fg="#fbbf24").pack(pady=15)

        tk.Label(self.current_frame, text=f"{cur['temperature_2m']}°C",
                 font=("Helvetica", 60, "bold"), bg="#0f172a", fg="white").pack()

        tk.Label(self.current_frame, text=self.describe(cur["weather_code"]),
                 font=("Arial", 16), bg="#0f172a", fg="#94a3b8").pack(pady=5)

        details = tk.Frame(self.current_frame, bg="#0f172a")
        details.pack(pady=20)

        for label, value in [("Humidity", f"{cur['relative_humidity_2m']}%"),
                             ("Wind", f"{cur['wind_speed_10m']} km/h")]:
            box = tk.Frame(details, bg="#1e40af", relief="raised", bd=1)
            box.pack(side="left", padx=20, pady=5, expand=True, fill="x")
            tk.Label(box, text=label, fg="#94a3b8", bg="#1e40af").pack()
            tk.Label(box, text=value, font=("Arial", 16, "bold"), fg="white", bg="#1e40af").pack()

    def show_forecast(self, daily):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        tk.Label(self.forecast_frame, text="7-Day Forecast", font=("Arial", 16, "bold"),
                 bg="#1e3a8a", fg="white").pack(pady=8)

        row = tk.Frame(self.forecast_frame, bg="#1e3a8a")
        row.pack(fill="both", expand=True)

        for i in range(7):  # good enough
            date = datetime.strptime(daily["time"][i], "%Y-%m-%d")
            day_box = tk.Frame(row, bg="#0f172a", relief="raised", bd=2)
            day_box.pack(side="left", expand=True, fill="both", padx=6, pady=6)

            tk.Label(day_box, text=date.strftime("%a\n%b %d"), fg="#94a3b8", bg="#0f172a").pack(pady=6)
            tk.Label(day_box, text=self.describe(daily["weather_code"][i]),
                     fg="white", bg="#0f172a", font=("Arial", 9)).pack()
            tk.Label(day_box, text=f"↑{daily['temperature_2m_max'][i]}° ↓{daily['temperature_2m_min'][i]}°",
                     fg="#fbbf24", bg="#0f172a", font=("Arial", 10, "bold")).pack(pady=4)
            tk.Label(day_box, text=f"💧 {daily['precipitation_sum'][i]}mm",
                     fg="#94a3b8", bg="#0f172a", font=("Arial", 9)).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
