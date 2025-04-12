CREATE TABLE PendingRecipes (
    pendingID INTEGER PRIMARY KEY,
    recipeName VARCHAR(50) NOT NULL,
    recipeDescription VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    reviewedBy INTEGER, -- admin who reviewed
    FOREIGN KEY (reviewedBy) REFERENCES Admins(adminID)
);

CREATE TABLE PendingRecipeIngredients (
    pendingID INTEGER,
    ingredientID INTEGER,
    ingredientQuantity DECIMAL,
    FOREIGN KEY (pendingID) REFERENCES PendingRecipes(pendingID),
    FOREIGN KEY (ingredientID) REFERENCES IngredientItem(ingredientID)
);