import os

def ensure_i18n_tag(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    already_loaded = any("{% load i18n %}" in line for line in lines[:10])

    if already_loaded:
        print(f"⏩ Уже есть: {file_path}")
        return False

    # Вставляем {% load i18n %} после возможного DOCTYPE или первой строки
    insert_index = 0
    if lines and lines[0].strip().lower().startswith("<!doctype"):
        insert_index = 1

    lines.insert(insert_index, "{% load i18n %}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ Добавлен {{% load i18n %}}: {file_path}")
    return True

def process_templates_for_i18n(directory, extensions=('.html', '.htm')):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                full_path = os.path.join(root, file)
                try:
                    ensure_i18n_tag(full_path)
                except Exception as e:
                    print(f"❌ Ошибка при обработке {full_path}: {e}")

# ==== Запуск ====
directory = r"C:\Users\admin\Desktop\Projects\bolnichka\HealthStack-System\templates"
process_templates_for_i18n(directory)
print("\n🎉 Готово: проверка и вставка {% load i18n %} завершена.")
