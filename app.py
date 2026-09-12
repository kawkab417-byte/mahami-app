import gradio as gr
import json
import os
import html
from datetime import datetime

# ============================================================
# MAHAMI — Hugging Face Space
# ============================================================

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

tasks = load_tasks()

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

# ---------------- DISPLAY ----------------
def stats(lang):
    L = LANG[lang]
    total = len(tasks)
    done = sum(1 for t in tasks if t.get("done", False))
    pending = total - done
    return f"""
    <div class="stats">
      <div class="stat"><b>{total}</b><span>{L["total"]}</span></div>
      <div class="stat"><b>{done}</b><span>{L["done"]}</span></div>
      <div class="stat"><b>{pending}</b><span>{L["pending"]}</span></div>
    </div>
    """

def show_tasks(lang, search=""):
    L = LANG[lang]
    search = (search or "").strip().lower()
    visible = []

    for i, task in enumerate(tasks):
        text = str(task.get("text", ""))
        if search and search not in text.lower():
            continue
        visible.append((i, task))

    if not visible:
        return f'<div class="empty">{L["empty"]}</div>'

    output = ""
    for original_index, task in visible:
        done = task.get("done", False)
        icon = "✅" if done else "⬜"
        text = html.escape(str(task.get("text", "")))
        date = html.escape(str(task.get("date", "")))
        priority = html.escape(str(task.get("priority", "")))
        category = html.escape(str(task.get("category", "")))

        output += f"""
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
        """
    return output

