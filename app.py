import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="MAHAMI - مهامي", layout="centered")

FILE = "mahami_memory_v2.json"

def load_tasks():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_tasks(tasks):
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("Memory error:", e)
        return False

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

for task in st.session_state.tasks:
    task.setdefault("priority", "عادية")
    task.setdefault("category", "عام")
    task.setdefault("done", False)
    task.setdefault("date", "")

LANG = {
    "العربية 🇲🇦": {
        "title": "MAHAMI",
        "arabic_title": "مهامي",
        "subtitle": "Smart Task Manager",
        "new": "المهمة الجديدة",
        "placeholder": "اكتب مهمتك هنا...",
        "add": "➕ إضافة مهمة",
        "delete": "🗑️ حذف",
        "search": "🔎 بحث",
        "search_placeholder": "ابحث عن مهمة...",
        "priority": "⭐ الأولوية",
        "category": "🏷️ الفئة",
        "tasks": "📋 المهام",
        "total": "إجمالي",
        "done": "مكتملة",
        "pending": "متبقية",
        "empty": "لا توجد مهام حاليا",
        "priorities": ["عادية", "مهمة", "مستعجلة"],
        "categories": ["عام", "عمل", "شخصية", "دراسة", "أخرى"]
    },
    "Français 🇫🇷": {
        "title": "MAHAMI",
        "arabic_title": "Gestionnaire de tâches",
        "subtitle": "Smart Task Manager",
        "new": "Nouvelle tâche",
        "placeholder": "Écrivez votre tâche ici...",
        "add": "➕ Ajouter",
        "delete": "🗑️ Supprimer",
        "search": "🔎 Recherche",
        "search_placeholder": "Rechercher une tâche...",
        "priority": "⭐ Priorité",
        "category": "🏷️ Catégorie",
        "tasks": "📋 Tâches",
        "total": "Total",
        "done": "Terminées",
        "pending": "Restantes",
        "empty": "Aucune tâche",
        "priorities": ["Normale", "Importante", "Urgente"],
        "categories": ["Général", "Travail", "Personnel", "Études", "Autre"]
    },
    "English 🇬🇧": {
        "title": "MAHAMI",
        "arabic_title": "Task Manager",
        "subtitle": "Smart Task Manager",
        "new": "New task",
        "placeholder": "Write your task here...",
        "add": "➕ Add task",
        "delete": "🗑️ Delete",
        "search": "🔎 Search",
        "search_placeholder": "Search tasks...",
        "priority": "⭐ Priority",
        "category": "🏷️ Category",
        "tasks": "📋 Tasks",
        "total": "Total",
        "done": "Completed",
        "pending": "Remaining",
        "empty": "No tasks",
        "priorities": ["Normal", "Important", "Urgent"],
        "categories": ["General", "Work", "Personal", "Study", "Other"]
    }
}

# اختيار اللغة من الشريط الجانبي أو الأعلى
lang_choice = st.sidebar.selectbox("🌍 Language / اللغة", list(LANG.keys()))
L = LANG[lang_choice]

# تصميم الهيدر العصري المطابق لتصميمك الأصلي
st.markdown("""
<style>
.header {
  background: linear-gradient(135deg, #111827, #1e3a8a);
  padding: 24px 15px; border-radius: 18px; text-align: center; margin-bottom: 20px; color: white;
}
.logo-text { font-size: 38px; font-weight: 900; letter-spacing: 4px; margin: 0; }
.arabic-sub { font-size: 22px; font-weight: bold; margin-top: 5px; }
.subtitle { color: #cbd5e1; font-size: 13px; margin-top: 3px; }
</style>
<div class="header">
  <div class="logo-text">MAHAMI</div>
  <div class="arabic-sub">مهامي</div>
  <div class="subtitle">Smart Task Manager</div>
</div>
""", unsafe_allow_html=True)

# الإحصائيات
total = len(st.session_state.tasks)
done_count = sum(1 for t in st.session_state.tasks if t.get("done", False))
pending_count = total - done_count

col1, col2, col3 = st.columns(3)
col1.metric(L["total"], total)
col2.metric(L["done"], done_count)
col3.metric(L["pending"], pending_count)

st.markdown("---")

# نموذج إضافة مهمة جديدة
with st.form("add_form", clear_on_submit=True):
    new_text = st.text_input(L["new"], placeholder=L["placeholder"])
    col_p, col_c = st.columns(2)
    with col_p:
        priority_val = st.selectbox(L["priority"], L["priorities"])
    with col_c:
        category_val = st.selectbox(L["category"], L["categories"])
    
    submitted = st.form_submit_button(L["add"])
    if submitted and new_text.strip():
        st.session_state.tasks.append({
            "text": new_text.strip(),
            "done": False,
            "priority": priority_val,
            "category": category_val,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_tasks(st.session_state.tasks)
        st.rerun()

# شريط البحث
search_query = st.text_input(L["search"], placeholder=L["search_placeholder"]).strip().lower()

st.subheader(L["tasks"])

# عرض المهام
if not st.session_state.tasks:
    st.info(L["empty"])
else:
    for i, task in enumerate(st.session_state.tasks):
        if search_query and search_query not in task["text"].lower():
            continue
        
        col_check, col_content, col_del = st.columns([0.1, 0.75, 0.15])
        
        with col_check:
            is_done = st.checkbox("", value=task.get("done", False), key=f"done_{i}")
            if is_done != task.get("done", False):
                st.session_state.tasks[i]["done"] = is_done
                save_tasks(st.session_state.tasks)
                st.rerun()
        
        with col_content:
            if task.get("done", False):
                st.markdown(f"~~{task['text']}~~")
            else:
                st.markdown(f"**{task['text']}**")
            st.caption(f"⭐ {task.get('priority')} | 🏷️ {task.get('category')} | 📅 {task.get('date')}")
            
        with col_del:
            if st.button(L["delete"], key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks(st.session_state.tasks)
                st.rerun()
        
        st.markdown("---")
