import streamlit as st
import speech_recognition as sr

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def listen(self):
        """Listen for voice commands"""
        try:
            with sr.Microphone() as source:
                st.info("🎤 Listening... Speak now")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            st.warning("⏱️ Timeout")
            return None
        except sr.UnknownValueError:
            st.error("❌ Could not understand")
            return None
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
            return None