# ---------------- TASK ACTIONS ----------------
def add_task(text, priority, category, lang):
    if not text or not text.strip():
        return stats(lang), show_tasks(lang), ""
    tasks.append({
        "text": text.strip(),
        "done": False,
        "priority": priority,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save()
    return stats(lang), show_tasks(lang), ""

def complete_task(number, lang):
    L = LANG[lang]
    try:
        index = int(float(number)) - 1
        if index < 0 or index >= len(tasks):
            raise ValueError
        tasks[index]["done"] = True
        save()
        return stats(lang), show_tasks(lang), L["completed"]
    except Exception:
        return stats(lang), show_tasks(lang), L["invalid"]

def delete_task(number, lang):
    L = LANG[lang]
    try:
        index = int(float(number)) - 1
        if index < 0 or index >= len(tasks):
            raise ValueError
        tasks.pop(index)
        save()
        return stats(lang), show_tasks(lang), L["deleted"]
    except Exception:
        return stats(lang), show_tasks(lang), L["invalid"]

def edit_task(number, new_text, priority, category, lang):
    L = LANG[lang]
    try:
        index = int(float(number)) - 1
        if index < 0 or index >= len(tasks):
            raise ValueError
        if new_text and new_text.strip():
            tasks[index]["text"] = new_text.strip()
        tasks[index]["priority"] = priority
        tasks[index]["category"] = category
        save()
        return stats(lang), show_tasks(lang), L["edited"]
    except Exception:
        return stats(lang), show_tasks(lang), L["invalid"]

def search_tasks(search, lang):
    return show_tasks(lang, search)

# ---------------- LANGUAGE UI UPDATE ----------------
def change_language(lang):
    L = LANG[lang]
    p = priority_choices(lang)
    c = category_choices(lang)

    return (
        gr.update(label=L["new"], placeholder=L["placeholder"]),
        gr.update(value=L["add"]),
        gr.update(choices=p, value=p[0], label=L["priority"]),
        gr.update(choices=c, value=c[0], label=L["category"]),
        gr.update(label=L["number"]),
        gr.update(value=L["complete"]),
        gr.update(value=L["delete"]),
        gr.update(value=L["edit"]),
        gr.update(label=L["search"], placeholder=L["search_placeholder"]),
        stats(lang),
        show_tasks(lang),
        gr.update(value="## " + L["tasks"]),
        gr.update(label=L["edit_text"]),
        gr.update(label=L["language"]),
    )

# ---------------- CSS ----------------
css = """
body { background:#f1f5f9; }
.gradio-container { max-width:900px !important; margin:auto !important; }
.header {
  background:linear-gradient(135deg,#111827,#1e3a8a);
  padding:28px 15px; border-radius:22px; text-align:center; margin-bottom:20px;
}
.logo { display:flex; justify-content:center; align-items:center; gap:12px; }
.logo-text { font-family:Arial,sans-serif; font-size:44px; font-weight:900; letter-spacing:6px; color:white; }
.symbol { width:28px; height:28px; position:relative; transform:rotate(45deg); }
.square { position:absolute; width:12px; height:12px; border-radius:3px; }
.s1 { background:#38bdf8; top:0; left:8px; }
.s2 { background:#818cf8; bottom:0; left:0; }
.s3 { background:#22d3ee; bottom:0; right:0; }
.arabic { color:white; font-size:28px; font-weight:bold; margin-top:10px; }
.subtitle { color:#cbd5e1; font-size:14px; margin-top:5px; }
.stats { display:flex; gap:12px; margin:15px 0; }
.stat { flex:1; background:white; padding:18px 10px; border-radius:16px; text-align:center; }
.stat b { display:block; font-size:28px; color:#1e3a8a; }
.stat span { font-size:13px; }
.task { display:flex; align-items:flex-start; gap:15px; background:white; padding:15px; border-radius:15px; margin:10px 0; }
.number { width:36px; height:36px; min-width:36px; background:#1e3a8a; color:white; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; }
.task-content { flex:1; }
.taskname { font-size:17px; font-weight:600; }
.badges { display:flex; gap:7px; flex-wrap:wrap; margin-top:8px; }
.badge { background:#eef2ff; padding:5px 9px; border-radius:8px; font-size:12px; }
.date { color:#64748b; font-size:12px; margin-top:7px; }
.empty { background:white; padding:35px; border-radius:16px; text-align:center; color:#64748b; }
@media (max-width:600px) {
  .logo-text { font-size:32px; letter-spacing:4px; }
  .arabic { font-size:23px; }
  .stats { gap:6px; }
  .stat { padding:13px 5px; }
  .stat b { font-size:23px; }
  .task { padding:12px; }
}
"""

# ---------------- APP ----------------
with gr.Blocks(title="MAHAMI", css=css) as app:
    gr.HTML("""
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
    """)

    language = gr.Dropdown(
        choices=list(LANG.keys()), value="العربية 🇲🇦", label="🌍 اللغة"
    )
    stats_box = gr.HTML(stats("العربية 🇲🇦"))

    task_input = gr.Textbox(
        label="المهمة الجديدة", placeholder="اكتب مهمتك هنا..."
    )
    priority = gr.Dropdown(
        choices=priority_choices("العربية 🇲🇦"),
        value="عادية", label="⭐ الأولوية"
    )
    category = gr.Dropdown(
        choices=category_choices("العربية 🇲🇦"),
        value="عام", label="🏷️ الفئة"
    )
    add_button = gr.Button("➕ إضافة مهمة", variant="primary")

    search_box = gr.Textbox(label="🔎 بحث", placeholder="ابحث عن مهمة...")
    number_input = gr.Number(label="رقم المهمة", precision=0)
    edit_text = gr.Textbox(label="✏️ النص الجديد", placeholder="اكتب النص الجديد...")
    edit_button = gr.Button("✏️ تعديل المهمة")
    complete_button = gr.Button("✅ إكمال المهمة")
    delete_button = gr.Button("🗑️ حذف المهمة", variant="stop")

    message = gr.Markdown("")
    tasks_title = gr.Markdown("## 📋 المهام")
    tasks_box = gr.HTML(show_tasks("العربية 🇲🇦"))

    language.change(
        change_language,
        inputs=language,
        outputs=[
            task_input, add_button, priority, category, number_input,
            complete_button, delete_button, edit_button, search_box,
            stats_box, tasks_box, tasks_title, edit_text, language
        ]
    )

    add_button.click(
        add_task,
        inputs=[task_input, priority, category, language],
        outputs=[stats_box, tasks_box, task_input]
    )

    complete_button.click(
        complete_task,
        inputs=[number_input, language],
        outputs=[stats_box, tasks_box, message]
    )

    delete_button.click(
        delete_task,
        inputs=[number_input, language],
        outputs=[stats_box, tasks_box, message]
    )

    edit_button.click(
        edit_task,
        inputs=[number_input, edit_text, priority, category, language],
        outputs=[stats_box, tasks_box, message]
    )

    search_box.change(
        search_tasks,
        inputs=[search_box, language],
        outputs=[tasks_box]
    )

print("========================================")
print("MAHAMI READY")
print("Arabic / Français / English")
print("Persistent task storage: ON")
print("Search / Priority / Categories / Edit / Date: ON")
print("========================================")

# Hugging Face Spaces compatible launch
app.launch()
