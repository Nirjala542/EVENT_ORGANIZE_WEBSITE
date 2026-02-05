import os
import json
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from django.conf import settings

from book_my_event.settings import GEMINI_API_KEY

# Ensure log directory exists
LOG_DIR = Path('c:\\Users\\JOKER\\Desktop\\Book_my_event\\.cursor')
LOG_FILE = LOG_DIR / 'debug.log'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# #region agent log
try:
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"A","location":"chatbot.py:15","message":"Before genai.configure() call","data":{"api_key_received":bool(GEMINI_API_KEY),"api_key_length":len(GEMINI_API_KEY) if GEMINI_API_KEY else 0,"api_key_empty":not bool(GEMINI_API_KEY)},"timestamp":int(__import__('time').time()*1000)})+'\n')
except: pass
# #endregion

# Configure Gemini API
try:
    # #region agent log
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"D","location":"chatbot.py:28","message":"Attempting genai.configure()","data":{"api_key_provided":bool(GEMINI_API_KEY)},"timestamp":int(__import__('time').time()*1000)})+'\n')
    except: pass
    # #endregion
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    # #region agent log
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"D","location":"chatbot.py:33","message":"genai.configure() succeeded","data":{},"timestamp":int(__import__('time').time()*1000)})+'\n')
    except: pass
    # #endregion
except Exception as e:
    # #region agent log
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"D","location":"chatbot.py:38","message":"genai.configure() failed","data":{"error":str(e),"error_type":type(e).__name__},"timestamp":int(__import__('time').time()*1000)})+'\n')
    except: pass
    # #endregion
    pass  # Will be handled when chatbot is used

# System prompt for the chatbot
SYSTEM_PROMPT = """
You are a helpful assistant for the Book My Event website. You help users with:
1. Event information and details
2. How to book events
3. How to create events (for organizers)
4. FAQs about the platform
5. General guidance about using the website

Be concise, friendly, and helpful. If a question is not related to events or the website, politely redirect the user.
Always respond in a conversational manner and provide clear, actionable information.

Website Features:
- Event browsing and booking
- User registration and profiles
- Event organizer dashboard
- Community features
- Gallery
- Event filtering by date and location

Keep responses brief (2-3 sentences max for initial responses, more detailed if they ask follow-up questions).
"""

