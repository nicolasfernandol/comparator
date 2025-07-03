from db_utils import get_session
from sqlite_model import Base, IngredientTemp, IngredientCatalog, now_utc

def main_logic(session):
    # initialize the database
    # create tables if they do not exist
    Base.metadata.create_all(session.bind)

    # load temporary data
    temp_ingredients = {
        temp_ingredient.substance_id: temp_ingredient
        for temp_ingredient in session.query(IngredientTemp).all()
        if temp_ingredient.substance_id
    }

    # load catalog data
    catalog_ingredients = {
        catalog_ingredient.substance_id: catalog_ingredient
        for catalog_ingredient in session.query(IngredientCatalog).all()
        if catalog_ingredient.substance_id
    }

    # initialize lists for new ingredients, modified ingredients, and removed ingredients
    new_ingredients = []
    modified_ingredients = []
    removed_ingredients = []

    # NEW INGREDIENTS
    # loop through each temporary ingredient
    for substance_id, ingredient_temp in temp_ingredients.items():

        # if the temporary ingredient does NOT EXISTS in the catalog, it is a new ingredient
        if substance_id not in catalog_ingredients:
            new_ingredients.append(ingredient_temp) # add to the list of new ingredients
            continue # continue to the next ingredient

        # MODIFIED INGREDIENTS
        # if the temporary ingredient EXISTS in the catalog, compare the fields
        # variables for comparison
        ingredient_catalog = catalog_ingredients[substance_id]
        modified = False

        # loop through all fields of the object
        for field_name in ingredient_temp.__dict__:
            # ignore private fields and the ID field
            if field_name.startswith("_") or field_name == "id":
                continue

            # read the current values of that field in the two objects
            value_temp = getattr(ingredient_temp,field_name)  # getattr(object, attribute's name)
            value_catalog = getattr(ingredient_catalog,field_name)

            # if the values are different, update the field in the catalog
            if value_temp != value_catalog:
                setattr(ingredient_catalog,field_name, value_temp) # setattr(object, attribute's name, value to set)
                modified = True

        # if at least one field value has changed, update the modification date
        if modified:
            ingredient_catalog.modify_date = now_utc()
            modified_ingredients.append(ingredient_catalog)

    # REMOVED INGREDIENTS
    # check if there are ingredients in the catalog that are no longer in the temp
    for substance_id, ingredient_catalog in catalog_ingredients.items():
        if substance_id not in temp_ingredients:
            # if missing, it means it has been removed
            # 0 FALSE
            # 1 TRUE (REMOVED)

            ingredient_catalog.removed = 1
            removed_ingredients.append(ingredient_catalog)

    # for each new ingredient identified
    for ingrediente_temp in new_ingredients:
        # extract all fields to copy, except private ones and the ID
        dati_ingredienti = {
            campo: valore for campo, valore in ingrediente_temp.__dict__.items()
            if not campo.startswith("_") and campo != "id"
        }

        # create a new object for the catalog table
        nuovo_ingrediente = IngredientCatalog(**dati_ingredienti)

        # set the loading date to the current time (UTC)
        nuovo_ingrediente.insert_date = now_utc()

        # add the new ingredient to the session for saving
        session.add(nuovo_ingrediente)

    # save changes to the database
    session.commit()

    print(f"New ingredients: {len(new_ingredients)}")
    print(f"Modified ingredients:: {len(modified_ingredients)}")
    print(f"Removed ingredients: {len(removed_ingredients)}")

if __name__ == "__main__":
    session = get_session()
    main_logic(session)

# script execution
"""
python ingredients_comparator.py
python3 ingredients_comparator.py
"""