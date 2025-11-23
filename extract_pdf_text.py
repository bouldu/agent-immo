#!/usr/bin/env python3
"""Script temporaire pour extraire le texte du PDF"""

try:
    from pypdf import PdfReader
except ImportError:
    try:
        import PyPDF2
        PdfReader = PyPDF2.PdfReader
    except ImportError:
        print("Aucune bibliothèque PDF trouvée. Installation de pypdf...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
        from pypdf import PdfReader

pdf_path = r'example_output\Annexe 6 - Etude de marché Inovefa - Ballainvilliers.pdf'

try:
    reader = PdfReader(pdf_path)

    # Extraire page par page pour mieux identifier la section
    print(f"Nombre total de pages: {len(reader.pages)}\n")

    # La section 1.a) devrait être vers la page 6 selon la table des matières
    # Cherchons dans les premières pages
    for page_num in range(min(10, len(reader.pages))):
        page = reader.pages[page_num]
        page_text = page.extract_text()

        # Chercher si cette page contient la section 1.a)
        if 'identité de la commune' in page_text.lower() or \
           ('1.a' in page_text and 'commune' in page_text.lower()):
            print(f"=== SECTION 1.a) IDENTITÉ DE LA COMMUNE (Page {page_num + 1}) ===\n")
            print(page_text)
            print("\n" + "="*80 + "\n")

            # Afficher aussi la page suivante au cas où
            if page_num + 1 < len(reader.pages):
                next_page = reader.pages[page_num + 1]
                next_text = next_page.extract_text()
                if 'identité du projet' not in next_text.lower():
                    print(f"=== Suite (Page {page_num + 2}) ===\n")
                    print(next_text)
            break
    else:
        # Si pas trouvé, chercher dans tout le document
        print("Recherche dans tout le document...\n")
        all_text = ''
        for page in reader.pages:
            all_text += page.extract_text() + '\n\n'

        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'identité de la commune' in line.lower() and i < 200:
                print(f"Trouvé à la ligne {i}: {line}\n")
                # Afficher le contexte
                for j in range(max(0, i-5), min(len(lines), i+30)):
                    print(lines[j])
                break

except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()
