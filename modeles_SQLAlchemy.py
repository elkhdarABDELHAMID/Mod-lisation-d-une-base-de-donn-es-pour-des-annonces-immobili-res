import pandas as pd
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/db1')

engine = create_engine(DATABASE_URL)




# Définir la base de données
Base = declarative_base()

# Modèles de tables
class Annonce(Base):
    __tablename__ = 'annonces'
    
    id = Column(Integer, primary_key=True)
    titre = Column(String, nullable=False)
    prix = Column(String)
    datetime = Column(DateTime)
    nb_rooms = Column(Integer)
    nb_baths = Column(Integer)
    surface_area = Column(Float)
    lien = Column(String)

    ville_id = Column(Integer, ForeignKey('villes.id'))
    ville = relationship("Ville", back_populates="annonces")

    equipements = relationship("Equipement", secondary="annonce_equipement", back_populates="annonces")


class Ville(Base):
    __tablename__ = 'villes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    annonces = relationship("Annonce", back_populates="ville")


class Equipement(Base):
    __tablename__ = 'equipements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    annonces = relationship("Annonce", secondary="annonce_equipement", back_populates="equipements")


class AnnonceEquipement(Base):
    __tablename__ = 'annonce_equipement'
    
    annonce_id = Column(Integer, ForeignKey('annonces.id'), primary_key=True)
    equipement_id = Column(Integer, ForeignKey('equipements.id'), primary_key=True)




Base.metadata.create_all(engine)

# Création de la session
Session = sessionmaker(bind=engine)
session = Session()

# Lecture du fichier CSV dans un DataFrame pandas
df = pd.read_csv('cleaned_avito_listing.csv')

# Afficher les colonnes du CSV pour vérification
logging.info("Colonnes CSV : %s", df.columns)

# Compteur des lignes insérées avec succès
inserted_rows = 0

# Insertion des données
for index, row in df.iterrows():
    try:
        if 'title' not in row or 'price' not in row or 'datetime' not in row:
            logging.error(f"Colonnes manquantes dans la ligne {index}. Ignorer cette ligne.")
            continue

        # Conversion sécurisée de la date
        annonce_datetime = pd.to_datetime(row['datetime'], errors='coerce')
        if pd.isnull(annonce_datetime):
            logging.error(f"Date non valide dans la ligne {index}. Ignorer cette ligne.")
            continue

        # Gestion des villes
        ville_name = row['city']
        ville = session.query(Ville).filter_by(name=ville_name).first()
        if not ville:
            ville = Ville(name=ville_name)
            session.add(ville)
            session.commit()

        # Création de l'annonce
        annonce = Annonce(
            titre=row['title'],
            prix=row['price'],
            datetime=annonce_datetime,
            nb_rooms=row.get('nb_rooms', None),
            nb_baths=row.get('nb_baths', None),
            surface_area=row.get('surface_area', None),
            lien=row.get('link', None),
            ville_id=ville.id
        )
        session.add(annonce)
        session.commit()

        # Gestion des équipements
        equipement_names = row['equipement'].split(',') if 'equipement' in row and pd.notnull(row['equipement']) else []
        for equip_name in equipement_names:
            equipement = session.query(Equipement).filter_by(name=equip_name.strip()).first()
            if not equipement:
                equipement = Equipement(name=equip_name.strip())
                session.add(equipement)
                session.commit()
            annonce.equipements.append(equipement)
        
        session.commit()
        inserted_rows += 1

    except Exception as e:
        logging.error(f"Erreur pendant l'insertion de la ligne {index} : {e}")
        session.rollback()

# Fermer la session
session.close()

logging.info(f"Données insérées avec succès! Nombre de lignes insérées : {inserted_rows}")
