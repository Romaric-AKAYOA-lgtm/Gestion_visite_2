from setuptools import setup, find_packages
import os

# Lire et traiter le fichier requirements.txt si disponible
requirements_file = "requirements.txt"
if os.path.exists(requirements_file):
    with open(requirements_file, encoding="utf-8") as f:
        required = [
            line.strip() for line in f.readlines() 
            if line.strip() and not line.startswith("#")  # Ignore les lignes vides et les commentaires
        ]
else:
    required = []

setup(
    name="Gestion_Visite_2",  # Nom du package
    version="1.0",  # Version du package
    description="Application de gestion des visites",  # Brève description
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",  # Description longue si README.md existe
    long_description_content_type="text/markdown",  # Format Markdown pour PyPI
    author="Ton Nom",  # Auteur (à modifier)
    author_email="ton.email@example.com",  # Email de l’auteur (optionnel)
    license="MIT",  # Type de licence (modifiable)
    url="https://github.com/ton-projet/Gestion_Visite_2",  # URL du projet (à modifier)
    packages=find_packages(),  # Recherche automatique des packages
    install_requires=required,  # Dépendances à installer
    python_requires=">=3.7",  # Version minimale de Python requise
    entry_points={  # Point d'entrée de la commande CLI
        "console_scripts": [
            "start-django=Gestion_Visite_2.start_server:start_server",  # Commande personnalisée
        ],
    },
    classifiers=[  # Catégories pour PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={  # Liens supplémentaires
        "Documentation": "https://github.com/ton-projet/Gestion_Visite_2/wiki",
        "Code Source": "https://github.com/ton-projet/Gestion_Visite_2",
        "Issues": "https://github.com/ton-projet/Gestion_Visite_2/issues",
    },
)
