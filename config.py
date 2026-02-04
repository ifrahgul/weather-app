import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    
    # App Settings
    APP_NAME = "Weather Forecast Pro"
    APP_VERSION = "4.0"
    DEFAULT_LOCATION = "Mumbai, India"
    DEFAULT_LAT = 19.0760
    DEFAULT_LON = 72.8777
    
    # Background Image URL
    BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80"
    
    # Colors (Modern Design)
    COLORS = {
        'primary': '#1a73e8',      # Blue
        'secondary': '#34a853',    # Green
        'warning': '#fbbc04',      # Yellow
        'danger': '#ea4335',       # Red
        'text_primary': '#202124',
        'text_secondary': '#5f6368',
        'text_light': '#ffffff',
        'bg_light': '#ffffff',
        'bg_dark': '#202124',
        'bg_grey': '#f8f9fa',
        'card_bg': 'rgba(255, 255, 255, 0.95)',
    }
    
    # Weather Settings
    UNITS = 'metric'
    LANGUAGE = 'en'
    
    # Map Settings
    MAP_ZOOM = 11
    MAP_TILE = 'CartoDB positron'
    
    # Features
    ENABLE_HOURLY_FORECAST = True
    ENABLE_DAILY_FORECAST = True
    ENABLE_MAPS = True
    ENABLE_CHARTS = True
    ENABLE_SETTINGS = True
    ENABLE_AIR_QUALITY = True