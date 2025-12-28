import tkinter as tk
from tkinter import font, ttk
from datetime import datetime, timedelta
import random

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyCast - Weather Forecast")
        
        # Make window resizable and set initial size
        self.root.geometry("700x550")  # Smaller initial size
        self.root.minsize(600, 450)    # Minimum size
        self.root.configure(bg="#1a1a2e")
        
        # City database with realistic parameters
        self.city_database = {
            "Istanbul": {"country": "Turkey", "lat": 41.0082, "lon": 28.9784, "timezone": 3},
            "Ankara": {"country": "Turkey", "lat": 39.9334, "lon": 32.8597, "timezone": 3},
            "Izmir": {"country": "Turkey", "lat": 38.4192, "lon": 27.1287, "timezone": 3},
            "Antalya": {"country": "Turkey", "lat": 36.8969, "lon": 30.7133, "timezone": 3},
            "London": {"country": "UK", "lat": 51.5074, "lon": -0.1278, "timezone": 0},
            "Paris": {"country": "France", "lat": 48.8566, "lon": 2.3522, "timezone": 1},
            "Berlin": {"country": "Germany", "lat": 52.5200, "lon": 13.4050, "timezone": 1},
            "Rome": {"country": "Italy", "lat": 41.9028, "lon": 12.4964, "timezone": 1},
            "New York": {"country": "USA", "lat": 40.7128, "lon": -74.0060, "timezone": -5},
            "Tokyo": {"country": "Japan", "lat": 35.6762, "lon": 139.6503, "timezone": 9},
        }
        
        # Weather condition colors
        self.weather_colors = {
            "Clear": "#FFD700",
            "Clouds": "#B0C4DE",
            "Rain": "#4682B4",
            "Snow": "#F0F8FF",
            "Thunderstorm": "#4B0082",
            "Drizzle": "#87CEEB",
            "Mist": "#D3D3D3",
            "default": "#87CEEB"
        }
        
        # Weather condition emojis
        self.weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Thunderstorm": "⛈️",
            "Drizzle": "🌦️",
            "Mist": "🌫️"
        }
        
        # Weather descriptions
        self.weather_descriptions = {
            "Clear": ["Sunny", "Clear", "Bright"],
            "Clouds": ["Partly Cloudy", "Cloudy", "Overcast"],
            "Rain": ["Light Rain", "Rainy", "Heavy Rain"],
            "Snow": ["Light Snow", "Snowy", "Blizzard"],
            "Thunderstorm": ["Thunderstorm", "Stormy"],
            "Drizzle": ["Drizzle", "Light Rain"],
            "Mist": ["Misty", "Foggy", "Hazy"]
        }
        
        # Seasonal temperature ranges
        self.seasonal_temps = {
            "winter": (-5, 10),
            "spring": (10, 20),
            "summer": (20, 35),
            "autumn": (5, 18)
        }
        
        self.setup_ui()
        
        # Show Istanbul by default
        self.root.after(100, lambda: self.search_city("Istanbul"))
    
    def setup_ui(self):
        """Setup the user interface with responsive design"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title section - smaller
        title_frame = tk.Frame(main_container, bg="#1a1a2e")
        title_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(title_frame, text="🌤️ SkyCast", 
                              font=("Helvetica", 24, "bold"),  # Smaller font
                              bg="#1a1a2e", fg="#FFFFFF")
        title_label.pack(side="left")
        
        subtitle_label = tk.Label(title_frame, text="Weather Simulation", 
                                 font=("Helvetica", 10),  # Smaller font
                                 bg="#1a1a2e", fg="#89CFF0")
        subtitle_label.pack(side="left", padx=(8, 0), pady=(5, 0))
        
        # Search bar - more compact
        search_frame = tk.Frame(main_container, bg="#16213e", relief="flat", bd=0)
        search_frame.pack(fill="x", pady=(0, 15))
        
        search_frame_inner = tk.Frame(search_frame, bg="#16213e")
        search_frame_inner.pack(padx=10, pady=10)
        
        self.city_entry = tk.Entry(search_frame_inner, 
                                  font=("Arial", 12),  # Smaller font
                                  width=20,  # Smaller width
                                  relief="flat",
                                  bg="#0f3460",
                                  fg="white",
                                  insertbackground="white")
        self.city_entry.pack(side="left", padx=(0, 8))
        self.city_entry.insert(0, "Istanbul")
        self.city_entry.bind("<Return>", lambda e: self.get_weather())
        
        search_btn = tk.Button(search_frame_inner, text="Search", 
                              font=("Arial", 11, "bold"),
                              bg="#4cc9f0",
                              fg="white",
                              activebackground="#4361ee",
                              activeforeground="white",
                              command=self.get_weather,
                              padx=20,  # Less padding
                              pady=6,   # Less padding
                              relief="flat",
                              cursor="hand2")
        search_btn.pack(side="left")
        
        # Content area - uses grid for better responsiveness
        content_frame = tk.Frame(main_container, bg="#1a1a2e")
        content_frame.pack(fill="both", expand=True)
        
        # Configure grid weights for responsive design
        content_frame.grid_columnconfigure(0, weight=3)  # Weather frame
        content_frame.grid_columnconfigure(1, weight=1)  # Side panel
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Weather information
        self.weather_frame = tk.Frame(content_frame, bg="#0f3460", relief="flat", bd=0)
        self.weather_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Right panel - Cities and info (scrollable if needed)
        right_panel = tk.Frame(content_frame, bg="#16213e", relief="flat", bd=0)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Create a canvas for scrollable content in right panel
        right_canvas = tk.Canvas(right_panel, bg="#16213e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=right_canvas.yview)
        scrollable_frame = tk.Frame(right_canvas, bg="#16213e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        
        right_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        right_canvas.configure(yscrollcommand=scrollbar.set)
        
        right_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        right_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Popular cities section
        cities_label = tk.Label(scrollable_frame, text="🏙️ Cities", 
                               font=("Arial", 12, "bold"),  # Smaller font
                               bg="#16213e", fg="white")
        cities_label.pack(pady=(15, 8), padx=10)
        
        cities_frame = tk.Frame(scrollable_frame, bg="#16213e")
        cities_frame.pack(pady=(0, 15), padx=10)
        
        popular_cities = list(self.city_database.keys())
        
        for city in popular_cities:
            city_btn = tk.Button(cities_frame, text=city,
                               font=("Arial", 9),  # Smaller font
                               bg="#0f3460",
                               fg="white",
                               activebackground="#4cc9f0",
                               activeforeground="white",
                               command=lambda c=city: self.search_city(c),
                               padx=12,  # Less padding
                               pady=6,   # Less padding
                               relief="flat",
                               cursor="hand2")
            city_btn.pack(fill="x", pady=2)
        
        # Information section
        info_frame = tk.Frame(scrollable_frame, bg="#16213e")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_label = tk.Label(info_frame, text="ℹ️ Info", 
                             font=("Arial", 11, "bold"),
                             bg="#16213e", fg="white")
        info_label.pack(anchor="w", pady=(0, 8))
        
        info_text = """Realistic weather simulation.

