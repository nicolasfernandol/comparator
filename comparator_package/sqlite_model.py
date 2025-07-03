from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime
from datetime import datetime, timezone

# function to create a declarative base for ORM classes
Base = declarative_base()

# function to get the current date and time in UTC
def now_utc():
    return datetime.now(timezone.utc)

# class that represents the ingredients table
class IngredientBase:
    name_of_common_ingredients_glossary = Column(Text)
    other_restrictions = Column(Text)
    note = Column(Text)
    ref_number = Column(Text)
    sccs_opinion_urls = Column(Text)
    inn_name = Column(Text)
    other = Column(Text)
    item_type = Column(Text)
    chemical_name = Column(Text)
    sccs_opinion = Column(Text)
    ref_number_letter = Column(Text)
    language = Column(Text)
    chemical_description = Column(Text)
    es_st_checksum = Column(Text)
    reference = Column(Text)
    cosmetic_restriction = Column(Text)
    ec_number = Column(Text)
    maximum_concentration = Column(Text)
    identified_ingredient = Column(Text)
    official_journal_publication = Column(Text)
    inci_name = Column(Text)
    es_st_file_name = Column(Text)
    cas_number = Column(Text)
    substance_id = Column(Text)
    datasource = Column(Text)
    annex_number = Column(Text)
    product_type_body_parts = Column(Text)
    ph_eur_name = Column(Text)
    es_content_type = Column(Text)
    other_regulations = Column(Text)
    classification_information = Column(Text)
    function_name = Column(Text)
    es_da_ingest_date = Column(Text)
    current_version = Column(Text)
    corporate_search_version = Column(Text)
    url = Column(Text)
    es_st_url = Column(Text)
    es_da_queue_date = Column(Text)
    ref_number_digit = Column(Text)
    colour = Column(Text)
    wording_of_conditions = Column(Text)
    inci_usa_name = Column(Text)
    related_regulations = Column(Text)
    perfuming = Column(Text)
    status = Column(Text)

# class that represents the temporary ingredients table
class IngredientTemp(Base, IngredientBase):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, autoincrement=True)


# class that represents the compared ingredients table
class IngredientCatalog(Base, IngredientBase):
    __tablename__ = "compared_ingredients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    insert_date = Column(DateTime, default=now_utc)
    modify_date = Column(DateTime, default=None, onupdate=now_utc)
    removed = Column(Integer, default=0)