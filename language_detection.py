import os
import fasttext

# Chargement du modèle
model = fasttext.load_model("lid.176.bin")

# Fonction pour détecter les langues
def detect_language_fasttext(text):
    predictions = model.predict(text.replace('\n', ' '), k=2)  # Top 2 langues # Replacing newline characters with spaces
    langs = [f"{lang.replace('__label__', '')}: {round(prob * 100, 2)}%" 
             for lang, prob in zip(predictions[0], predictions[1])]
    return ", ".join(langs)

# Fonction pour analyser un corpus de textes
def analyze_corpus_with_fasttext(corpus_folder):
    results = {}
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                # Process the file line by line
                for line in file:
                    text = line.strip()  # Remove leading/trailing whitespace
                    if text:  # Skip empty lines
                        detected_lang = detect_language_fasttext(text)
                        results.setdefault(filename, []).append(detected_lang) # Append detected language to list associated with filename
                
    # If you want a single language for each file, you can choose the most frequent
    # Or you can keep the list of languages detected in each line
    return results # or {filename: max(set(langs), key=langs.count) for filename, langs in results.items()}


# Chemin vers le dossier contenant les textes
corpus_folder = "/content/"  # À adapter

# Analyse des fichiers
results = analyze_corpus_with_fasttext(corpus_folder)


from collections import defaultdict

# Fonction pour calculer les proportions globales des langues
def calculate_language_proportions(results):
    aggregated_results = {}

    for filename, lang_lines in results.items():
        lang_counts = defaultdict(float)

        # Parcours de chaque ligne détectée
        for line in lang_lines:
            # Extraction des prédictions (langue: probabilité)
            predictions = [lang_prob.split(": ") for lang_prob in line.split(", ")]
            for lang, prob in predictions:
                lang_counts[lang] += float(prob.strip('%'))  # Addition des probabilités

        # Normalisation pour obtenir un total de 100 %
        total = sum(lang_counts.values())
        proportions = {lang: round((count / total) * 100, 2) for lang, count in lang_counts.items()}
        
        aggregated_results[filename] = proportions

    return aggregated_results

# Exemple d'utilisation avec vos résultats
aggregated_results = calculate_language_proportions(results)

# Affichage des résultats
for filename, langs in aggregated_results.items():
    print(f"\n{filename} :")
    for lang, proportion in sorted(langs.items(), key=lambda x: x[1], reverse=True):
        print(f"{lang} : {proportion}%")
