# Suivi des expzditions
API FastAPI (Python 3.13, Pydantic, SQLAlchemy, SQLite) qui enregistre des colis,
calcule les frais de livraison et suit leur expzdition.

## Installation
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Lancer l'API
uvicorn app.main:app --reload (sur mac ca veux jamais se lancer comme ca donc je rajoute python3 -m au debut pour que ca fonctionne)

La base `expeditions.db` est creee automatiquement au lancement.
Documentation interactive : http://127.0.0.1:8000/docs

## Lancer le script de verification des frais
python -m scripts.check_fee

## Lancer les tests
python -m pytest -q

## Routes
| Methode | Route                        | Description                                   |
|---------|------------------------------|-----------------------------------------------|
| POST    | /shipments                   | Cree un colis (201, 409 si doublon, 422)      |
| GET     | /shipments?status=           | Liste (filtre `prepared` ou `shipped`)        |
| POST    | /shipments/{id}/dispatch     | Expedie un colis (404 inconnu, 409 deja fait) |
| GET     | /stats                       | Compteurs et somme des frais                  |

et voila ! c'etait un peu ez vu que j'avais refait le controle de vendredi.
Impression : j'ai toujours pas le sentiment de comprendre pleinement le truc (j'arrive un minimum a comprendre ce que je fais mais j'arrive pas a m'habituer au langage, donc ca me perd). vu que j'ai deja fait le controle de vendredi, y'a eu beaucoup de copie colle avec seulement les variables a changer, mais bon, j'ai encore 3 ans pour devenir un crac en python. c'est tout pour moi !