• Seasonal variations
• Geographic effects
• Time-based changes
• No API required"""

        tk.Label(info_frame, text=info_text,
                font=("Arial", 8),  # Smaller font
                bg="#16213e", fg="#89CFF0",
                justify="left").pack(anchor="w")
        
        # Add some spacing at the bottom
        tk.Frame(scrollable_frame, bg="#16213e", height=20).pack()
        
        # Footer - simplified
        footer_frame = tk.Frame(main_container, bg="#1a1a2e")
        footer_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(footer_frame, text="SkyCast v1.0", 
                font=("Arial", 8),
                bg="#1a1a2e", fg="#89CFF0").pack()
    
    def search_city(self, city):
        """Search for a specific city"""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.get_weather()
    
    def get_weather(self):
        """Get weather data for the entered city"""
        city = self.city_entry.get().strip()
        if not city:
            self.show_message("Please enter a city name!", "warning")
            return
        
        # Generate realistic weather data
        weather_data = self.generate_realistic_weather(city)
        self.display_weather(weather_data)
    
    def generate_realistic_weather(self, city):
        """Generate realistic weather data based on city parameters"""
        now = datetime.now()
        month = now.month
        hour = now.hour
        
        # Determine season
        if month in [12, 1, 2]:
            season = "winter"
        elif month in [3, 4, 5]:
            season = "spring"
        elif month in [6, 7, 8]:
            season = "summer"
        else:
            season = "autumn"
        
        # Get city info
        city_info = self.city_database.get(city, {"country": "??", "lat": 0, "lon": 0, "timezone": 0})
        
        # Calculate temperature based on latitude
        lat = abs(city_info["lat"])
        if lat > 50:
            temp_mod = -5
        elif lat > 35:
            temp_mod = 0
        else:
            temp_mod = 10
        
        # Southern hemisphere adjustment
        if city_info["lat"] < 0:
            if season == "winter":
                season = "summer"
            elif season == "summer":
                season = "winter"
            elif season == "spring":
                season = "autumn"
            else:
                season = "spring"
        
        # Base temperature
        min_temp, max_temp = self.seasonal_temps[season]
        base_temp = random.uniform(min_temp, max_temp) + temp_mod
        
        # Time of day effect
        if 0 <= hour < 6:
            base_temp -= random.uniform(3, 8)
        elif 6 <= hour < 12:
            base_temp -= random.uniform(0, 3)
        elif 12 <= hour < 18:
            base_temp += random.uniform(0, 5)
        else:
            base_temp -= random.uniform(1, 4)
        
        # Determine weather conditions
        if season == "winter":
            conditions = ["Clear", "Clouds", "Snow", "Mist"]
            weights = [0.2, 0.4, 0.3, 0.1]
        elif season == "spring":
            conditions = ["Clear", "Clouds", "Rain", "Drizzle"]
            weights = [0.3, 0.4, 0.2, 0.1]
        elif season == "summer":
            conditions = ["Clear", "Clouds", "Thunderstorm"]
            weights = [0.6, 0.3, 0.1]
        else:
            conditions = ["Clear", "Clouds", "Rain", "Mist"]
            weights = [0.3, 0.4, 0.2, 0.1]
        
        main_weather = random.choices(conditions, weights=weights)[0]
        
        # Temperature adjustment based on weather
        if main_weather in ["Rain", "Snow", "Thunderstorm"]:
            temp = base_temp - random.uniform(3, 8)
        elif main_weather == "Clouds":
            temp = base_temp - random.uniform(1, 3)
        else:
            temp = base_temp + random.uniform(0, 5)
        
        # Weather description
        description = random.choice(self.weather_descriptions.get(main_weather, ["Fair"]))
        
        # Additional parameters
        feels_like = temp - random.uniform(1, 3) if temp > 0 else temp - random.uniform(0.5, 1.5)
        humidity = random.randint(60, 95) if main_weather in ["Rain", "Snow", "Thunderstorm"] else random.randint(40, 75)
        pressure = random.randint(1000, 1020)
        
        # Wind speed
        if main_weather == "Thunderstorm":
            wind_speed = random.uniform(15, 35)
        elif main_weather in ["Rain", "Snow"]:
            wind_speed = random.uniform(10, 25)
        else:
            wind_speed = random.uniform(0, 15)
        
        # Sunrise and sunset
        sunrise_hour = 6 + random.randint(-1, 1)
        sunset_hour = 18 + random.randint(-1, 1)
        
        if season == "summer":
            sunrise_hour -= 1
            sunset_hour += 1
        elif season == "winter":
            sunrise_hour += 1
            sunset_hour -= 1
        
        sunrise_time = now.replace(hour=sunrise_hour, minute=random.randint(0, 59))
        sunset_time = now.replace(hour=sunset_hour, minute=random.randint(0, 59))
        
        tz_offset = city_info.get("timezone", 0)
        sunrise_time += timedelta(hours=tz_offset)
        sunset_time += timedelta(hours=tz_offset)
        
        return {
            'name': city,
            'sys': {'country': city_info["country"]},
            'main': {
                'temp': round(temp, 1),
                'feels_like': round(feels_like, 1),
                'humidity': humidity,
                'pressure': pressure
            },
            'wind': {'speed': round(wind_speed, 1)},
            'weather': [{
                'description': description,
                'main': main_weather
            }],
            'sys_data': {
                'sunrise': sunrise_time,
                'sunset': sunset_time
            },
            'timezone': tz_offset,
            'season': season
        }
    
    def display_weather(self, data):
        """Display weather information in the main frame"""
        # Clear previous content
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        # Extract data
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        main_weather = data['weather'][0]['main']
        
        # Get colors
        bg_color = self.weather_colors.get(main_weather, self.weather_colors["default"])
        self.weather_frame.config(bg=bg_color)
        
        # Create main container with scroll if needed
        container = tk.Frame(self.weather_frame, bg=bg_color)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # City and country - smaller
        icon_emoji = self.weather_icons.get(main_weather, "🌤️")
        
        city_label = tk.Label(container, 
                             text=f"{icon_emoji} {city}, {country}",
                             font=("Helvetica", 18, "bold"),  # Smaller
                             bg=bg_color, fg="#333333")
        city_label.pack(pady=(5, 5))
        
        # Temperature - smaller
        temp_label = tk.Label(container,
                             text=f"{temp:.1f}°C",
                             font=("Helvetica", 48, "bold"),  # Smaller
                             bg=bg_color, fg="#FF4500")
        temp_label.pack(pady=5)
        
        # Description
        desc_label = tk.Label(container,
                             text=description,
                             font=("Helvetica", 14),  # Smaller
                             bg=bg_color, fg="#555555")
        desc_label.pack(pady=5)
        
        # Feels like
        feels_label = tk.Label(container,
                              text=f"Feels like: {feels_like:.1f}°C",
                              font=("Helvetica", 12),  # Smaller
                              bg=bg_color, fg="#666666")
        feels_label.pack(pady=5)
        
        # Separator
        separator = tk.Frame(container, bg="#E0E0E0", height=1)
        separator.pack(fill="x", pady=10)
        
        # Weather details - compact grid
        details_frame = tk.Frame(container, bg=bg_color)
        details_frame.pack(pady=5)
        
        # Create 2x2 grid for details
        details = [
            ("💧 Humidity", f"{humidity}%"),
            ("💨 Wind", f"{wind_speed} km/h"),
            ("📊 Pressure", f"{pressure} hPa"),
            ("🌡️ Feels", f"{feels_like:.1f}°C"),
        ]
        
        for i, (icon_text, value_text) in enumerate(details):
            row = i // 2
            col = i % 2
            
            detail_frame = tk.Frame(details_frame, bg=bg_color)
            detail_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            
            # Icon and label
            icon_label = tk.Label(detail_frame, text=icon_text,
                                 font=("Arial", 10),  # Smaller
                                 bg=bg_color, fg="#2c3e50")
            icon_label.pack(anchor="w")
            
            # Value
            value_label = tk.Label(detail_frame, text=value_text,
                                  font=("Arial", 11, "bold"),  # Smaller
                                  bg=bg_color, fg="#2c3e50")
            value_label.pack(anchor="w")
        
        # Sunrise and sunset - compact
        time_frame = tk.Frame(container, bg=bg_color)
        time_frame.pack(pady=10)
        
        sunrise_time = data['sys_data']['sunrise'].strftime("%H:%M")
        sunset_time = data['sys_data']['sunset'].strftime("%H:%M")
        
        sun_frame = tk.Frame(time_frame, bg=bg_color)
        sun_frame.pack()
        
        sunrise_label = tk.Label(sun_frame, text=f"🌅 {sunrise_time}",
                                font=("Arial", 10),  # Smaller
                                bg=bg_color, fg="#2c3e50")
        sunrise_label.pack(side="left", padx=(0, 15))
        
        sunset_label = tk.Label(sun_frame, text=f"🌇 {sunset_time}",
                               font=("Arial", 10),  # Smaller
                               bg=bg_color, fg="#2c3e50")
        sunset_label.pack(side="left")
        
        # Additional info - smaller
        info_frame = tk.Frame(container, bg=bg_color)
        info_frame.pack(pady=5)
        
        season = data.get('season', 'Unknown')
        timezone = data.get('timezone', 0)
        tz_text = f"UTC{'+' if timezone >= 0 else ''}{timezone}"
        
        info_label = tk.Label(info_frame, text=f"Season: {season.title()} • TZ: {tz_text}",
                             font=("Arial", 8, "italic"),  # Smaller
                             bg=bg_color, fg="#7f8c8d")
        info_label.pack()
        
        # Update time - smaller
        update_time = datetime.now().strftime("%H:%M:%S")
        update_label = tk.Label(container, text=f"Updated: {update_time}",
                               font=("Arial", 8),  # Smaller
                               bg=bg_color, fg="#95a5a6")
        update_label.pack(pady=(5, 0))
    
    def show_message(self, message, msg_type="info"):
        """Show message to user"""
        color = "#e74c3c" if msg_type == "warning" else "#3498db"
        
        msg_frame = tk.Frame(self.weather_frame, bg=color)
        msg_frame.place(relx=0.5, rely=0.1, anchor="center")
        
        msg_label = tk.Label(msg_frame, text=message,
                            font=("Arial", 10, "bold"),  # Smaller
                            bg=color, fg="white",
                            padx=15, pady=8)  # Less padding
        msg_label.pack()
        
        self.root.after(3000, msg_frame.destroy)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    
    # Make window resizable
    root.resizable(True, True)
    
    # Bind window resize event to update layout
    def on_resize(event):
        # You can add resize handling here if needed
        pass
    
    root.bind('<Configure>', on_resize)
    
    root.mainloop()
