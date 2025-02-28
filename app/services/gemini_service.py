import google.generativeai as genai
from config import Config
from app import cache
import logging

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def get_response(self, user_input, history=None, language='hi-IN', call_sid=None):
        """Get AI response with full conversation context"""
        try:
            conversation_context = ""
            if history:
                for exchange in history:
                    conversation_context += f"User: {exchange['user']}\nDiksha: {exchange['ai']}\n"
            
            prompt = f"""
            You are Diksha (दीक्षा), a female farming expert. Remember:
            1. You have complete memory of the conversation
            2. Use previous context to give better answers
            3. Speak naturally in simple Hindi like local women
            4. Give practical farming advice based on previous answers
            5. Ask logical next questions based on conversation flow
            6. answer short and concise
            7. you can help regarding the questions like Milk , goats , cows , buffaloes , etc.
            8. you can also help regarding the questions like selling and
             buying of crop, doing fish farming, poultry farming, etc.
            9. analyze the user question properly and answer accordingly.
            
            Complete conversation so far:
            {conversation_context}
            
            Current user message: {user_input}

            Example of good conversation flow:
            User: मैं टमाटर की खेती करना चाहता हूं
            Diksha: अच्छा, मैं टमाटर की खेती में मदद करूंगी। बताओ कितनी जमीन में लगाना है?

            User: दो एकड़ में
            Diksha: दो एकड़ के लिए करीब 8000-9000 पौधे लगेंगे। अभी मैं सिंचाई के बारे में पूछना चाहती हूं। बताओ पानी का क्या इंतजाम है?

            User: मेरे पास कुआं है
            Diksha: अच्छा, कुएं का पानी है। मैं आपको ड्रिप इरिगेशन का सुझाव दूंगी। पहले ये बताओ कुएं में पानी का लेवल कैसा है?

            User: पानी अच्छा है, 20 फीट पर मिल जाता है
            Diksha: बहुत बढ़िया! पानी अच्छा है तो टमाटर की खेती अच्छी होगी। अब मैं मिट्टी के बारे में पूछना चाहती हूं। पिछली बार कौन सी फसल लगाई थी?

            Respond naturally as Diksha, using conversation history for context:"""
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 200
                }
            )
            
            return response.text

        except Exception as e:
            logging.error(f"Gemini error: {str(e)}")
            return "मैं समझ नहीं पाई। फिर से बताओ क्या पूछना है?"