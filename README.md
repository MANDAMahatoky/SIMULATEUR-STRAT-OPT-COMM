# SIMULATEUR-STRAT-OPT-COMM
🇲🇬 Simulateur Stratégique & Optimisation Commerciale - Madagascar

Un outil de pilotage commercial multiniveaux développé sous Streamlit pour analyser, simuler et optimiser les performances des agences commerciales (Commerciaux/Vendeurs - CS, et Manageurs/Ventes - MV) à travers Madagascar.

🚀 Fonctionnalités Principales

Tableau de Bord National (KPIs) : Vue d'ensemble instantanée des volumes moyens par CS/MV et de la charge moyenne de points de vente (PDV).

Analyse Croisée & Codes Couleurs : Suivi dynamique des statuts d'équilibre, de surcharge ou de sous-charge par agence pour les CS et les MV.

Paramétrage Personnalisable : Ajustement en temps réel des objectifs de visites, des jours travaillés, des coûts de structure et des seuils d'alerte via la barre latérale.

Simulation des Zones Blanches : Module interactif pour évaluer l'impact de l'intégration de nouvelles zones et volumes par agence.

Simulation Financière (Break-even) : Calcul automatique du seuil de rentabilité et de la couverture des coûts par CS selon la marge nette par hectolitre.

Cartographie Interactive : Visualisation géographique des agences à Madagascar via Plotly.

Recommandations & Plan d'Action Régional : Suggestions automatisées de transferts inter-agences, de recrutements locaux ou de renforts d'encadrement, avec option d'export au format CSV.

🛠️ Prérequis & Installation Locale

Si vous souhaitez exécuter ou modifier ce projet en local, assurez-vous d'avoir Python installé, puis suivez ces étapes :

Cloner le dépôt :

git clone https://github.com/votre-nom-utilisateur/votre-repo.git
cd votre-repo


Créer un environnement virtuel (recommandé) :

python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate


Installer les dépendances :

pip install streamlit pandas numpy plotly


Lancer l'application :

streamlit run app.py


📦 Déploiement sur Streamlit Community Cloud

L'application est configurée pour être déployée facilement sur Streamlit Cloud :

Créez un dépôt public sur GitHub contenant votre fichier principal (ex: app.py) et un fichier requirements.txt listant vos dépendances (streamlit, pandas, numpy, plotly).

Rendez-vous sur Streamlit Community Cloud.

Connectez votre compte GitHub, sélectionnez votre dépôt, votre branche principale et le fichier de script (app.py).

Cliquez sur Deploy !

📄 Dépendances (requirements.txt)

streamlit>=1.20.0
pandas>=1.5.0
numpy>=1.22.0
plotly>=5.0.0


🤝 Contribuer

Les contributions, suggestions d'amélioration ou signalements de bugs sont les bienvenus. N'hésitez pas à ouvrir une Issue ou à proposer une Pull Request.
