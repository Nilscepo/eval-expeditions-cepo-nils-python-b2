def shipping_fee(weight_g: int) -> float:
    MAX_WEIGHT_G = 20000

    if weight_g <= 0 or weight_g > MAX_WEIGHT_G:
        raise ValueError(f"Poids invalide : {weight_g} g, le poids doit etre compris entre 1 et {MAX_WEIGHT_G} g")
    if weight_g <= 500:
        return 3.50
    if weight_g <= 2000:
        return 6.0
    return 10.0