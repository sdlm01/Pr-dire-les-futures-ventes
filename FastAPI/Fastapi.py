from fastapi import FastAPI
import pandas as pd
import pickle
from pydantic import BaseModel
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from fastapi import UploadFile, File

# Charger le modèle entraîné 
with open('/app/ML/model_vente_mensuelle.pkl', 'rb') as f: #Le charchement est fait à partir du volume du docker
    model = pickle.load(f)

# Créer une instance de l'application FastAPI
app = FastAPI()

# Modèle pour les requêtes de prédiction
class PredictionRequest(BaseModel):
    shop_id: int
    item_id: int
    item_price: float
    date_block_num: int 
 

# Endpoint de prédiction
@app.post("/predict")
def predict_sales(request: PredictionRequest):
    # Préparer les données pour la prédiction
    input_data = pd.DataFrame([{
        'date_block_num': request.date_block_num,
        'shop_id': request.shop_id,
        'item_id': request.item_id,
        'item_price': request.item_price,
    }])
    
    # Faire la prédiction
    prediction = model.predict(input_data)[0]
    
    # Convertir en float pour éviter les erreurs liées à numpy.float32
    prediction = float(prediction)
    
    return {"prediction": prediction}

# Endpoint pour réentraîner le modèle
@app.post("/train")
def retrain_model():
    # Simuler la recharge des nouvelles données depuis une source
    df_vente_mensuelle = pd.read_csv('/app/Data/nouvelle_bd.csv')  

    # Préparation des features et de la cible
    X = df_vente_mensuelle[['date_block_num', 'shop_id', 'item_id', 'item_price']]
    y = df_vente_mensuelle['vente_mensuelle']

    # Séparation en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Réentraîner le modèle
    global model
    model = XGBRegressor(objective='reg:squarederror', n_estimators=100, max_depth=6)
    model.fit(X_train, y_train)

    # Sauvegarder le modèle mis à jour
    with open('/app/ML/model_vente_mensuelle.pkl', 'wb') as f:
        pickle.dump(model, f)

    return {"message": "Modèle réentraîné et sauvegardé avec succès."}


# Endpoint pour mettre à jour les données
@app.post("/update_data")
async def update_data(file: UploadFile = File(...)):
    try:
        # Charger les nouvelles données envoyées par l'utilisateur
        new_data = pd.read_csv(file.file)

        # Charger la base de données actuelle des ventes
        df_vente_mensuelle = pd.read_csv('/app/Data/nouvelle_bd.csv')

        # Ajouter les nouvelles données à la base existante
        df_vente_mensuelle = pd.concat([df_vente_mensuelle, new_data], ignore_index=True)

        # Sauvegarder la nouvelle version des données
        df_vente_mensuelle.to_csv('/app/Data/updated_vente_mensuelle.csv', index=False)

        return {"message": "Données mises à jour avec succès."}
    except Exception as e:
        return {"error": str(e)}


# Exécuter l'API avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
