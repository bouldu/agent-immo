PROMPT_CITY_INFORMATION = """
Tu reçois en entrée le nom d’une commune française.
À partir de ce nom, produis les trois blocs d’information suivants :

1. Situation :
- Localisation géographique précise (département, région, appartenance à une
agglomération si pertinent).
- Distance approximative aux grandes villes les plus proches.
- Toujours rester factuel.

2. Couleur politique :
- Nom du/de la maire actuel·le.
- Appartenance politique (sigle).
- Année de début du mandat en cours.
- Si l'information est introuvable : indiquer "information non disponible".

3. Présentation qualitative de la commune :
- Description synthétique du caractère de la commune (5–7 lignes).
- Mention d’au moins un élément patrimonial, culturel ou historique notable.
- Présenter clairement les points caractéristiques du territoire.

Format de sortie JSON strict :

{
  "situation": "…",
  "politique_color": "…",
  "qualitative_presentation": "…"
}

Toujours répondre en français. Si une donnée est incertaine ou absente, le préciser explicitement.
Entrée : {nom_de_la_commune}
Sortie : l’objet JSON ci-dessus complété.
"""
