import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from fpdf import FPDF
import matplotlib.pyplot as plt

# Proje Modülleri
from database import (
    init_db, SessionLocal, create_course, get_courses, 
    get_course_by_id, get_lessons_by_course, update_lesson_content, 
    delete_course, create_lesson, save_quiz_score, get_recent_scores
)
from ai_service import AIService

# Sayfa Konfigürasyonu
st.set_page_config(page_title="AI-LMS Pro Premium", layout="wide", initial_sidebar_state="expanded")

# --- MODERN CSS TASARIMI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dinamik Arka Plan */
    .main { background-color: transparent; }
    
    /* Kart Tasarımı */
    .card {
        padding: 2rem;
        border-radius: 1rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-left: 5px solid #4F46E5;
        transition: transform 0.2s;
    }
    .card:hover { transform: translateY(-5px); }
    
    /* İstatistik Kartları */
    .stat-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
    }
    .stat-card h3, .stat-card p { color: white !important; margin: 0; }
</style>
""", unsafe_allow_html=True)

# --- YARDIMCI FONKSİYONLAR ---
def export_as_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    
    # 🌍 Evrensel Unicode Desteği (Windows & Cloud/Linux uyumlu)
    local_font = "Roboto-Regular.ttf"
    windows_font = "C:/Windows/Fonts/arial.ttf"
    
    selected_font = None
    if os.path.exists(local_font):
        pdf.add_font("Roboto", "", local_font)
        selected_font = "Roboto"
    elif os.path.exists(windows_font):
        pdf.add_font("Arial", "", windows_font)
        selected_font = "Arial"
    
    if selected_font: pdf.set_font(selected_font, size=16)
    else: pdf.set_font("Helvetica", size=16)
        
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    if selected_font: pdf.set_font(selected_font, size=12)
    else: pdf.set_font("Helvetica", size=12)
        
    pdf.multi_cell(0, 10, txt=content)
    return bytes(pdf.output())

# --- BAŞLATMA ---
init_db()

def main():
    if 'page' not in st.session_state: st.session_state.page = "Dashboard"
    if 'selected_course_id' not in st.session_state: st.session_state.selected_course_id = None
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    
    if 'groq_key' not in st.session_state:
        load_dotenv()
        st.session_state.groq_key = os.getenv("GROQ_API_KEY", "")

    ai_service = AIService(groq_key=st.session_state.groq_key)

    with st.sidebar:
        st.title("🎓 AI-LMS PRO")
        st.divider()
        menu = {"🏠 Dashboard": "Dashboard", "📚 Kurslarım": "MyCourses", "🎨 AI Kurs Tasarla": "CreateCourse", "🤖 AI Asistanı": "AIAssistant", "⚙️ Ayarlar": "Settings"}
        for label, page_id in menu.items():
            if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.page = page_id
                st.session_state.selected_course_id = None
                st.session_state.quiz_active = False
                st.rerun()
        st.divider()
        st.info("⚡ Powered by Groq AI")
        
    if st.session_state.page == "Dashboard": render_dashboard()
    elif st.session_state.page == "MyCourses":
        if st.session_state.selected_course_id: render_course_detail(st.session_state.selected_course_id, ai_service)
        else: render_my_courses()
    elif st.session_state.page == "CreateCourse": render_create_course(ai_service)
    elif st.session_state.page == "AIAssistant": render_ai_assistant(ai_service)
    elif st.session_state.page == "Settings": render_settings()

def render_dashboard():
    st.markdown("# 🚀 Hoş Geldiniz!")
    db = SessionLocal()
    courses = get_courses(db)
    recent_scores = get_recent_scores(db)
    db.close()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div class="stat-card"><h3>{len(courses)}</h3><p>Aktif Kurs</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="stat-card"><h3>1,248</h3><p>Öğrenci</p></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="stat-card"><h3>{len(recent_scores)}</h3><p>Yeni Skorlar</p></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="stat-card"><h3>98%</h3><p>Memnuniyet</p></div>', unsafe_allow_html=True)

    st.divider()
    if recent_scores:
        st.markdown("#### 🌟 Son Quiz Skorları")
        score_data = pd.DataFrame([{"Ders No": s.lesson_id, "Skor": s.score, "Toplam": s.total} for s in recent_scores])
        st.table(score_data)

def render_my_courses():
    st.markdown("# 📚 Mevcut Kurslar")
    db = SessionLocal()
    courses = get_courses(db)
    if not courses: st.info("Henüz bir kursunuz yok.")
    else:
        for course in courses:
            with st.container():
                st.markdown(f'<div class="card"><h3>{course.title}</h3><p>{course.description}</p></div>', unsafe_allow_html=True)
                c1, c2 = st.columns([1, 4])
                if c1.button("📂 İçeriği Gör", key=f"view_{course.id}"):
                    st.session_state.selected_course_id = course.id
                    st.rerun()
                if c2.button("🗑️ Sil", key=f"del_{course.id}"):
                    delete_course(db, course.id)
                    st.rerun()
    db.close()

def render_course_detail(course_id, ai_service):
    db = SessionLocal()
    course = get_course_by_id(db, course_id)
    lessons = get_lessons_by_course(db, course_id)
    
    if st.button("⬅️ Geri Dön"):
        st.session_state.selected_course_id = None
        st.session_state.quiz_active = False
        st.rerun()

    if st.session_state.quiz_active:
        render_interactive_quiz(ai_service)
    else:
        st.title(f"📖 {course.title}")
        for lesson in lessons:
            with st.expander(f"📝 {lesson.title}", expanded=True):
                new_content = st.text_area("İçerik Editörü", value=lesson.content, height=400, key=f"edit_{lesson.id}")
                c1, c2, c3 = st.columns(3)
                if c1.button("💾 Güncelle", key=f"save_{lesson.id}"):
                    update_lesson_content(db, lesson.id, new_content)
                    st.success("İçerik güncellendi!")
                
                pdf_data = export_as_pdf(lesson.title, new_content)
                c2.download_button(label="📥 PDF İndir", data=pdf_data, file_name=f"{lesson.title}.pdf", key=f"pdf_{lesson.id}")
                
                if c3.button("❓ Quiz Moduna Gir", key=f"quiz_{lesson.id}"):
                    st.session_state.quiz_active = True
                    st.session_state.quiz_lesson_content = lesson.content
                    st.session_state.quiz_step = "initializing"
                    st.session_state.current_lesson_id = lesson.id
                    st.rerun()
    db.close()

def render_interactive_quiz(ai_service):
    st.markdown("## 📝 İnteraktif Quiz")
    if st.session_state.quiz_step == "initializing":
        with st.spinner("AI Soruları hazırlıyor..."):
            questions = ai_service.get_interactive_quiz(st.session_state.quiz_lesson_content)
            if questions:
                st.session_state.quiz_questions = questions
                st.session_state.quiz_step = "taking_quiz"
                st.session_state.current_q_idx = 0
                st.session_state.answers = []
                st.rerun()
    elif st.session_state.quiz_step == "taking_quiz":
        idx = st.session_state.current_q_idx
        q = st.session_state.quiz_questions[idx]
        st.subheader(f"Soru {idx + 1}: {q['question']}")
        choice = st.radio("Cevabınız:", q['options'], key=f"q_{idx}")
        if st.button("Sonraki Soru"):
            st.session_state.answers.append(choice)
            if idx + 1 < len(st.session_state.quiz_questions): st.session_state.current_q_idx += 1
            else: st.session_state.quiz_step = "finished"
            st.rerun()
    elif st.session_state.quiz_step == "finished":
        st.balloons()
        correct_count = 0
        for i, q in enumerate(st.session_state.quiz_questions):
            if st.session_state.answers[i][0] == q['answer'][0]: correct_count += 1
        st.success(f"Skor: {correct_count} / {len(st.session_state.quiz_questions)}")
        db = SessionLocal()
        save_quiz_score(db, 1, st.session_state.current_lesson_id, correct_count, len(st.session_state.quiz_questions))
        db.close()
        if st.button("Ders İçeriklerine Dön"):
            st.session_state.quiz_active = False ; st.rerun()

def render_create_course(ai_service):
    st.title("🎨 AI ile Kurs Tasarla")
    topic = st.text_input("Öğretmek istediğiniz konu nedir?")
    if st.button("🚀 Müfredat ve İçerik Üret"):
        if topic:
            with st.status("Groq AI içerik hazırlıyor...") as status:
                plan = ai_service.generate_lesson_plan(topic)
                st.session_state.temp_plan = plan
                st.session_state.temp_topic = topic
                status.update(label="İçerik Hazır!", state="complete")
    if getattr(st.session_state, 'temp_plan', None):
        st.markdown(st.session_state.temp_plan)
        if st.button("💾 Kursu Kaydet"):
            db = SessionLocal()
            nc = create_course(db, st.session_state.temp_topic, "Groq AI tarafından oluşturuldu.", 1)
            create_lesson(db, nc.id, "Ders İçeriği", st.session_state.temp_plan)
            db.close()
            st.success("Kurs kaydedildi!")
            st.session_state.temp_plan = None ; st.rerun()

def render_ai_assistant(ai_service):
    st.title("🤖 AI Asistanı")
    q = st.text_area("Sorunuzu buraya yazın...")
    if st.button("Sor"):
        if q:
            with st.spinner("Groq AI Yanıtlıyor..."):
                res = ai_service.generate_content(q)
                st.info(res)

def render_settings():
    st.title("⚙️ Ayarlar")
    st.session_state.groq_key = st.text_input("Groq API Key", value=st.session_state.groq_key, type="password")
    if st.button("Kaydet ve Yenile"): st.rerun()

if __name__ == "__main__": main()
