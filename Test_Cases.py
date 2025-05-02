import sqlite3
from user_queries import *
from general_queries import *
from ingredient_queries import *
from recipe_queries import *
from user_queries import *

connection = sqlite3.connect("nutrition.db")
cursor = connection.cursor()

def test_user_management():
    # Test adding a new user
    assert add_user(cursor, "jsons/add_user.json") == True
    
    # Test adding duplicate user
    assert add_user(cursor, "jsons/add_user.json") == False
    
    # Test checking user exists
    assert check_user_exists(cursor, "admin1", "admin123") == True
    assert check_user_exists(cursor, "nonexistent", "wrongpass") == False

def test_user_favorites():
    # Test adding favorite recipe
    assert add_user_favorite(cursor, "jsons/add_user_favorite.json") == True
    
    # Test querying favorites
    view = query_user_favorites(cursor, "jsons/query_user_favorites.json")
    assert view is not None
    print_view(cursor, view)
    
    # Test dropping favorite
    assert drop_user_favorite(cursor, "jsons/drop_user_favorite.json") == True
    
    # Test dropping non-existent favorite
    assert drop_user_favorite(cursor, "jsons/drop_user_favorite.json") == False


def test_recipe_workflow():
    # Test recipe submission
    assert submit_recipe_for_approval(cursor, "jsons/recipe_submission.json") == True
    
    # Test recipe approval
    assert recipe_approval_rejection(cursor, "jsons/approval_request.json") is not None
    
    # Test recipe nutrition calculation
    nutrition_view = calculate_recipe_nutrition(cursor, 1)
    assert nutrition_view is not None
    print_view(cursor, nutrition_view)


# test_user_favorites()
# test_user_management()
connection.commit()
connection.close()