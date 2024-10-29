import pandas as pd
import numpy as np

# Génération de données aléatoires pour 5000 lignes
n = 5000
np.random.seed(42)

# Génération des colonnes
date_block_num = np.random.randint(0, 36, size=n)  # Périodes mensuelles entre 0 et 35
shop_id = np.random.randint(1, 60, size=n)  # 60 magasins (identifiants entre 1 et 60)
item_id = np.random.randint(1, 500, size=n)  # 500 produits (identifiants entre 1 et 500)
item_price = np.round(np.random.uniform(10, 1000, size=n), 2)  # Prix des produits entre 10 et 1000
vente_mensuelle = np.random.randint(0, 20, size=n)  # Ventes mensuelles entre 0 et 20

# Création du DataFrame
df_vente_mensuelle = pd.DataFrame({
    'date_block_num': date_block_num,
    'shop_id': shop_id,
    'item_id': item_id,
    'item_price': item_price,
    'vente_mensuelle': vente_mensuelle
})

# Sauvegarder dans un fichier CSV
df_vente_mensuelle.to_csv('C:/Users/Maryse/Documents/Proj_Predict_Future_Sales/nouvelle_bd_2.csv', index=False)

print("Fichier CSV généré avec succès.")
