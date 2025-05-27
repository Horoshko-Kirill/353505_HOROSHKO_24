import re
import zipfile
import os

class Regular:

    @staticmethod
    def print_inf(fileinput, fileoutput):
        with open(fileinput, 'r', encoding = "utf-8") as file:
            text = file.read()

        text = re.sub(r'\s+', ' ', text.strip())

        sentences = re.findall(r'[.!?]', text)
        sentence_count = len(sentences)

        n_declarative = len(re.findall(r'[А-ЯA-Z][^.!?]*[.]', text))  # повествовательные (.)
        n_interrogative = len(re.findall(r'[А-ЯA-Z][^.!?]*[?]', text))  # вопросительные (?)
        n_imperative = len(re.findall(r'[А-ЯA-Z][^.!?]*[!]', text))

        sentences = re.split(r'[.!?]+', text)
        num_sentences = len(sentences)
        total_sentences_length = 0

        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence)
            total_sentences_length += sum(len(word) for word in words)



        avg_sentence_length = total_sentences_length / num_sentences

        all_words = re.findall(r'\b\w+\b', text)
        avg_word_length = sum(len(word) for word in all_words) / len(all_words) if all_words else 0

        emoji_pattern = r'(?:[:;])-*\[{1,}|\]{1,}|\({1,}|\){1,}'
        emojis = re.findall(emoji_pattern, text)
        emoji_count = len(emojis)

        lowercase_words = re.findall(r'\b[a-zа-яё]\w*', text)

        punctuation_marks = re.findall(r'[.,!?;:\-()\[\]…]', text)

        consonant_word_pattern = r'\b[БВГДЖЭЙКЛМНПРСТФХЦЧШЩбвгджзйклмнпрстфхцчшщBCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz]\w*\b'
        consonant_words = re.findall(consonant_word_pattern, text, re.IGNORECASE)
        consonant_word_count = len(consonant_words)

        words_with_double_letters = []
        for i, word in enumerate(all_words):
            if re.search(r'(.)\1', word, re.IGNORECASE):  # ищет повторяющуюся букву
                words_with_double_letters.append((i + 1, word))  # индекс с 1

        sorted_words = sorted(set(word.lower() for word in all_words))

        result = (
            f"Общее количество предложений: {sentence_count}\n"
            f"Повествовательные предложения: {n_declarative}\n"
            f"Вопросительные предложения: {n_interrogative}\n"
            f"Побудительные предложения: {n_imperative}\n"
            f"Средняя длина предложения (в символах): {avg_sentence_length:.2f}\n"
            f"Средняя длина слова: {avg_word_length:.2f}\n"
            f"Количество смайликов: {emoji_count}\n"
            f"Слова, начинающиеся со строчной буквы:\n{', '.join(lowercase_words)}\n"
            f"Знаки препинания:\n{', '.join(punctuation_marks)}\n"
            f"Количество слов, начинающихся с согласной: {consonant_word_count}\n"
            f"Слова с двойными буквами подряд и их номера:\n" +
            "\n".join([f"{idx}: {word}" for idx, word in words_with_double_letters]) + "\n"
            f"Слова в алфавитном порядке:\n{', '.join(sorted_words)}\n"
        )

        print(result)

        with open(fileoutput, "w", encoding="utf-8") as f_out:
            f_out.write(result)

        zip_filename = "result_archive.zip"
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(fileoutput, arcname=os.path.basename(fileoutput))

        info = archive.getinfo(os.path.basename(fileoutput))
        print(f"Файл '{info.filename}' добавлен в архив '{zip_filename}'")
        print(f"  - Размер оригинала: {info.file_size} байт")
        print(f"  - Размер в архиве: {info.compress_size} байт")

    @staticmethod
    def isMAC(string):
        pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
        return bool(re.fullmatch(pattern, string))

