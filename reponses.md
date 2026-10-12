# Reponses

## Exercice 1 — Frais de livraison
python -m scripts.check_fee
3.50 €
6.00 €
10.00 €

## Exercice 3 — Persistance
Verification du redemarrage :

1. Lancer l'API :
uvicorn app.main:app

2. Creer un colis :
curl -X POST localhost:8000/shipments -H "Content-Type: application/json" -d '{"reference":"R1","recipient":"Alice","weight_g":501}'

3. L'expedier : 
curl -X POST localhost:8000/shipments/1/dispatch
4. Arreter l'API (Ctrl+C) puis la relancer.

5. curl localhost:8000/shipments : 
le colis est toujours la, avec status: "shipped" et shipping_fee: 6.0.