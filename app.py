import streamlit as st
import json
import os
from datetime import datetime

# ============================================================
# MAHAMI — Streamlit App
# ============================================================

st.set_page_config(page_title="MAHAMI", page_icon="📋", layout="centered")

FILE = "mahami_memory_v2.json"

# ---------------- MEMORY ----------------
def load_tasks():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

tasks = st.session_state.tasks

for task in tasks:
    task.setdefault("priority", "عادية")
    task.setdefault("category", "عام")
    task.setdefault("done", False)
    task.setdefault("date", "")

def save():
    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("Memory error:", e)
        return False

# ---------------- LANGUAGES ----------------
LANG = {
    "العربية 🇲🇦": {
        "new": "المهمة الجديدة",
        "placeholder": "اكتب مهمتك هنا...",
        "add": "➕ إضافة مهمة",
        "number": "رقم المهمة",
        "complete": "✅ إكمال المهمة",
        "delete": "🗑️ حذف المهمة",
        "edit": "✏️ تعديل المهمة",
        "edit_text": "✏️ النص الجديد",
        "search": "🔎 بحث",
        "search_placeholder": "ابحث عن مهمة...",
        "priority": "⭐ الأولوية",
        "category": "🏷️ الفئة",
        "tasks": "📋 المهام",
        "total": "إجمالي",
        "done": "مكتملة",
        "pending": "متبقية",
        "empty": "لا توجد مهام حاليا",
        "completed": "✅ تم إكمال المهمة",
        "deleted": "🗑️ تم حذف المهمة",
        "edited": "✏️ تم تعديل المهمة",
        "invalid": "⚠️ رقم المهمة غير صحيح",
        "language": "🌍 اللغة",
    },
    "Français 🇫🇷": {
        "new": "Nouvelle tâche",
        "placeholder": "Écrivez votre tâche ici...",
        "add": "➕ Ajouter",
        "number": "Numéro de tâche",
        "complete": "✅ Terminer",
        "delete": "🗑️ Supprimer",
        "edit": "✏️ Modifier",
        "edit_text": "✏️ Nouveau texte",
        "search": "🔎 Recherche",
        "search_placeholder": "Rechercher une tâche...",
        "priority": "⭐ Priorité",
        "category": "🏷️ Catégorie",
        "tasks": "📋 Tâches",
        "total": "Total",
        "done": "Terminées",
        "pending": "Restantes",
        "empty": "Aucune tâche",
        "completed": "✅ Tâche terminée",
        "deleted": "🗑️ Tâche supprimée",
        "edited": "✏️ Tâche modifiée",
        "invalid": "⚠️ Numéro incorrect",
        "language": "🌍 Langue",
    },
    "English 🇬🇧": {
        "new": "New task",
        "placeholder": "Write your task here...",
        "add": "➕ Add task",
        "number": "Task number",
        "complete": "✅ Complete",
        "delete": "🗑️ Delete",
        "edit": "✏️ Edit",
        "edit_text": "✏️ New text",
        "search": "🔎 Search",
        "search_placeholder": "Search tasks...",
        "priority": "⭐ Priority",
        "category": "🏷️ Category",
        "tasks": "📋 Tasks",
        "total": "Total",
        "done": "Completed",
        "pending": "Remaining",
        "empty": "No tasks",
        "completed": "✅ Task completed",
        "deleted": "🗑️ Task deleted",
        "edited": "✏️ Task edited",
        "invalid": "⚠️ Invalid task number",
        "language": "🌍 Language",
    }
}

def priority_choices(lang):
    if lang == "العربية 🇲🇦":
        return ["عادية", "مهمة", "مستعجلة"]
    if lang == "Français 🇫🇷":
        return ["Normale", "Importante", "Urgente"]
    return ["Normal", "Important", "Urgent"]

