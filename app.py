import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment
load_dotenv()

# Import modules
from config import Config
from modules.weather_api import WeatherAPI
from modules.ui_manager import UIManager
from modules.theme_manager import ThemeManager
from modules.map_manager import MapManager

# Initialize
weather_api = WeatherAPI()
ui = UIManager()
theme_manager = ThemeManager()
map_manager = MapManager()

# Page config
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",  # Sidebar expanded by default
    menu_items={
        'About': f"""
        # {Config.APP_NAME} v{Config.APP_VERSION}
        
        🌤️ **Advanced Weather Forecast Application**
        
        **Features:**
        • Real-time weather data
        • 7-hour & 7-day forecasts
        • Interactive temperature charts
        • Location maps
        • Air quality monitoring
        • Customizable settings
        
        **Version:** {Config.APP_VERSION}
        """
    }
)

# Apply theme
st.markdown(theme_manager.get_css(), unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.location = Config.DEFAULT_LOCATION
        st.session_state.lat = Config.DEFAULT_LAT
        st.session_state.lon = Config.DEFAULT_LON
        st.session_state.address = Config.DEFAULT_LOCATION
        st.session_state.weather_data = None
        st.session_state.hourly_data = None
        st.session_state.daily_data = None
        st.session_state.air_quality_data = None
        st.session_state.forecast_data = None
        st.session_state.last_update = None
        st.session_state.search_history = []
        st.session_state.favorites = []
        st.session_state.unit = "metric"
        st.session_state.theme = "Auto"
        st.session_state.show_charts = True
        st.session_state.show_maps = True
        st.session_state.use_current_location = False
        st.session_state.sidebar_open = True

init_session_state()

def update_location(search_query):
    """Update location and fetch weather"""
    try:
        with st.spinner(f"🌍 Searching for {search_query}..."):
            lat, lon, address = weather_api.get_location_coordinates(search_query)
            
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.address = address
            st.session_state.location = search_query
            
            # Clear cached data
            st.session_state.weather_data = None
            st.session_state.hourly_data = None
            st.session_state.daily_data = None
            st.session_state.air_quality_data = None
            st.session_state.forecast_data = None
            
            # Add to search history
            if search_query not in st.session_state.search_history:
                st.session_state.search_history.append(search_query)
                if len(st.session_state.search_history) > 10:
                    st.session_state.search_history.pop(0)
            
            st.rerun()
            
    except Exception as e:
        st.error(f"Error updating location: {str(e)}")

def fetch_weather_data():
    """Fetch all weather data"""
    if not st.session_state.weather_data:
        try:
            with st.spinner("🌤️ Loading weather data..."):
                # Current weather
                st.session_state.weather_data = weather_api.get_current_weather(
                    st.session_state.lat, st.session_state.lon
                )
                
                # Forecast
                st.session_state.forecast_data = weather_api.get_forecast(
                    st.session_state.lat, st.session_state.lon
                )
                
                if st.session_state.forecast_data:
                    # 7-hour forecast
                    st.session_state.hourly_data = weather_api.get_7_hour_forecast(
                        st.session_state.forecast_data
                    )
                    # 7-day forecast
                    st.session_state.daily_data = weather_api.get_daily_forecast_data(
                        st.session_state.forecast_data
                    )
                
                # Air quality
                st.session_state.air_quality_data = weather_api.get_air_quality(
                    st.session_state.lat, st.session_state.lon
                )
                
                st.session_state.last_update = datetime.now()
                
        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")
            # Use sample data
            st.session_state.weather_data = weather_api._get_sample_data()
            st.session_state.hourly_data = weather_api._get_7_hour_sample_data()
            st.session_state.daily_data = weather_api._get_sample_daily_data()

def display_sidebar():
    """Display sidebar with settings and features"""
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <h3 style="color: {Config.COLORS['primary']}; margin: 0;">⚙️ Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        
        # Temperature Unit
        unit_options = ["Celsius (°C)", "Fahrenheit (°F)"]
        selected_unit = st.selectbox(
            "Temperature Unit",
            unit_options,
            index=0 if st.session_state.unit == "metric" else 1
        )
        
        # Theme
        theme_options = ["Auto", "Light", "Dark", "High Contrast"]
        selected_theme = st.selectbox(
            "Theme",
            theme_options,
            index=theme_options.index(st.session_state.theme)
        )
        
        # Features Toggles
        st.markdown("### 🔧 Features")
        show_charts = st.toggle("Show Charts", value=st.session_state.show_charts)
        show_maps = st.toggle("Show Maps", value=st.session_state.show_maps)
        enable_alerts = st.toggle("Weather Alerts", value=True)
        
        # Save Settings Button
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            st.session_state.unit = "metric" if selected_unit == "Celsius (°C)" else "imperial"
            st.session_state.theme = selected_theme
            st.session_state.show_charts = show_charts
            st.session_state.show_maps = show_maps
            st.session_state.weather_data = None  # Clear cache to reload with new settings
            st.success("✅ Settings saved!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent Searches
        if st.session_state.search_history:
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown("### 🔍 Recent Searches")
            for loc in reversed(st.session_state.search_history[-5:]):
                if st.button(f"📍 {loc}", key=f"sidebar_history_{loc}", use_container_width=True):
                    update_location(loc)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Favorites
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("### ⭐ Favorites")
        
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(f"📍 {fav}", key=f"fav_{fav}", use_container_width=True):
                        update_location(fav)
                with col2:
                    if st.button("🗑️", key=f"remove_{fav}"):
                        st.session_state.favorites.remove(fav)
                        st.success(f"Removed {fav}")
                        st.rerun()
        else:
            st.info("No favorites yet")
            
        if st.button("➕ Add Current to Favorites", use_container_width=True):
            if st.session_state.address not in st.session_state.favorites:
                st.session_state.favorites.append(st.session_state.address)
                st.success(f"Added {st.session_state.address} to favorites!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export Data
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Export Data")
        
        if st.button("Export Weather Data", use_container_width=True):
            if st.session_state.weather_data:
                data = {
                    "location": st.session_state.address,
                    "coordinates": {
                        "lat": st.session_state.lat,
                        "lon": st.session_state.lon
                    },
                    "current_weather": st.session_state.weather_data,
                    "forecast": st.session_state.forecast_data,
                    "air_quality": st.session_state.air_quality_data,
                    "timestamp": datetime.now().isoformat(),
                    "unit": st.session_state.unit
                }
                
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_str,
                    file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("No weather data to export")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # About Section
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        st.markdown("### ℹ️ About")
        st.markdown(f"""
        **{Config.APP_NAME} v{Config.APP_VERSION}**
        
        A professional weather application with advanced features.
        
        **Data Source:** OpenWeatherMap API
        """)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Display sidebar
    display_sidebar()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # App header
        ui.display_app_header()
    
    with col2:
        # Current time display
        current_time = datetime.now().strftime('%I:%M %p')
        st.markdown(f"""
        <div style="text-align: right; padding: 20px 0;">
            <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">
                ⏰ {current_time}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Search section
    search_query = ui.display_search_section()
    
    # Check for quick location
    if hasattr(st.session_state, 'quick_location'):
        update_location(st.session_state.quick_location)
        del st.session_state.quick_location
    
    # Check for search
    if search_query:
        update_location(search_query)
    
    # Check for current location
    if hasattr(st.session_state, 'use_current_location') and st.session_state.use_current_location:
        st.info("📍 Please use search to find locations.")
        del st.session_state.use_current_location
    
    # Fetch weather data
    fetch_weather_data()
    
    if st.session_state.weather_data:
        # Current weather section
        ui.display_current_weather(st.session_state.weather_data, st.session_state.address)
        
        # 7-hour forecast
        if st.session_state.hourly_data:
            ui.display_7_hour_forecast(st.session_state.hourly_data)
        
        # 7-day forecast
        if st.session_state.daily_data:
            ui.display_daily_forecast(st.session_state.daily_data)
        
        # Temperature chart
        if st.session_state.show_charts and st.session_state.hourly_data:
            ui.display_temperature_chart(st.session_state.hourly_data)
        
        # Air quality
        if st.session_state.air_quality_data:
            ui.display_air_quality(st.session_state.air_quality_data)
        
        # Map
        if st.session_state.show_maps:
            try:
                map_manager.display_map(
                    st.session_state.lat,
                    st.session_state.lon,
                    st.session_state.address
                )
            except Exception as e:
                st.error(f"Map error: {str(e)}")
                st.info(f"**📍 Location:** {st.session_state.address}")
                st.info(f"**🌍 Coordinates:** {st.session_state.lat:.4f}, {st.session_state.lon:.4f}")
        
        # Action buttons at bottom
        st.markdown('<div style="margin: 30px 0;"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
                st.session_state.weather_data = None
                st.rerun()
        
        with col2:
            if st.button("📱 Share Weather", use_container_width=True):
                temp = st.session_state.weather_data['main']['temp']
                weather_desc = st.session_state.weather_data['weather'][0]['description']
                share_text = f"🌤️ Weather in {st.session_state.address}: {temp:.1f}°C, {weather_desc}"
                st.info(f"**Copy to share:**\n\n`{share_text}`")
        
        with col3:
            if st.button("📊 More Analytics", use_container_width=True):
                st.info("Advanced analytics feature coming soon!")
    
    else:
        # Show loading or error state
        st.error("⚠️ Weather data could not be loaded. Please try again.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Retry Loading", use_container_width=True, type="primary"):
                st.session_state.weather_data = None
                st.rerun()
        with col2:
            if st.button("🏠 Use Default Location", use_container_width=True):
                update_location(Config.DEFAULT_LOCATION)
    
    # Footer
    st.markdown("---")
    
    last_update = st.session_state.last_update.strftime('%I:%M %p') if st.session_state.last_update else "Never"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0; color: {Config.COLORS['text_secondary']};">
        <p style="margin: 0 0 8px 0; font-weight: 500; font-size: 14px;">
            🌤️ {Config.APP_NAME} v{Config.APP_VERSION} • 
            Last updated: {last_update} • 
            Location: {st.session_state.address}
        </p>
        <p style="margin: 0; font-size: 12px; opacity: 0.8;">
            Powered by OpenWeatherMap API • 
            <a href="#" style="color: {Config.COLORS['primary']}; text-decoration: none;">Privacy</a> • 
            <a href="#" style="color: {Config.COLORS['primary']}; text-decoration: none;">Terms</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()