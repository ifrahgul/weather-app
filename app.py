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
    initial_sidebar_state="expanded",
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

# Initialize session state - sidebar_visibility کو یقینی بنائیں
def init_session_state():
    """Initialize all session state variables"""
    # ضروری session state variables
    required_vars = {
        'initialized': False,
        'location': Config.DEFAULT_LOCATION,
        'lat': Config.DEFAULT_LAT,
        'lon': Config.DEFAULT_LON,
        'address': Config.DEFAULT_LOCATION,
        'weather_data': None,
        'hourly_data': None,
        'daily_data': None,
        'air_quality_data': None,
        'forecast_data': None,
        'last_update': None,
        'search_history': [],
        'favorites': [],
        'unit': "metric",
        'theme': "Auto",
        'show_charts': True,
        'show_maps': True,
        'use_current_location': False,
        'sidebar_visibility': "visible"  # یہ لائن اہم ہے
    }
    
    # Initialize each variable if not exists
    for var, default_val in required_vars.items():
        if var not in st.session_state:
            st.session_state[var] = default_val
    
    # Mark as initialized
    if not st.session_state.initialized:
        st.session_state.initialized = True

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
            
            # Ensure sidebar visibility
            if 'sidebar_visibility' not in st.session_state:
                st.session_state.sidebar_visibility = "visible"
            
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
        # Sidebar header with toggle button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px 0 20px 0;">
                <h3 style="color: {Config.COLORS['primary']}; margin: 0;">⚙️ Settings</h3>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("✕", key="close_sidebar", help="Close sidebar"):
                st.session_state.sidebar_visibility = "collapsed"
                st.rerun()
        
        # Check sidebar visibility with safe access
        sidebar_visible = st.session_state.get('sidebar_visibility', 'visible')
        
        if sidebar_visible == "visible":
            # Temperature Unit
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            unit_options = ["Celsius (°C)", "Fahrenheit (°F)"]
            selected_unit = st.selectbox(
                "Temperature Unit",
                unit_options,
                index=0 if st.session_state.unit == "metric" else 1
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Theme
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            theme_options = ["Auto", "Light", "Dark", "High Contrast"]
            selected_theme = st.selectbox(
                "Theme",
                theme_options,
                index=theme_options.index(st.session_state.get('theme', 'Auto'))
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Features Toggles
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown("### 🔧 Features")
            show_charts = st.toggle("Show Charts", value=st.session_state.get('show_charts', True))
            show_maps = st.toggle("Show Maps", value=st.session_state.get('show_maps', True))
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Save Settings Button
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            if st.button("💾 Save Settings", use_container_width=True, type="primary"):
                st.session_state.unit = "metric" if selected_unit == "Celsius (°C)" else "imperial"
                st.session_state.theme = selected_theme
                st.session_state.show_charts = show_charts
                st.session_state.show_maps = show_maps
                st.session_state.weather_data = None
                st.success("✅ Settings saved!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recent Searches
            search_history = st.session_state.get('search_history', [])
            if search_history:
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                st.markdown("### 🔍 Recent Searches")
                for loc in reversed(search_history[-5:]):
                    if st.button(f"📍 {loc}", key=f"sidebar_history_{loc}", use_container_width=True):
                        update_location(loc)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Favorites
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            st.markdown("### ⭐ Favorites")
            
            favorites = st.session_state.get('favorites', [])
            if favorites:
                for fav in favorites:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        if st.button(f"📍 {fav}", key=f"fav_{fav}", use_container_width=True):
                            update_location(fav)
                    with col2:
                        if st.button("🗑️", key=f"remove_{fav}"):
                            favorites.remove(fav)
                            st.session_state.favorites = favorites
                            st.success(f"Removed {fav}")
                            st.rerun()
            else:
                st.info("No favorites yet")
                
            if st.button("➕ Add Current to Favorites", use_container_width=True):
                current_address = st.session_state.get('address', '')
                if current_address and current_address not in favorites:
                    favorites.append(current_address)
                    st.session_state.favorites = favorites
                    st.success(f"Added {current_address} to favorites!")
                    st.rerun()
            
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
        
        else:
            # اگر sidebar بند ہے تو صرف ایک بٹن دکھائیں
            st.markdown('<div class="weather-card">', unsafe_allow_html=True)
            if st.button("⚙️ Open Settings", use_container_width=True, type="primary"):
                st.session_state.sidebar_visibility = "visible"
                st.rerun()
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
    
    if st.session_state.get('weather_data'):
        # Current weather section
        ui.display_current_weather(
            st.session_state.weather_data, 
            st.session_state.get('address', 'Unknown Location')
        )
        
        # 7-hour forecast
        if st.session_state.hourly_data:
            ui.display_7_hour_forecast(st.session_state.hourly_data)
        
        # 7-day forecast
        if st.session_state.daily_data:
            ui.display_daily_forecast(st.session_state.daily_data)
        
        # Temperature chart
        if st.session_state.get('show_charts', True) and st.session_state.hourly_data:
            ui.display_temperature_chart(st.session_state.hourly_data)
        
        # Air quality
        if st.session_state.air_quality_data:
            ui.display_air_quality(st.session_state.air_quality_data)
        
        # Map
        if st.session_state.get('show_maps', True):
            try:
                map_manager.display_map(
                    st.session_state.lat,
                    st.session_state.lon,
                    st.session_state.get('address', '')
                )
            except Exception as e:
                st.error(f"Map error: {str(e)}")
                st.info(f"**📍 Location:** {st.session_state.get('address', 'Unknown')}")
                st.info(f"**🌍 Coordinates:** {st.session_state.get('lat', 0):.4f}, {st.session_state.get('lon', 0):.4f}")
        
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
            Location: {st.session_state.get('address', 'Unknown')}
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