def category_choices(lang):
    if lang == "العربية 🇲🇦":
        return ["عام", "عمل", "شخصية", "دراسة", "أخرى"]
    if lang == "Français 🇫🇷":
        return ["Général", "Travail", "Personnel", "Études", "Autre"]
    return ["General", "Work", "Personal", "Study", "Other"]

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>
body { background:#f1f5f9; }
.header {
  background:linear-gradient(135deg,#111827,#1e3a8a);
  padding:28px 15px; border-radius:22px; text-align:center; margin-bottom:20px;
}
.logo { display:flex; justify-content:center; align-items:center; gap:12px; }
.logo-text { font-family:Arial,sans-serif; font-size:44px; font-weight:900; letter-spacing:6px; color:white; }
.symbol { width:28px; height:28px; position:relative; transform:rotate(45deg); display:inline-block; }
.square { position:absolute; width:12px; height:12px; border-radius:3px; }
.s1 { background:#38bdf8; top:0; left:8px; }
.s2 { background:#818cf8; bottom:0; left:0; }
.s3 { background:#22d3ee; bottom:0; right:0; }
.arabic { color:white; font-size:28px; font-weight:bold; margin-top:10px; }
.subtitle { color:#cbd5e1; font-size:14px; margin-top:5px; }
.stats { display:flex; gap:12px; margin:15px 0; }
.stat { flex:1; background:white; padding:18px 10px; border-radius:16px; text-align:center; border: 1px solid #e2e8f0; }
.stat b { display:block; font-size:28px; color:#1e3a8a; }
.stat span { font-size:13px; color:#64748b; }
.task { display:flex; align-items:flex-start; gap:15px; background:white; padding:15px; border-radius:15px; margin:10px 0; border: 1px solid #e2e8f0; }
.number { width:36px; height:36px; min-width:36px; background:#1e3a8a; color:white; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; }
.task-content { flex:1; }
.taskname { font-size:17px; font-weight:600; color:#0f172a; }
.badges { display:flex; gap:7px; flex-wrap:wrap; margin-top:8px; }
.badge { background:#eef2ff; color:#1e3a8a; padding:5px 9px; border-radius:8px; font-size:12px; }
.date { color:#64748b; font-size:12px; margin-top:7px; }
.empty { background:white; padding:35px; border-radius:16px; text-align:center; color:#64748b; border: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER UI ----------------
st.markdown("""
<div class="header">
  <div class="logo">
    <div class="logo-text">MAHAMI</div>
    <div class="symbol">
      <div class="square s1"></div>
      <div class="square s2"></div>
      <div class="square s3"></div>
    </div>
  </div>
  <div class="arabic">مهامي</div>
  <div class="subtitle">Smart Task Manager</div>
</div>
""", unsafe_allow_html=True)

# ---------------- LANGUAGE SELECTOR ----------------
selected_lang = st.selectbox("🌍 اللغة / Language", list(LANG.keys()), index=0)
L = LANG[selected_lang]

# ---------------- STATS ----------------
total = len(tasks)
done_count = sum(1 for t in tasks if t.get("done", False))
pending_count = total - done_count

st.markdown(f"""
<div class="stats">
  <div class="stat"><b>{total}</b><span>{L["total"]}</span></div>
  <div class="stat"><b>{done_count}</b><span>{L["done"]}</span></div>
  <div class="stat"><b>{pending_count}</b><span>{L["pending"]}</span></div>
</div>
""", unsafe_allow_html=True)

# ---------------- ADD TASK ----------------
with st.form("add_form", clear_on_submit=True):
    new_task_text = st.text_input(L["new"], placeholder=L["placeholder"])
    col_p, col_c = st.columns(2)
    with col_p:
        p_choice = st.selectbox(L["priority"], priority_choices(selected_lang))
    with col_c:
        c_choice = st.selectbox(L["category"], category_choices(selected_lang))
    
    submitted = st.form_submit_button(L["add"])
    if submitted and new_task_text.strip():
        tasks.append({
            "text": new_task_text.strip(),
            "done": False,
            "priority": p_choice,
            "category": c_choice,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save()
        st.rerun()

# ---------------- SEARCH & ACTIONS ----------------
search_query = st.text_input(L["search"], placeholder=L["search_placeholder"])

st.markdown("---")

if tasks:
    task_numbers = [str(i+1) for i in range(len(tasks))]
    selected_num = st.selectbox(L["number"], task_numbers)
    idx = int(selected_num) - 1

    edit_text_input = st.text_input(L["edit_text"], value=tasks[idx]["text"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(L["complete"]):
            tasks[idx]["done"] = True
            save()
            st.success(L["completed"])
            st.rerun()
    with col2:
        if st.button(L["edit"]):
            if edit_text_input.strip():
                tasks[idx]["text"] = edit_text_input.strip()
            save()
            st.success(L["edited"])
            st.rerun()
    with col3:
        if st.button(L["delete"], type="primary"):
            tasks.pop(idx)
            save()
            st.success(L["deleted"])
            st.rerun()

# ---------------- DISPLAY TASKS ----------------
st.markdown(f"## {L['tasks']}")

filtered_tasks = []
for i, task in enumerate(tasks):
    txt = str(task.get("text", ""))
    if search_query.strip() and search_query.strip().lower() not in txt.lower():
        continue
    filtered_tasks.append((i, task))

if not filtered_tasks:
    st.markdown(f'<div class="empty">{L["empty"]}</div>', unsafe_allow_html=True)
else:
    for original_index, task in filtered_tasks:
        done = task.get("done", False)
        icon = "✅" if done else "⬜"
        text = task.get("text", "")
        date = task.get("date", "")
        priority = task.get("priority", "")
        category = task.get("category", "")

        st.markdown(f"""
        <div class="task">
          <div class="number">{original_index + 1}</div>
          <div class="task-content">
            <div class="taskname">{icon} {text}</div>
            <div class="badges">
              <span class="badge">⭐ {priority}</span>
              <span class="badge">🏷️ {category}</span>
            </div>
            <div class="date">📅 {date}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
