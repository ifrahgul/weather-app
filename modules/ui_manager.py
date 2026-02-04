import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from config import Config

class UIManager:
    @staticmethod
    def display_app_header():
        """Display app header"""
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0 30px 0;">
            <h1 style="color: {Config.COLORS['text_primary']}; margin-bottom: 10px; font-size: 42px; font-weight: 800;">
                🌤️ Weather Forecast
            </h1>
            <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 18px;">
                Real-time weather updates & forecasts
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_search_section():
        """Display search section"""
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_query = st.text_input(
                "",
                placeholder="🔍 Search city or location...",
                help="Enter city name to get weather",
                key="search_input",
                label_visibility="collapsed"
            )
        
        with col2:
            search_clicked = st.button("Search", use_container_width=True, type="primary", key="search_btn")
        
        with col3:
            if st.button("📍 Current", use_container_width=True, key="current_btn"):
                st.session_state.use_current_location = True
        
        # Quick locations
        st.markdown('<div style="margin: 20px 0 10px 0;">', unsafe_allow_html=True)
        st.markdown('<p style="color: #5f6368; font-size: 14px; font-weight: 600;">Popular Cities:</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        locations = ["Karachi", "Lahore", "Islamabad", "Mumbai", "Delhi", "Dubai", "London", "New York"]
        cols = st.columns(8)
        
        for idx, loc in enumerate(locations):
            with cols[idx]:
                if st.button(loc, key=f"quick_{loc}", use_container_width=True):
                    st.session_state.quick_location = loc
        
        return search_query if search_clicked else None
    
    @staticmethod
    def display_current_weather(weather_data, location):
        """Display current weather with icons"""
        if not weather_data:
            st.warning("Weather data not available")
            return
        
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        
        # Location header
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f'<div style="text-align: center;"><h2 style="color: {Config.COLORS["text_primary"]}; margin: 0; font-size: 32px; font-weight: 700;">{location}</h2></div>', unsafe_allow_html=True)
        
        # Main weather display
        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description'].title()
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 20px;">
                    <div>
                        <div style="font-size: 72px; font-weight: 300; color: {Config.COLORS['text_primary']}; line-height: 1;">
                            {temp:.1f}°C
                        </div>
                        <p style="color: {Config.COLORS['text_secondary']}; font-size: 20px; margin: 5px 0;">
                            {weather_desc}
                        </p>
                    </div>
                    <img src="{icon_url}" width="120">
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Weather metrics grid
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Air Quality
            st.markdown(f"""
            <div style="margin-bottom: 30px; padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">🌫️</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Air Quality</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    Moderate
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Wind Speed
            wind_speed = weather_data['wind']['speed']
            st.markdown(f"""
            <div style="margin-bottom: 30px; padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">💨</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Wind Speed</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {wind_speed} km/h
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Humidity
            humidity = weather_data['main']['humidity']
            st.markdown(f"""
            <div style="padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">💧</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Humidity</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {humidity}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Wind Direction
            wind_deg = weather_data['wind'].get('deg', 0)
            st.markdown(f"""
            <div style="margin-bottom: 30px; padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">🧭</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Wind Direction</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {wind_deg}°
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Highest Temperature
            temp_max = weather_data['main']['temp_max']
            st.markdown(f"""
            <div style="margin-bottom: 30px; padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">🌡️</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">High Temp</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {temp_max:.1f}°C
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Visibility
            visibility = weather_data.get('visibility', 10000) / 1000
            st.markdown(f"""
            <div style="padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">👁️</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Visibility</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {visibility:.1f} km
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Lowest Temperature
            temp_min = weather_data['main']['temp_min']
            st.markdown(f"""
            <div style="margin-bottom: 30px; padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">🌡️</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Low Temp</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {temp_min:.1f}°C
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Pressure
            pressure = weather_data['main']['pressure']
            st.markdown(f"""
            <div style="margin-bottom: 30px; padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                    <span style="font-size: 24px;">🎈</span>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Pressure</p>
                </div>
                <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 28px; font-weight: 700;">
                    {pressure} hPa
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Sunrise & Sunset
            if 'sys' in weather_data:
                sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
                sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
                st.markdown(f"""
                <div style="padding: 20px; background: rgba(26, 115, 232, 0.05); border-radius: 12px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="font-size: 24px;">🌅</span>
                        <p style="color: {Config.COLORS['text_secondary']}; margin: 0; font-size: 16px; font-weight: 500;">Sunrise / Sunset</p>
                    </div>
                    <p style="color: {Config.COLORS['primary']}; margin: 0; font-size: 24px; font-weight: 700;">
                        {sunrise} / {sunset}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_7_hour_forecast(hourly_data):
        """Display 7-hour forecast"""
        if not hourly_data:
            st.info("Hourly forecast data not available")
            return
        
        st.markdown('<div style="margin: 30px 0 20px 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #202124; font-size: 28px; font-weight: 700;">📅 Next 7 Hours</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        
        # Create 7 columns for each hour
        cols = st.columns(7)
        
        for idx, hour in enumerate(hourly_data[:7]):
            with cols[idx]:
                icon_url = f"https://openweathermap.org/img/wn/{hour['icon']}@2x.png"
                
                st.markdown(f"""
                <div style="text-align: center; padding: 15px 10px;">
                    <p style="font-weight: 600; margin: 0 0 15px 0; color: {Config.COLORS['text_primary']}; font-size: 18px;">
                        {hour['time']}
                    </p>
                    <div style="margin: 15px 0;">
                        <img src="{icon_url}" width="60">
                    </div>
                    <p style="font-size: 24px; margin: 10px 0; color: {Config.COLORS['primary']}; font-weight: 700;">
                        {hour['temp']}°
                    </p>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 5px 0; font-size: 14px;">
                        {hour['weather']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_daily_forecast(daily_data):
        """Display 7-day forecast"""
        if not daily_data or len(daily_data) == 0:
            st.info("Daily forecast data not available")
            return
        
        st.markdown('<div style="margin: 30px 0 20px 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #202124; font-size: 28px; font-weight: 700;">📆 7-Day Forecast</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        
        # Create cards for each day
        for idx, day in enumerate(daily_data[:7]):
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 2, 1])
            
            with col1:
                day_name = day.get('day', 'N/A')
                if idx == 0:
                    day_name = "Today"
                elif idx == 1:
                    day_name = "Tomorrow"
                
                st.markdown(f'<div style="padding: 15px 0;"><p style="font-weight: 700; margin: 0; color: {Config.COLORS["text_primary"]}; font-size: 18px;">{day_name}</p></div>', unsafe_allow_html=True)
            
            with col2:
                icon_url = f"https://openweathermap.org/img/wn/{day.get('icon', '01d')}@2x.png"
                st.image(icon_url, width=60)
            
            with col3:
                st.markdown(f'<div style="padding: 15px 0;"><p style="font-weight: 600; margin: 0; color: {Config.COLORS["text_primary"]}; font-size: 18px;">{day.get("weather", "N/A")}</p></div>', unsafe_allow_html=True)
            
            with col4:
                temp = day.get('temp', 'N/A')
                max_temp = day.get('max_temp', 'N/A')
                min_temp = day.get('min_temp', 'N/A')
                
                st.markdown(f"""
                <div style="padding: 15px 0;">
                    <p style="font-size: 22px; font-weight: 700; margin: 0; color: {Config.COLORS['primary']};">
                        {temp}°C
                    </p>
                    <p style="color: {Config.COLORS['text_secondary']}; margin: 5px 0 0 0; font-size: 14px;">
                        H: {max_temp}° • L: {min_temp}°
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                precipitation = day.get('precipitation', 0)
                if precipitation > 0:
                    st.markdown(f"""
                    <div style="padding: 15px 0; text-align: center;">
                        <div style="background: rgba(52, 168, 83, 0.15); border-radius: 10px; padding: 8px 12px;">
                            <p style="color: #34a853; margin: 0; font-weight: 700; font-size: 16px;">🌧️ {precipitation}%</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div style="padding: 15px 0; text-align: center;"><p style="color: #fbbc04; margin: 0; font-size: 16px; font-weight: 600;">☀️ 0%</p></div>', unsafe_allow_html=True)
            
            if idx < 6:
                st.markdown('<hr style="margin: 15px 0; border-color: rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_temperature_chart(hourly_data):
        """Display temperature chart"""
        if not hourly_data or len(hourly_data) < 3:
            return
        
        st.markdown('<div style="margin: 30px 0 20px 0;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #202124; font-size: 28px; font-weight: 700;">📊 Temperature Trend</h3>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="weather-card">', unsafe_allow_html=True)
        
        # Create DataFrame
        df = pd.DataFrame(hourly_data)
        
        # Create chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['temp'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color=Config.COLORS['primary'], width=4),
            marker=dict(size=10, color=Config.COLORS['primary'], symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(26, 115, 232, 0.1)'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            plot_bgcolor='rgba(255,255,255,0.95)',
            paper_bgcolor='rgba(255,255,255,0.95)',
            height=400,
            font=dict(size=14),
            hovermode='x unified',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                tickangle=0
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            margin=dict(l=40, r=40, t=30, b=40),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def display_air_quality(aqi_data):
        """Display air quality information - FIXED: Pure Streamlit components"""
        if not aqi_data:
            st.info("Air quality data not available for this location")
            return
        
        try:
            if 'list' not in aqi_data or len(aqi_data['list']) == 0:
                st.info("Air quality data format is not valid")
                return
            
            aqi = aqi_data['list'][0]['main']['aqi']
            
            # AQI levels
            aqi_levels = {
                1: {"label": "Good", "color": "#34a853", "emoji": "😊", "desc": "Air quality is satisfactory"},
                2: {"label": "Fair", "color": "#fbbc04", "emoji": "🙂", "desc": "Acceptable air quality"},
                3: {"label": "Moderate", "color": "#ff9900", "emoji": "😐", "desc": "Sensitive groups affected"},
                4: {"label": "Poor", "color": "#ea4335", "emoji": "😷", "desc": "Unhealthy for everyone"},
                5: {"label": "Very Poor", "color": "#a50e0e", "emoji": "🤢", "desc": "Health alert - Limit outdoor activities"}
            }
            
            level = aqi_levels.get(aqi, aqi_levels[3])
            
            # Display AQI information using Streamlit components
            st.markdown("""
            <div style="margin: 30px 0 20px 0;">
                <h3 style="color: #202124; font-size: 28px; font-weight: 700;">🌬️ Air Quality</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create two columns
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # AQI Box
                st.markdown(f"""
                <div style="text-align: center; padding: 25px; background: {level['color']}15; 
                         border-radius: 16px; border-left: 6px solid {level['color']};">
                    <div style="font-size: 48px; margin-bottom: 15px;">{level['emoji']}</div>
                    <div style="font-size: 42px; font-weight: 700; color: {level['color']}; margin-bottom: 10px;">
                        AQI {aqi}
                    </div>
                    <div style="color: {Config.COLORS['text_primary']}; font-size: 20px; font-weight: 600;">
                        {level['label']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Health Recommendations Box
                st.markdown(f"""
                <div style="padding: 30px; background: rgba(255, 255, 255, 0.9); border-radius: 16px;">
                    <h4 style="color: #202124; margin-bottom: 15px; font-size: 22px;">
                        Health Recommendations
                    </h4>
                    <p style="color: #202124; margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                        {level['desc']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Air Quality Level with Progress Bar
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            
            # Create a container for AQI level display
            with st.container():
                col_label, col_value = st.columns([1, 1])
                with col_label:
                    st.markdown('<p style="color: #5f6368; font-weight: 500; margin: 0;">Air Quality Level</p>', unsafe_allow_html=True)
                with col_value:
                    st.markdown(f'<p style="color: {level["color"]}; font-weight: 600; margin: 0; text-align: right;">{level["label"]}</p>', unsafe_allow_html=True)
                
                # Progress bar
                progress_html = f"""
                <div style="background: rgba(0,0,0,0.1); height: 12px; border-radius: 6px; overflow: hidden; margin-top: 10px;">
                    <div style="width: {(aqi/5)*100}%; height: 100%; background: {level['color']};"></div>
                </div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)
            
            # Health alerts based on AQI level using Streamlit native components
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            
            if aqi <= 2:
                st.success("✅ **Good for outdoor activities** - Air quality poses little or no risk.")
            elif aqi == 3:
                st.warning("⚠️ **Sensitive groups should limit outdoor exposure** - Children and people with respiratory issues may experience symptoms.")
            else:
                st.error("❌ **Limit outdoor activities** - Everyone may begin to experience health effects.")
                
        except Exception as e:
            st.error(f"Error displaying air quality data: {str(e)}")
            st.info("Air quality data format is not as expected.")