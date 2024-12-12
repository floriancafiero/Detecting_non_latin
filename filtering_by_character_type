def filter_passages_by_character_types(corpus_folder, character_types, min_length=10):
    filtered_passages = {}

    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                passages = []
                for idx, line in enumerate(file, start=1):
                    text = line.strip()
                    if len(text) >= min_length:  # Longueur minimale
                        # Vérification des types de caractères
                        for char_type in character_types:
                            if re.search(CHARACTER_SETS[char_type], text):
                                passages.append((idx, text))
                                break  # Évite d'ajouter plusieurs fois la même ligne

            if passages:
                filtered_passages[filename] = passages

    return filtered_passages

# Exemple d'utilisation
character_types = ["japonais", "arabe"]  # Types de caractères à filtrer
min_length = 10  # Longueur minimale des passages

filtered_by_characters = filter_passages_by_character_types(corpus_folder, character_types, min_length)

# Affichage des résultats
print("\nPassages filtrés par types de caractères :")
for filename, passages in filtered_by_characters.items():
    print(f"\nFichier : {filename}")
    for line_num, passage in passages:
        print(f"Ligne {line_num} : {passage}")
