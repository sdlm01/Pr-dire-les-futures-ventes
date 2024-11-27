Pipeline CI/CD GitLab pour une application FastAPI de prediction des futures ventes
Ce dépôt contient un pipeline CI/CD pour construire, tester et déployer une application FastAPI à l'aide de Docker et Kubernetes. Le pipeline est défini dans le fichier .gitlab-ci.yml.

Étapes du pipeline

Étape de construction (Build)
L'étape build crée une image Docker pour l'application FastAPI et la pousse dans le registre GitLab.

Détails

Image utilisée : docker:20.10.24
Services utilisés : docker:20.10.24-dind
Variables d'environnement :
IMAGE_TAG : Le tag de l'image Docker, généré dynamiquement avec $CI_REGISTRY_IMAGE et $CI_COMMIT_REF_SLUG.

Commandes exécutées

Construction de l'image Docker :
docker build -t $IMAGE_TAG .
Connexion au registre GitLab :
echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
Poussée de l'image dans le registre :
docker push $IMAGE_TAG

Déclencheurs
Cette étape s'exécute sur les branches :

main
develop


Étape de tests automatisés (Test)
L'étape test exécute des tests automatisés avec pytest pour valider le bon fonctionnement de l'application.

Détails


Image utilisée : L'image Docker générée lors de l'étape build ($IMAGE_TAG).


Commandes exécutées :
Installation des dépendances Python :
pip install -r requirements_fastapi.txt
Lancement des tests
pytest /app/tests/


Déclencheurs
Cette étape s'exécute sur les branches :

main
develop


Étape de déploiement (Deploy)
L'étape deploy déploie l'application sur un cluster Kubernetes à l'aide de kubectl.

Détails

Image utilisée : bitnami/kubectl:latest
Commandes exécutées :

Génération du fichier kubeconfig.yaml à partir de la variable d'environnement KUBECONFIG
echo "$KUBECONFIG" > kubeconfig.yaml
Test de la connexion au cluster Kubernetes :
kubectl --kubeconfig=kubeconfig.yaml cluster-info
Application des fichiers manifestes Kubernetes :
kubectl --kubeconfig=kubeconfig.yaml apply -f deployment.yaml
kubectl --kubeconfig=kubeconfig.yaml apply -f service.yaml
Déclencheurs

Cette étape s'exécute uniquement sur la branche main.

#Variables d'environnement
Le pipeline utilise les variables d'environnement suivantes :
CI_REGISTRY : URL du registre GitLab.
CI_REGISTRY_USER : Nom d'utilisateur pour le registre GitLab.
CI_REGISTRY_PASSWORD : Mot de passe ou jeton d'accès pour le registre GitLab.
IMAGE_TAG : Tag de l'image Docker, généré automatiquement.
KUBECONFIG : Configuration Kubernetes encodée en Base64 pour l'authentification avec le cluster.
#Fichiers importants
deployment.yaml : Manifeste Kubernetes pour déployer l'application.
service.yaml : Manifeste Kubernetes pour exposer l'application.
#Comment utiliser
Configurer les variables d'environnement :
Ajoutez les variables nécessaires (CI_REGISTRY, CI_REGISTRY_USER, CI_REGISTRY_PASSWORD, KUBECONFIG) dans les paramètres de votre projet GitLab sous Paramètres > CI/CD > Variables.
Pousser le code :
Poussez vos changements sur les branches main ou develop pour déclencher le pipeline.
