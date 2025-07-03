import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite_model import Base, IngredientTemp, IngredientCatalog
import ingredients_comparator as comparator 

@pytest.fixture
def session():
    engine = create_engine('sqlite:///ingredients_tests.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
 
def test_new_ingredient(session):

    # cleaning the tables
    session.query(IngredientTemp).delete()
    session.query(IngredientCatalog).delete()
    session.commit()

    # creation and insertion of a new temporary ingredient
    i = IngredientTemp()
    setattr(i, "substance_id", "100000")
    setattr(i, "name_of_common_ingredients_glossary", "CRATAEGUS OXYACANTHA LEAF TEST")
    session.add(i)
    session.commit()

    assert session.query(IngredientTemp).filter_by(substance_id="100000").first() is not None

    # start the comparison script
    # override the session in the comparator
    comparator.session = session
    comparator.Base.metadata.create_all(session.bind)
    # main comparison logic function
    comparator.main_logic(session)
    session.commit()

    new = session.query(IngredientCatalog).filter_by(substance_id="100000").first()
    assert new is not None
    assert new.name_of_common_ingredients_glossary == "CRATAEGUS OXYACANTHA LEAF TEST"

def test_ingredient_modify(session):
    # insert a temporary ingredient
    i = IngredientTemp()
    setattr(i, "substance_id", "100001")
    setattr(i, "name_of_common_ingredients_glossary", "TRICHILIA EMETICA SEED TEST NEW")
    # ingredient present in the catalog with the same substance_id but with a different name before comparison
    old_ingredient = IngredientCatalog(
        substance_id="100001", name_of_common_ingredients_glossary="TRICHILIA EMETICA SEED TEST"
    )
    session.add(i)
    session.add(old_ingredient)
    session.commit()
 
    comparator.session = session
    comparator.main_logic(session)

    modified = session.query(IngredientCatalog).filter_by(substance_id="100001").first()
    # verify that the new ingredient has been updated
    assert modified.name_of_common_ingredients_glossary == "TRICHILIA EMETICA SEED TEST NEW"
    assert modified.modify_date is not None

def test_ingrediente_remove(session):
    catalog_ingredient = IngredientCatalog(
        substance_id="100002", name_of_common_ingredients_glossary="REMOVED TEST"
    )
    session.add(catalog_ingredient)
    session.commit()
 
    # start the comparison script
    # it turns out that the ingredient is no longer in the temporary table
    comparator.session = session
    comparator.main_logic(session)

    rimosso = session.query(IngredientCatalog).filter_by(substance_id="100002").first()
    # verify that removed = 1 has been inserted in the catalog
    assert rimosso.removed == 1