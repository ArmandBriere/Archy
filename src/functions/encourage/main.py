import random

import functions_framework

encouragements = [
    "Courage",
    "Tu peux y arriver",
    "T'es le/la/lo meilleur(e)",
    "T'es le/la/lo plus vraiment meilleur(e) du monde",
    "Les froges sont avec toi",
    "Tu mets du soleil dans nos coeurs",
]


@functions_framework.http
def encourage(request):
    """HTTP Cloud Function."""
    request_json = request.get_json(silent=True)
    if request_json:
        name = request_json.get("name", None)
        if name:
            return f"{random.choice(encouragements)} <@{name}> <3!"
    return "Hello !"
