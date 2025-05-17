import polib
from googletrans import Translator
import time
import os

import re

def translate_with_context(text, translator, dest_lang='ru'):
    # Обновлённый prompt с более понятным форматом
    prompt = f"Medical UI label: {text}"
    result = translator.translate(prompt, dest=dest_lang)
    translated = result.text.strip()

    # Убираем все лишние обёртки (если есть)
    match = re.search(r"[«“\"](.+?)[»”\"]", translated)
    if match:
        return match.group(1)

    # Убираем всё до двоеточия, если перевод вернул фразу вида: "Медицинская метка: Настройки профиля"
    if ":" in translated:
        translated = translated.split(":", 1)[-1]

    return translated.strip(" :«»\"“”")



def translate_po_file(filepath, dest_lang='ru'):
    if not os.path.exists(filepath):
        print(f"❌ Файл не найден: {filepath}")
        return

    print(f"\n📄 Открываю файл: {filepath}")
    po = polib.pofile(filepath)
    translator = Translator()

    translated_count = 0

    for entry in po.untranslated_entries():
        try:
            if entry.msgid.strip():
                translated_text = translate_with_context(entry.msgid, translator, dest_lang)
                entry.msgstr = translated_text
                translated_count += 1

                # 🔍 Выводим результат в консоль
                print("─────────────────────────────────────────────")
                print(f"Original  : {entry.msgid}")
                print(f"Translated: {entry.msgstr}")
                print("─────────────────────────────────────────────")

                time.sleep(0.5)  # пауза для API
        except Exception as e:
            print(f"⚠️ Ошибка при переводе '{entry.msgid}': {e}")

    if translated_count > 0:
        po.save(filepath)
        print(f"\n✅ Переведено {translated_count} строк. Сохранено в: {filepath}")
    else:
        print("\nℹ️ Все строки уже переведены.")


if __name__ == "__main__":
    file_path = r"C:\Users\User\Desktop\bolnichka\HealthStack-System\locale\ru\LC_MESSAGES\django.po"
    translate_po_file(file_path)
