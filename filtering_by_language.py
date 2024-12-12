def filter_passages_by_language(results, target_languages, corpus_folder, threshold=70, min_length=10):
    filtered_passages = {}

    for filename, lang_lines in results.items():
        file_path = os.path.join(corpus_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            passages = []
            for idx, line in enumerate(file, start=1):
                text = line.strip()
                if len(text) >= min_length:
                    detected_lang = detect_language_fasttext(text)
                    langs = [lang_prob.split(": ") for lang_prob in detected_lang.split(", ")]

                    # Vérifie si une langue cible est présente avec un seuil
                    for lang, prob in langs:
                        if lang in target_languages and float(prob.strip('%')) >= threshold:
                            passages.append((idx, text))
                            break

            if passages:
                filtered_passages[filename] = passages

    return filtered_passages

# Exemple d'utilisation
target_languages = ["fr"]  # Langue cible : anglais
threshold = 40  # Seuil de confiance
min_length = 5  # Longueur minimale des passages

filtered_by_languages = filter_passages_by_language(results, target_languages, corpus_folder, threshold, min_length)

# Affichage des résultats
print("\nPassages filtrés par langues spécifiques :")
for filename, passages in filtered_by_languages.items():
    print(f"\nFichier : {filename}")
    for line_num, passage in passages:
        print(f"Ligne {line_num} : {passage}")