class EventsChatbot:
    def __init__(self):
        # #region agent log
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"G","location":"chatbot.py:68","message":"EventsChatbot.__init__","data":{"api_key_available":bool(GEMINI_API_KEY)}, "timestamp":int(__import__('time').time()*1000)})+'\n')
        except:
            pass
        # #endregion
        # List available models and use the first one that supports generateContent
        try:
            # #region agent log
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run7","hypothesisId":"H","location":"chatbot.py:80","message":"Listing available models","data":{},"timestamp":int(__import__('time').time()*1000)})+'\n')
            except:
                pass
            # #endregion
            
            # List available models that support generateContent
            available_models = []
            try:
                for model in genai.list_models():
                    if 'generateContent' in model.supported_generation_methods:
                        available_models.append(model.name)
                # #region agent log
                try:
                    with open(LOG_FILE, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run7","hypothesisId":"H","location":"chatbot.py:90","message":"Available models found","data":{"models":available_models[:5]},"timestamp":int(__import__('time').time()*1000)})+'\n')
                except:
                    pass
                # #endregion
            except Exception as list_err:
                # #region agent log
                try:
                    with open(LOG_FILE, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run7","hypothesisId":"H","location":"chatbot.py:97","message":"Could not list models","data":{"error":str(list_err)},"timestamp":int(__import__('time').time()*1000)})+'\n')
                except:
                    pass
                # #endregion
                pass
            
            # Use the first available model, or fallback to common names
            model_initialized = False
            
            # First, try models from the list_models() result
            if available_models:
                for model_name in available_models:
                    try:
                        # Remove 'models/' prefix if present, GenerativeModel handles it
                        clean_name = model_name.replace('models/', '')
                        self.model = genai.GenerativeModel(clean_name)
                        # #region agent log
                        try:
                            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                                f.write(json.dumps({"sessionId":"debug-session","runId":"run7","hypothesisId":"H","location":"chatbot.py:112","message":"Model initialized from available list","data":{"model_name":clean_name,"original_name":model_name},"timestamp":int(__import__('time').time()*1000)})+'\n')
                        except:
                            pass
                        # #endregion
                        model_initialized = True
                        break
                    except Exception as model_err:
                        # #region agent log
                        try:
                            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                                f.write(json.dumps({"sessionId":"debug-session","runId":"run7","hypothesisId":"H","location":"chatbot.py:121","message":"Model from list failed, trying next","data":{"model_name":clean_name,"error":str(model_err)[:100]},"timestamp":int(__import__('time').time()*1000)})+'\n')
                        except:
                            pass
                        # #endregion
                        continue
            
            # If no model from list worked, try common fallback names
            if not model_initialized:
                fallback_models = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-pro']
                for model_name in fallback_models:
                    try:
                        self.model = genai.GenerativeModel(model_name)
                        # #region agent log
                        try:
                            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                                f.write(json.dumps({"sessionId":"debug-session","runId":"run7","hypothesisId":"H","location":"chatbot.py:133","message":"Model initialized from fallback","data":{"model_name":model_name},"timestamp":int(__import__('time').time()*1000)})+'\n')
                        except:
                            pass
                        # #endregion
                        model_initialized = True
                        break
                    except Exception as model_err:
                        continue
            
            if not model_initialized:
                raise Exception(f"No working model found. Available models: {available_models[:3]}")
        except Exception as e:
            # #region agent log
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run6","hypothesisId":"H","location":"chatbot.py:128","message":"All model initialization attempts failed","data":{"error":str(e)},"timestamp":int(__import__('time').time()*1000)})+'\n')
            except:
                pass
            # #endregion
            # Re-raise so we can see the error
            raise
        self.conversation_history = []
    
    def add_message(self, role, content):
        """Add a message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content
        })
    
    def get_response(self, user_message):
        """Get chatbot response using Gemini API"""
        # #region agent log
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"A","location":"chatbot.py:95","message":"get_response() called","data":{"user_message_length":len(user_message),"api_key_available":bool(GEMINI_API_KEY)},"timestamp":int(__import__('time').time()*1000)})+'\n')
        except: pass
        # #endregion
        try:
            # Check if API key is configured
            if not GEMINI_API_KEY:
                # #region agent log
                try:
                    with open(LOG_FILE, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"A","location":"chatbot.py:102","message":"API key missing in get_response","data":{},"timestamp":int(__import__('time').time()*1000)})+'\n')
                except: pass
                # #endregion
                return "Sorry, I encountered an error: No API_KEY or ADC found. Please either: - Set the `GOOGLE_API_KEY` environment variable. - Manually pass the key with `genai.configure(api_key=my_api_key)`. - Or set up Application Default Credentials, see https://ai.google.dev/gemini-api/docs/oauth for more information.. Please try again later."
            
            # Add user message to history
            self.add_message('user', user_message)
            
            # Prepare conversation for API
            messages = [{'role': msg['role'], 'content': msg['content']} 
                       for msg in self.conversation_history]
            
            # #region agent log
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"E","location":"chatbot.py:115","message":"Before model.generate_content()","data":{},"timestamp":int(__import__('time').time()*1000)})+'\n')
            except: pass
            # #endregion
            
            # Get response from Gemini
            # #region agent log
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"E","location":"chatbot.py:138","message":"Calling model.generate_content()","data":{"api_key_configured":bool(GEMINI_API_KEY),"model_name":getattr(self.model, '_model_name', 'unknown')}, "timestamp":int(__import__('time').time()*1000)})+'\n')
            except: pass
            # #endregion
            
            response = self.model.generate_content(
                f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
            )
            
            # #region agent log
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"E","location":"chatbot.py:145","message":"model.generate_content() returned","data":{"has_response":bool(response),"has_text":hasattr(response, 'text')}, "timestamp":int(__import__('time').time()*1000)})+'\n')
            except: pass
            # #endregion
            
            bot_response = response.text
            
            # Add bot response to history
            self.add_message('assistant', bot_response)
            
            # #region agent log
            try:
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run3","hypothesisId":"E","location":"chatbot.py:128","message":"model.generate_content() succeeded","data":{"response_length":len(bot_response)},"timestamp":int(__import__('time').time()*1000)})+'\n')
            except: pass
            # #endregion
            
            return bot_response
        
        except Exception as e:
            # #region agent log
            try:
                import traceback
                with open(LOG_FILE, 'a', encoding='utf-8') as f:
                    f.write(json.dumps({"sessionId":"debug-session","runId":"run4","hypothesisId":"E","location":"chatbot.py:155","message":"Exception in get_response","data":{"error":str(e),"error_type":type(e).__name__,"traceback":traceback.format_exc()[:500]},"timestamp":int(__import__('time').time()*1000)})+'\n')
            except: pass
            # #endregion
            # Check if it's an API key error from Gemini
            error_str = str(e).lower()
            if 'api_key' in error_str or 'api key' in error_str or 'no api_key' in error_str or 'adc' in error_str:
                return f"Sorry, I encountered an error: {str(e)}. Please check your GEMINI_API_KEY in the .env file. Get a valid key from https://makersuite.google.com/app/apikey"
            return f"Sorry, I encountered an error: {str(e)}. Please try again later."
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
