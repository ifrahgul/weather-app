import folium
from streamlit_folium import folium_static
import streamlit as st
from config import Config

class MapManager:
    @staticmethod
    def create_map(lat, lon, location_name):
        """Create interactive map - FIXED attribution"""
        try:
            # Create map with CartoDB tiles (no attribution issues)
            m = folium.Map(
                location=[lat, lon],
                zoom_start=Config.MAP_ZOOM,
                tiles="CartoDB positron",
                control_scale=True,
                attr='CartoDB'
            )
            
            # Add marker
            folium.Marker(
                [lat, lon],
                popup=f"<b>{location_name}</b><br>Lat: {lat:.4f}<br>Lon: {lon:.4f}",
                tooltip="Click for details",
                icon=folium.Icon(color='red', icon='cloud')
            ).add_to(m)
            
            # Add circle around location
            folium.Circle(
                location=[lat, lon],
                radius=1000,
                color=Config.COLORS['primary'],
                fill=True,
                fill_color=Config.COLORS['primary'],
                fill_opacity=0.2,
                weight=2
            ).add_to(m)
            
            return m
            
        except Exception as e:
            st.error(f"Map creation error: {str(e)}")
            return None
    
    @staticmethod
    def display_map(lat, lon, location_name):
        """Display interactive map in Streamlit"""
        try:
            st.markdown("""
            <div style="margin: 30px 0 20px 0;">
                <h3 style="color: #202124; font-size: 28px; font-weight: 700;">🗺️ Location Map</h3>
            </div>
            """, unsafe_allow_html=True)
            
            map_obj = MapManager.create_map(lat, lon, location_name)
            
            if map_obj:
                # Display map
                folium_static(map_obj, width=700, height=500)
                
                # Map controls and info
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📍 Latitude", f"{lat:.4f}")
                
                with col2:
                    st.metric("📍 Longitude", f"{lon:.4f}")
                
                with col3:
                    # Google Maps link
                    google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                    st.markdown(f"""
                    <div style="margin-top: 8px;">
                        <a href="{google_maps_url}" target="_blank">
                            <button style="background: {Config.COLORS['primary']}; color: white; border: none; 
                                    padding: 10px 15px; border-radius: 8px; cursor: pointer; width: 100%; 
                                    font-weight: 500; font-size: 14px;">
                                📍 Google Maps
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                # Fallback display
                st.warning("⚠️ Interactive map could not be loaded. Showing location details instead.")
                
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📍 Latitude", f"{lat:.4f}")
                
                with col2:
                    st.metric("📍 Longitude", f"{lon:.4f}")
                
                with col3:
                    st.metric("🌍 Location", location_name)
                
                # Google Maps link
                google_maps_url = f"https://www.google.com/maps?q={lat},{lon}"
                st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                    <a href="{google_maps_url}" target="_blank" style="text-decoration: none;">
                        <button style="background: {Config.COLORS['primary']}; color: white; border: none; 
                                padding: 12px 25px; border-radius: 10px; cursor: pointer; 
                                font-weight: 600; font-size: 16px; width: 100%;">
                            📍 View on Google Maps
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
        except Exception as e:
            # Simple fallback
            st.error(f"Map display error: {str(e)}")
            st.info(f"**📍 Location:** {location_name}")
            st.info(f"**🌍 Coordinates:** {lat:.4f}, {lon:.4f}")