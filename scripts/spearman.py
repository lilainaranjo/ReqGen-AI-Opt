# -*- coding: utf-8 -*-
from scipy.stats import spearmanr
from scipy.stats import rankdata

# Medias originales por anotador
anotador1 = [9.429, 8.714, 7.000, 8.857, 8.000, 9.143, 8.429]
anotador2 = [1.429, 3.571, 3.000, 2.286, 3.571, 5.000, 3.571]
anotador3 = [7.286, 7.714, 6.143, 7.143, 7.571, 7.714, 7.143]
anotador4 = [3.571, 5.143, 5.714, 2.714, 6.571, 4.714, 4.143]

# Convertimos medias a rangos (ranking inverso: mayor media = rango 1)
# Para invertir, usamos 'max - value' antes de rankdata, o bien rankdata(-medias)
ranks1 = rankdata([-x for x in anotador1], method='average')
ranks2 = rankdata([-x for x in anotador2], method='average')
ranks3 = rankdata([-x for x in anotador3], method='average')
ranks4 = rankdata([-x for x in anotador4], method='average')

# Calculamos Spearman sobre los rankings
pairs = [
    ("A1-A2", ranks1, ranks2),
    ("A1-A3", ranks1, ranks3),
    ("A1-A4", ranks1, ranks4),
    ("A2-A3", ranks2, ranks3),
    ("A2-A4", ranks2, ranks4),
    ("A3-A4", ranks3, ranks4),
]

with open("outputs_spearman_correlation.txt", "a", encoding="utf-8") as f:
    for name, r_i, r_j in pairs:
        rho, p = spearmanr(r_i, r_j)
        f.write(f"Spearman {name}: ρ={rho:.3f} (p={p:.3f})\n")
