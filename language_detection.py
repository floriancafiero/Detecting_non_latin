import os
import pycld3

# Fonction pour détecter les langues dans un texte
def detect_languages_pycld3(text):
    try:
        # Utilise pycld3 pour détecter les langues
        detected_langs = pycld3.get_frequent_languages(text, num_langs=3)
        results = [f"{lang.language}: {round(lang.probability * 100, 2)}%" for lang in detected_langs]
        return ", ".join(results)
    except Exception as e:
        return f"Erreur de détection : {e}"

# Fonction pour analyser un corpus de textes
def analyze_corpus_with_languages(corpus_folder):
    results = {}

    # Parcours des fichiers dans le dossier
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                detected_langs = detect_languages_pycld3(text)
                results[filename] = detected_langs

    return results

# Chemin vers le dossier contenant les textes
corpus_folder = "/content/"  # À adapter selon votre environnement

# Analyse des fichiers
results = analyze_corpus_with_languages(corpus_folder)

# Affichage des résultats
print("Détection des langues dans chaque fichier :\n")
for filename, langs in results.items():
    print(f"{filename} : {langs}")
