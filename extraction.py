# Fonction l'extraction des passages dans une langue
def extract_passages_improved(results, target_language, corpus_folder, threshold=70, min_length=10):
    language_passages = {}

    # Parcours des fichiers et lignes analysés
    for filename, lang_lines in results.items():
        file_path = os.path.join(corpus_folder, filename)
        passages = []

        with open(file_path, 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file, start=1):  # Lecture ligne par ligne avec numéro
                text = line.strip()
                if len(text) >= min_length:  # Ignorer les très courts passages
                    detected_lang = detect_language_fasttext(text)
                    langs = [lang_prob.split(": ") for lang_prob in detected_lang.split(", ")]

                    # Filtrer les langues avec une probabilité supérieure au seuil
                    for lang, prob in langs:
                        if lang == target_language and float(prob.strip('%')) >= threshold:
                            passages.append((idx, text))  # Ajouter la ligne avec son numéro

        if passages:
            language_passages[filename] = passages

    return language_passages

# Exemple d'utilisation
target_language = "de"  # Langue cible (allemand)
threshold = 33  # Probabilité minimale pour considérer la détection
min_length = 6  # Longueur minimale des passages, en caractères

language_passages = extract_passages_improved(results, target_language, corpus_folder, threshold, min_length)

# Affichage des résultats
print(f"\nPassages améliorés détectés en langue '{target_language}' :")
for filename, passages in language_passages.items():
    print(f"\nFichier : {filename}")
    for line_num, passage in passages:
        print(f"Ligne {line_num} : {passage}")
