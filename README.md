# T411_unblocked

## Préparation
Cloner le git : 
```bash
git clone git@github.com:0x726170746f72/t411_unblocked.git
```

## Pré-installation
Installer python3.

## Installation
Créer un virtual env : 
```bash
virtualenv -p python3 env
```
Rentrer dans l'env :
```bash
source env/bin/activate
```
Installer les pré-requis:
```bash
pip3 install -r requirements.txt
```
## Paramétrage
Créer et éditer le fichier /t411/local_settings.py comme ceci:
```bash
T411_SETTINGS = {
  'base_url':'http://api.t411.li',
  'username':'<votre_username>',
  'password':'<votre_password',
  'tracker_key':'<votre clef tracker>',
  'tracker_url':'http://t411.download/',
  'fake_btclient':'<faux identifiant de client bt, 20chars> | OPTIONNEL',
  'default_nbr_peers':<nombre de pairs maximum à demander, défaut:50> | OPTIONNEL
}
```
Votre clef tracker est disponible sur la page 'mon compte' de t411.

## Démarrage
Faire les migrations avant de démarrer le serveur : 
```bash
./manage.py makemigrations api
./manage.py migrate
./manage.py runserver
```

Maintenant, accéder à http://127.0.0.1:8000.  
Pour bind sur une adresse/un port personnalisé : 

```bash
./manage.py runserver adress:port
```
