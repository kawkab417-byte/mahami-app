
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="MAHAMI", layout="centered")

FILE = "mahami_memory_v2.json"

# Memory functions
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

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

for task in st.session_state.tasks:
    task.setdefault("priority", "عادية")
    task.setdefault("category", "عام")
    task.setdefault("done", False)
    task.setdefault("date", "")

# Language dictionary
LANG = {
    "العربية 🇲🇦": {
        "title": "تطبيق مهامي - MAHAMI",
        "subtitle": "Smart Task Manager",
        "new": "المهمة الجديدة",
        "placeholder": "اكتب مهمتك هنا...",
        "add": "➕ إضافة مهمة",
        "complete": "إكمال",
        "delete": "حذف",
        "search": "🔎 بحث",
        "search_placeholder": "ابحث عن مهمة...",
        "priority": "⭐ الأولوية",
        "category": "🏷️ الفئة",
        "total": "إجمالي",
        "done": "مكتملة",
        "pending": "متبقية",
        "empty": "لا توجد مهام حاليا",
        "priorities": ["عادية", "مهمة", "مستعجلة"],
        "categories": ["عام", "عمل", "شخصية", "دراسة", "أخرى"]
    },
    "Français 🇫🇷": {
        "title": "Gestionnaire de tâches - MAHAMI",
        "subtitle": "Smart Task Manager",
        "new": "Nouvelle tâche",
        "placeholder": "Écrivez votre tâche ici...",
        "add": "➕ Ajouter",
        "complete": "Terminer",
        "delete": "Supprimer",
        "search": "🔎 Recherche",
        "search_placeholder": "Rechercher une tâche...",
        "priority": "⭐ Priorité",
        "category": "🏷️ Catégorie",
        "total": "Total",
        "done": "Terminées",
        "pending": "Restantes",
        "empty": "Aucune tâche",
        "priorities": ["Normale", "Importante", "Urgente"],
        "categories": ["Général", "Travail", "Personnel", "Études", "Autre"]
    },
    "English 🇬🇧": {
        "title": "MAHAMI Task Manager",
        "subtitle": "Smart Task Manager",
        "new": "New task",
        "placeholder": "Write your task here...",
        "add": "➕ Add task",
        "complete": "Complete",
        "delete": "Delete",
        "search": "🔎 Search",
        "search_placeholder": "Search tasks...",
        "priority": "⭐ Priority",
        "category": "🏷️ Category",
        "total": "Total",
        "done": "Completed",
        "pending": "Remaining",
        "empty": "No tasks",
        "priorities": ["Normal", "Important", "Urgent"],
        "categories": ["General", "Work", "Personal", "Study", "Other"]
    }
}

# Sidebar Language Selection
lang_choice = st.sidebar.selectbox("🌍 Language / اللغة", list(LANG.keys()))
L = LANG[lang_choice]

st.title(L["title"])
st.markdown(f"*{L['subtitle']}*")

# Stats
total = len(st.session_state.tasks)
done_count = sum(1 for t in st.session_state.tasks if t.get("done", False))
pending_count = total - done_count

col1, col2, col3 = st.columns(3)
col1.metric(L["total"], total)
col2.metric(L["done"], done_count)
col3.metric(L["pending"], pending_count)

st.markdown("---")

# Add Task Form
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

# Search Box
search_query = st.text_input(L["search"], placeholder=L["search_placeholder"]).strip().lower()

st.subheader("📋")

# Display Tasks
if not st.session_state.tasks:
    st.info(L["empty"])
else:
    for i, task in enumerate(st.session_state.tasks):
        if search_query and search_query not in task["text"].lower():
            continue
        
        col_check, col_text, col_actions = st.columns([0.1, 0.6, 0.3])
        
        with col_check:
            is_done = st.checkbox("", value=task.get("done", False), key=f"done_{i}")
            if is_done != task.get("done", False):
                st.session_state.tasks[i]["done"] = is_done
                save_tasks(st.session_state.tasks)
                st.rerun()
        
        with col_text:
            text_style = f"~~{task['text']}~~" if task.get("done", False) else f"**{task['text']}**"
            st.markdown(text_style)
            st.caption(f"⭐ {task.get('priority')} | 🏷️ {task.get('category')} | 📅 {task.get('date')}")
            
        with col_actions:
            if st.button(L["delete"], key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks(st.session_state.tasks)
                st.rerun()
        
        st.markdown("---")
