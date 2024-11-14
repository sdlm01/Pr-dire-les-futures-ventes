from airflow import DAG 
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.empty import EmptyOperator
import pendulum  
from datetime import timedelta
from airflow.operators.python import PythonOperator
import requests

# Configuration des paramètres du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Fonction Python pour envoyer le fichier de données
def send_update_data():
    url = 'http://fastapi:8000/update_data'
    file_path = '/opt/airflow/dags/nouvelle_bd.csv'  # Chemin du fichier dans le conteneur Airflow
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
        response.raise_for_status()  # Lève une exception si le code HTTP n'est pas 200
    return response.json()

# Initialiser le DAG
with DAG(
    'model_training_update',
    default_args=default_args,
    description="DAG pour réentraîner le modèle et mettre à jour les données",
    schedule='@daily',  # Exécuter tous les jours
    start_date=pendulum.today('UTC').add(days=-1),
    catchup=False,
) as dag:

    # Tâche de démarrage
    start_task = EmptyOperator(task_id='start')

    # Tâche pour réentraîner le modèle
    train_model = HttpOperator(
        task_id='train_model',
        method='POST',
        http_conn_id='fastapi',  # Nom de la connexion dans Airflow
        endpoint='/train',
        headers={"Content-Type": "application/json"},
        response_check=lambda response: response.status_code == 200,
    )

    # Tâche pour mettre à jour les données de vente en utilisant un opérateur Python
    update_data = PythonOperator(
        task_id='update_data',
        python_callable=send_update_data,
    )

    # Tâche de fin
    end_task = EmptyOperator(task_id='end')

    # Ordre des tâches
    start_task >> [train_model, update_data] >> end_task
