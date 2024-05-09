#!/bin/bash

model_name="remote_run"
absolute_path=$(readlink -f "$0")
script_dir=$(dirname "$absolute_path")
# Spécifiez le chemin du fichier à rechercher
fichier_a_chercher="${script_dir}/${model_name}.pkl"
echo $fichier_a_chercher
# Vérifiez si le fichier existe
if [ -f "$fichier_a_chercher" ]; then
    echo "Modele déja chargé"
else
    echo "Le model n est pas trouvé, chargement du modèle"
    # Exécutez votre script Python alternatif
    python -m api.model_loader $model_name;
fi
python -m api.main
# uvicorn api.main:app 