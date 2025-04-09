/*

CREATE TABLE Admins (
    adminID INTEGER PRIMARY KEY,
    userID INTEGER NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID)
);



CREATE TABLE RecipeIngredients(
    recipeID INTEGER,
    ingredientID INTEGER,
    ingredientQuantity DECIMAL,
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID),
    FOREIGN KEY (ingredientID) REFERENCES IngredientItem(ingredientID)
);


CREATE TABLE UserFavoriteIngredients(
    userID INTEGER,
    ingredientID INTEGER,
    savedDate DATE,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (ingredientID) REFERENCES IngredientItem(ingredientID)   
);


CREATE TABLE UserFavoriteRecipes(
    userID INTEGER,
    recipeID INTEGER,
    savedDate DATE,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (recipeID) REFERENCES Recipes(recipeID) 
);



CREATE TABLE Recipes (
    recipeID INTEGER PRIMARY KEY,
    recipeName VARCHAR(50) NOT NULL,
    recipeDescription VARCHAR(500) NOT NULL
);



CREATE TABLE Users(
    userID INTEGER PRIMARY KEY,
    userName VARCHAR(50) NOT NULL,
    userPassword VARCHAR(20) NOT NULL
);


CREATE TABLE IngredientItem (
    ingredientID INTEGER PRIMARY KEY,
    ingredientName VARCHAR(50) NOT NULL,
    Calories_per_100g DECIMAL(5, 2) NOT NULL,
    Fat_g DECIMAL(5, 2),
    SaturatedFats_g DECIMAL(5, 2),
    MonounsaturatedFats_g DECIMAL(5, 2),
    PolyunsaturatedFats_g DECIMAL(5, 2),
    Carbohydrates_g DECIMAL(5, 2),
    Sugars_g DECIMAL(5, 2),
    Protein_g DECIMAL(5, 2),
    DietaryFiber_g DECIMAL(5, 2),
    Cholesterol_mg DECIMAL(5, 2),
    Sodium_mg DECIMAL(5, 2),
    Water_g DECIMAL(5, 2),
    VitaminA_mg DECIMAL(5, 2),
    VitaminB1_mg DECIMAL(5, 2),
    VitaminB11_mg DECIMAL(5, 2),
    VitaminB12_mg DECIMAL(5, 2),
    VitaminB2_mg DECIMAL(5, 2),
    VitaminB3_mg DECIMAL(5, 2),
    VitaminB5_mg DECIMAL(5, 2),
    VitaminB6_mg DECIMAL(5, 2),
    VitaminC_mg DECIMAL(5, 2),
    VitaminD_mg DECIMAL(5, 2),
    VitaminE_mg DECIMAL(5, 2),
    VitaminK_mg DECIMAL(5, 2),
    Calcium_mg DECIMAL(5, 2),
    Copper_mg DECIMAL(5, 2),
    Iron_mg DECIMAL(5, 2),
    Magnesium_mg DECIMAL(5, 2),
    Manganese_mg DECIMAL(5, 2),
    Phosphorus_mg DECIMAL(5, 2),
    Potassium_mg DECIMAL(5, 2),
    Selenium_mg DECIMAL(5, 2),
    Zinc_mg DECIMAL(5, 2),
    NutritionDensity DECIMAL(5, 2)
);
*/
