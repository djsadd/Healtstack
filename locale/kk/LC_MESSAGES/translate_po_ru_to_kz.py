import polib
from googletrans import Translator
import os
import re

def clean_text(text):
    # Убираем кавычки, двоеточия и лишние символы
    return text.strip().strip("«»\"“”:")

def translate_text(text, translator, src='ru', dest='kk'):
    if not text.strip():
        return ''
    result = translator.translate(text, src=src, dest=dest)
    translated = result.text.strip()
    # Извлекаем чистый перевод, если есть лишнее
    match = re.search(r"[«“\"]?(.+?)[»”\"]?$", translated)
    return clean_text(match.group(1)) if match else clean_text(translated)

def translate_po_file(filepath):
    print(f"📄 Открываю файл: {filepath}")
    po = polib.pofile(filepath)
    translator = Translator()

    for entry in po.translated_entries():
        # Только те строки, которые уже на русском
        if entry.msgstr and not entry.msgstr.strip().startswith('['):
            original_ru = entry.msgstr
            translated_kz = translate_text(original_ru, translator)
            print(f"🔁 RU: {original_ru} → KZ: {translated_kz}")
            entry.msgstr = translated_kz

    # Сохраняем в отдельный файл
    base, ext = os.path.splitext(filepath)
    new_filepath = f"{base}_kk{ext}"
    po.save(new_filepath)
    print(f"\n✅ Сохранено: {new_filepath}")

if __name__ == "__main__":
    path = r"C:\Users\User\Desktop\bolnichka\HealthStack-System\locale\kk\LC_MESSAGES\django.po"
    if os.path.exists(path):
        translate_po_file(path)
    else:
        print("❌ Файл не найден.")
