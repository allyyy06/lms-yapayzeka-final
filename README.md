# AI-Powered Learning Management System (LMS) 🎓

An advanced, AI-integrated LMS built with Streamlit and Groq. Design, manage, and export AI-generated courses with interactive quizzes and progress tracking.

[Türkçe dökümantasyon için aşağı kaydırın.](#türkçe)

---

## 🚀 Features

- **AI-Powered Course Generation**: Create comprehensive lesson plans, summaries, and quizzes using the power of **Groq (Llama 3.3)**.
- **Interactive Quiz Mode**: Real-time self-assessment extracted from course content with live scoring.
- **Progress Tracking**: Monitor your learning journey with a dedicated dashboard and score persistence.
- **PDF Export**: Download your lessons as professional PDFs with full Unicode (Turkish) support.
- **Advanced UI/UX**: Premium, responsive dashboard with Light/Dark mode compatibility.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lms-yapayzeka-final.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables in a `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🌐 Live Deployment (Streamlit Cloud)

1. Push your code to GitHub (ensure `.env` and `lms.db` are ignored).
2. Connect your repository to [Streamlit Cloud](https://share.streamlit.io/).
3. In the "Advanced Settings", add your `GROQ_API_KEY` to the **Secrets** section.

---

<a name="türkçe"></a>
# AI Destekli Eğitim Yönetim Sistemi (LMS) 🇹🇷

Streamlit ve Groq altyapısıyla geliştirilmiş, yapay zeka entegreli gelişmiş bir LMS platformu.

## ✨ Özellikler

- **Yapay Zeka ile Kurs Tasarımı**: Groq (Llama 3.3) kullanarak saniyeler içinde müfredat, detaylı anlatım ve quiz oluşturun.
- **İnteraktif Quiz Modu**: Ders içeriğinden anlık üretilen testler ile bilginizi ölçün.
- **Gelişim Takibi**: Dashboard üzerinden geçmiş quiz skorlarınızı ve öğrenme sürecinizi takip edin.
- **PDF Dışa Aktarma**: Ders notlarını Türkçe karakter desteğiyle profesyonel PDF formatında indirin.
- **Premium Arayüz**: Hem gece hem gündüz moduyla uyumlu, modern ve hızlı kullanıcı deneyimi.

## ⚙️ Kurulum

1. Depoyu klonlayın.
2. `pip install -r requirements.txt` komutuyla kütüphaneleri yükleyin.
3. `.env` dosyasına `GROQ_API_KEY` anahtarınızı ekleyin.
4. `streamlit run app.py` ile başlatın.

## 📄 Lisans
Bu proje MIT lisansı ile lisanslanmıştır.
