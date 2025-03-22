CREATE TABLE FoodItem (
    FoodID INT PRIMARY KEY,
    FoodName VARCHAR(50) NOT NULL,
    CaloricValue_in_kcal INT NOT NULL
);

CREATE TABLE FoodNutrition (
    FoodID INT,
    AmountPerServing_grams INT,
    FOREIGN KEY (FoodID) REFERENCES FoodItem(FoodID)
);

CREATE TABLE NutritionalMetrics(
    NutrientID INT PRIMARY KEY,
    NutrientName VARCHAR(20),
    Unit VARCHAR(2)
);