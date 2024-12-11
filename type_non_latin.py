import os
import re
import unicodedata

# Définition des ensembles de caractères pour chaque système d'écriture
CHARACTER_SETS = {
    "japonais": r'[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]',  # Hiragana, Katakana, Kana étendu
    "kanji": r'[\u4E00-\u9FFF]',  # Kanji (partagé avec le chinois)
    "coréen": r'[\uAC00-\uD7AF\u1100-\u11FF]',  # Hangul
    "russe": r'[\u0400-\u04FF]',  # Alphabet cyrillique
    "arabe": r'[\u0600-\u06FF\u0750-\u077F]',  # Arabe
    "hébreu": r'[\u0590-\u05FF]',  # Hébreu
    "grec": r'[\u0370-\u03FF]',  # Alphabet grec
    "latin étendu": r'[\u0100-\u024F]',  # Caractères latins avec accents
    "autre": r'[^\u0000-\u007F]',  # Tout caractère non ASCII
}

# Fonction pour classifier et calculer les proportions des types de caractères
def classify_text_with_proportions(text):
    normalized_text = unicodedata.normalize('NFC', text)
    total_characters = len(normalized_text)
    char_counts = {charset: 0 for charset in CHARACTER_SETS}

    # Compter les caractères pour chaque ensemble
    for charset, regex in CHARACTER_SETS.items():
        char_counts[charset] += len(re.findall(regex, normalized_text))

    # Traitement spécifique pour japonais et chinois
    is_japanese = char_counts["japonais"] > 0
    has_kanji = char_counts["kanji"] > 0

    if is_japanese:  # Si hiragana/katakana présents, les kanji sont japonais
        char_counts["japonais"] += char_counts["kanji"]
        char_counts["kanji"] = 0
    elif has_kanji:  # Si kanji seuls... c'est du chinois pour moi
        char_counts["chinois"] = char_counts["kanji"]
        char_counts["kanji"] = 0

    # Calculer les proportions en pourcentage
    proportions = {}
    for charset, count in char_counts.items():
        if count > 0:
            proportions[charset] = round((count / total_characters) * 100, 2)

    return proportions

# Fonction pour analyser un corpus de textes
def find_texts_with_non_latin_characters(corpus_folder):
    results = {}

    # Parcours des fichiers dans le dossier
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                proportions = classify_text_with_proportions(text)
                if proportions:  # Ajouter les fichiers non vides
                    results[filename] = proportions

    return results

# Chemin vers le dossier contenant les textes
corpus_folder = "/content/"  # À adapter selon votre environnement

# Analyse des fichiers
results = find_texts_with_non_latin_characters(corpus_folder)

# Affichage des résultats
print("Classification des fichiers avec proportions des types de caractères :\n")
for filename, proportions in results.items():
    detected = ", ".join(f"{charset}: {percent}%" for charset, percent in proportions.items())
    print(f"{filename} : {detected}")
