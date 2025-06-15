# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from irrCAC.raw import CAC

all_data = np.array([
  [[10, 1, 9],
    [7, 4, 5],
    [8, 3, 8],
    [9, 3, 8],
    [5, 4, 8],
    [10, 5, 9],
    [8, 4, 7]],
    
  [[10, 2, 6],
    [9, 5, 9],
    [8, 4, 6],
    [9, 3, 7],
    [9, 4, 8],
    [10, 6, 8],
    [9, 4, 7]],
    
  [[10, 1, 5],
    [9, 3, 7],
    [8, 2, 5],
    [9, 1, 5],
    [9, 4, 7],
    [10, 4, 6],
    [9, 3, 6]],
    
  [[8, 2, 8],
    [10, 5, 10],
    [8, 2, 7],
    [9, 2, 8],
    [9, 4, 8],
    [10, 4, 8],
    [9, 3, 8]],
    
  [[10, 1, 9],
    [9, 3, 8],
    [4, 3, 4],
    [9, 3, 8],
    [8, 2, 7],
    [9, 6, 8],
    [9, 4, 8]],
    
  [[9, 2, 8],
    [8, 1, 7],
    [7, 4, 7],
    [8, 1, 7],
    [8, 3, 7],
    [7, 5, 7],
    [9, 3, 7]],
    
  [[9, 1, 6],
    [9, 4, 8],
    [6, 3, 6],
    [9, 3, 7],
    [8, 4, 8],
    [8, 5, 8],
    [6, 4, 7]],
])

for i, data in enumerate(all_data):
    df = pd.DataFrame(data, columns=["Anotador 1", "Anotador 2", "Anotador 3"])
    cac_4raters = CAC(df, weights='ordinal')
    alpha = cac_4raters.krippendorff()
    value = alpha['est']['coefficient_value']
    with open("../outputs/krippendorff_alpha.txt", "a", encoding="utf-8") as f:
        f.write(f"Krippendorff's alpha Q{i+1}: {value}\n")
