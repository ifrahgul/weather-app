import streamlit as st
from config import Config

class ThemeManager:
    @staticmethod
    def get_css():
        """Get CSS with background image and modern styling"""
        background_image = Config.BACKGROUND_IMAGE
        
        return f"""
        <style>
            /* Main app with background image */
            .stApp {{
                background: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.94)), 
                            url('{background_image}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
            }}
            
            /* Weather cards */
            .weather-card {{
                background: {Config.COLORS['card_bg']};
                border-radius: 20px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
                border: 1px solid rgba(0,0,0,0.08);
                backdrop-filter: blur(10px);
            }}
            
            /* Input fields */
            .stTextInput > div > div > input {{
                background: rgba(255, 255, 255, 0.95) !important;
                color: {Config.COLORS['text_primary']} !important;
                border: 2px solid {Config.COLORS['primary']} !important;
                border-radius: 15px !important;
                padding: 15px 25px !important;
                font-size: 16px !important;
                height: 55px !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                transition: all 0.3s ease !important;
            }}
            
            .stTextInput > div > div > input:focus {{
                box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.2) !important;
                border-color: {Config.COLORS['secondary']} !important;
            }}
            
            /* Primary buttons */
            .stButton > button {{
                background: linear-gradient(135deg, {Config.COLORS['primary']}, {Config.COLORS['secondary']}) !important;
                color: white !important;
                border: none !important;
                border-radius: 15px !important;
                padding: 14px 28px !important;
                font-weight: 600 !important;
                font-size: 15px !important;
                transition: all 0.3s ease !important;
                height: 55px !important;
                box-shadow: 0 6px 20px rgba(26, 115, 232, 0.3);
            }}
            
            .stButton > button:hover {{
                transform: translateY(-3px) !important;
                box-shadow: 0 8px 25px rgba(26, 115, 232, 0.4) !important;
                background: linear-gradient(135deg, {Config.COLORS['secondary']}, {Config.COLORS['primary']}) !important;
            }}
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
                background: rgba(255, 255, 255, 0.9);
                padding: 10px;
                border-radius: 15px;
                margin: 30px 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }}
            
            .stTabs [data-baseweb="tab"] {{
                background: rgba(255, 255, 255, 0.9);
                color: {Config.COLORS['text_primary']} !important;
                border-radius: 12px;
                padding: 12px 28px;
                font-weight: 500;
                font-size: 14px;
                border: 1px solid rgba(0,0,0,0.08);
                transition: all 0.3s ease;
            }}
            
            .stTabs [aria-selected="true"] {{
                background: linear-gradient(135deg, {Config.COLORS['primary']}, {Config.COLORS['secondary']}) !important;
                color: white !important;
                border-color: {Config.COLORS['primary']} !important;
                box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
            }}
            
            /* Hide Streamlit elements */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            
            /* Custom scrollbar */
            ::-webkit-scrollbar {{
                width: 10px;
                height: 10px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: rgba(0,0,0,0.05);
                border-radius: 10px;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: {Config.COLORS['primary']};
                border-radius: 10px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: {Config.COLORS['secondary']};
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .weather-card {{
                    padding: 20px;
                    margin: 10px 0;
                }}
                
                .folium-map {{
                    height: 300px !important;
                }}
            }}
        </style>
        """