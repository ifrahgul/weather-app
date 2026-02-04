import requests
import pandas as pd
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import json
from config import Config

class WeatherAPI:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        if not self.api_key:
            raise ValueError("OpenWeather API key not found. Add it to .env file")
        
        self.geolocator = Nominatim(user_agent="weather_forecast_pro", timeout=10)
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_location_coordinates(self, location_name):
        """Get coordinates for a location"""
        try:
            # Try with OpenWeather geocoding
            geo_url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                'q': location_name,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(geo_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = data[0]['lat']
                    lon = data[0]['lon']
                    name = data[0].get('name', '')
                    country = data[0].get('country', '')
                    address = f"{name}, {country}" if name and country else location_name
                    return lat, lon, address
            
            # Fallback to Nominatim
            try:
                location = self.geolocator.geocode(location_name)
                if location:
                    return location.latitude, location.longitude, location.address
            except:
                pass
            
            return Config.DEFAULT_LAT, Config.DEFAULT_LON, Config.DEFAULT_LOCATION
            
        except Exception as e:
            print(f"Location error: {str(e)}")
            return Config.DEFAULT_LAT, Config.DEFAULT_LON, Config.DEFAULT_LOCATION
    
    def get_current_weather(self, lat, lon):
        """Get current weather data"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': Config.UNITS,
                'lang': Config.LANGUAGE
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Weather API error: {str(e)}")
            return self._get_sample_data()
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return self._get_sample_data()
    
    def get_forecast(self, lat, lon):
        """Get 5-day forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': Config.UNITS,
                'cnt': 40
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except:
            return None
    
    def get_7_hour_forecast(self, forecast_data):
        """Get 7-hour forecast data"""
        if not forecast_data:
            return self._get_7_hour_sample_data()
        
        hourly_data = []
        
        for item in forecast_data['list'][:7]:
            dt = datetime.fromtimestamp(item['dt'])
            
            hour_str = dt.strftime('%I %p').lstrip('0')
            if hour_str.startswith(' '):
                hour_str = hour_str[1:]
            
            hourly_data.append({
                'time': hour_str,
                'temp': round(item['main']['temp']),
                'icon': item['weather'][0]['icon'],
                'weather': item['weather'][0]['main'],
                'humidity': item['main']['humidity'],
                'wind_speed': round(item['wind']['speed'], 1),
            })
        
        return hourly_data
    
    def get_daily_forecast_data(self, forecast_data):
        """Process daily forecast data"""
        if not forecast_data:
            return self._get_sample_daily_data()
        
        daily_data = {}
        
        for item in forecast_data['list']:
            date_str = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date_str not in daily_data:
                daily_data[date_str] = {
                    'temps': [],
                    'weather': [],
                    'icons': [],
                    'pop': []
                }
            
            daily_data[date_str]['temps'].append(item['main']['temp'])
            daily_data[date_str]['weather'].append(item['weather'][0]['main'])
            daily_data[date_str]['icons'].append(item['weather'][0]['icon'])
            daily_data[date_str]['pop'].append(item.get('pop', 0) * 100)
        
        processed_data = []
        dates = list(daily_data.keys())[:7]
        
        for date_str in dates:
            data = daily_data[date_str]
            day_name = datetime.strptime(date_str, '%Y-%m-%d').strftime('%a')
            avg_temp = sum(data['temps']) / len(data['temps'])
            max_temp = max(data['temps'])
            min_temp = min(data['temps'])
            
            weather = max(set(data['weather']), key=data['weather'].count) if data['weather'] else 'Clear'
            icon = max(set(data['icons']), key=data['icons'].count) if data['icons'] else '01d'
            
            processed_data.append({
                'date': date_str,
                'day': day_name,
                'temp': round(avg_temp),
                'max_temp': round(max_temp),
                'min_temp': round(min_temp),
                'weather': weather,
                'icon': icon,
                'precipitation': round(max(data['pop'])) if data['pop'] else 0,
            })
        
        return processed_data
    
    def get_air_quality(self, lat, lon):
        """Get air quality data"""
        try:
            url = f"{self.base_url}/air_pollution"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except:
            return None
    
    def _get_sample_data(self):
        """Return sample data for testing"""
        return {
            'weather': [{'main': 'Overcast Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
            'main': {
                'temp': 26.99,
                'feels_like': 27.0,
                'temp_min': 26.94,
                'temp_max': 26.99,
                'pressure': 1001,
                'humidity': 89
            },
            'wind': {'speed': 4.63, 'deg': 230},
            'clouds': {'all': 100},
            'sys': {
                'sunrise': int(datetime.now().replace(hour=6, minute=30, second=0).timestamp()),
                'sunset': int(datetime.now().replace(hour=18, minute=30, second=0).timestamp())
            },
            'visibility': 800,
            'name': 'Mumbai'
        }
    
    def _get_7_hour_sample_data(self):
        """Return sample 7-hour data"""
        base_time = datetime.now()
        sample_data = []
        
        for i in range(7):
            time_delta = timedelta(hours=i)
            dt = base_time + time_delta
            hour_str = dt.strftime('%I %p').lstrip('0')
            
            sample_data.append({
                'time': hour_str,
                'temp': 26 + (i % 2),
                'icon': '04d' if i < 4 else '01d',
                'weather': 'Clouds' if i < 4 else 'Clear',
                'humidity': 80 - i*5,
                'wind_speed': 3.5 + i/2,
            })
        
        return sample_data
    
    def _get_sample_daily_data(self):
        """Return sample daily data"""
        base_date = datetime.now()
        sample_data = []
        
        days = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']
        
        for i in range(7):
            dt = base_date + timedelta(days=i)
            
            sample_data.append({
                'date': dt.strftime('%Y-%m-%d'),
                'day': days[i],
                'temp': 27 + (i % 2),
                'max_temp': 28 + (i % 2),
                'min_temp': 26 + (i % 2),
                'weather': 'Overcast Clouds' if i < 3 else 'Clear',
                'icon': '04d' if i < 3 else '01d',
                'precipitation': 0,
            })
        
        return sample_data