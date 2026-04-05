import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self, groq_key=None):
        self.groq_api_key = groq_key or os.getenv("GROQ_API_KEY")
        self.groq_model_name = "llama-3.3-70b-versatile" # En güçlü ve stabil Groq modeli
        
        self.groq_client = None
        self._setup_groq()

    def _setup_groq(self):
        if self.groq_api_key:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"Groq Setup Error: {e}")
                self.groq_client = None

    def generate_content(self, prompt):
        try:
            if not self.groq_client: return "HATA: Groq API anahtarı ayarlanmamış."
            
            chat_completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.groq_model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"AI Hatası (GROQ): {str(e)}"

    def generate_lesson_plan(self, topic):
        prompt = f"""
        Sen uzman bir eğitmensin. '{topic}' konusu üzerine derinlemesine, kapsamlı ve profesyonel bir ders içeriği oluştur. 
        Lütfen şu bölümleri KURALLARA UYGUN şekilde hazırla:
        
        1. **Ders Başlığı ve Giriş**: Konunun kapsamı ve neden öğrenilmesi gerektiği.
        2. **🔍 Detaylı Ders Anlatımı**: Konuyu tüm detaylarıyla, teknik derinliğiyle ve örnek vakalarla açıkla. Bu bölüm oldukça uzun ve öğretici olmalıdır. 
        3. **🎯 Bölüm Sonu Özeti**: Dersteki en kritik noktaları maddeler halinde özetleyen kısa bir bölüm.
        4. **📝 Bölüm Sonu Quiz**: En az 5 soruluk bir test. Her soru için 4 seçenek (A, B, C, D) ve en sonda doğru cevap anahtarı bulunmalıdır.
        
        Dil: Türkçe. Markdown formatında şık bir sunum yap.
        """
        return self.generate_content(prompt)

    def get_interactive_quiz(self, content):
        prompt = f"""
        Aşağıdaki ders içeriğinden sadece QUIZ bölümünü al ve JSON formatında bir liste olarak döndür.
        Örnek format:
        [
            {{"question": "Soru metni", "options": ["A şıkkı", "B şıkkı", "C şıkkı", "D şıkkı"], "answer": "A"}},
            ...
        ]
        Sadece JSON döndür, başka açıklama yazma.
        İçerik:
        {content}
        """
        raw_res = self.generate_content(prompt)
        
        # JSON bloğunu ayıkla (Markdown code block'ları temizle)
        json_match = re.search(r'\[.*\]', raw_res, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception as e:
                print(f"JSON Parse Error: {e}")
                return None
        return None
