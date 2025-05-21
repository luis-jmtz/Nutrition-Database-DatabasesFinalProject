Food Nutrition Database  
Luis Martinez  
Professor Chris Cianci  
COMP 373 Databases  
3 May 2025

**1\. Archive of the application components**  
*Python version and Libraries*:

* Python: 3.11.8  
* Pip: 24.0  
* Flask: 3.1.0  
* Pandas: 2.2.3  
* SQLite: 3.45.3  
* Json: 2.0.9

*Code and Data Acquisition*  
I’ve included all critical SQL and Python code in my submission, organized into the Table\_initializer and Python\_Scripts folders. The full repository is available on GitHub ([https://github.com/luis-jmtz/Nutrition-Database-DatabasesFinalProject](https://github.com/luis-jmtz/Nutrition-Database-DatabasesFinalProject) ). The original dataset was sourced from Kaggle ([https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset](https://www.kaggle.com/datasets/utsavdey1410/food-nutrition-dataset) ), and the Data folder contains both the raw files (marked with "subset" in their names) and the cleaned versions, along with the Jupyter notebook used for data processing. To enhance testing, I generated synthetic users and recipes using an LLM. The Data\_population\_code scripts loaded the processed data into the database, and I manually added supplemental test data during development.

**2\. Report**  
Abstract  
This project addresses the challenge college students face in making informed dietary decisions, as existing tools often lack flexibility or have cumbersome interfaces, making the process inefficient. To solve this, I developed the backend for a nutrition database application that allows users to filter foods by specific nutritional values, view recipes with their nutritional data, save favorite recipes/ingredients, and submit requests to add new entries. While I initially planned to implement a full-stack solution, time constraints led me to prioritize backend functionality. However, I ensured seamless frontend integration by designing the system to process JSON data. The application uses a SQLite database populated with a Kaggle nutrition dataset, converted from CSV for optimized querying. Python serves as the backend language, with Flask available for future frontend integration. Although dietary restriction filters (e.g., vegan, shellfish-free) were not implemented, they would be a natural extension in future iterations. This project demonstrates key database concepts such as normalization, SQL querying, and data integrity while providing practical utility for students seeking personalized dietary insights.

User Documentation  
Since this application currently operates as a backend system without a graphical interface, all interactions would theoretically occur through simple forms in a future frontend implementation. Below are practical use-case scenarios demonstrating how users would interact with the system:

*New User Registration*

1. Action: Click "Sign Up" on the homepage  
2. Input:  
   1. Choose a unique username (e.g., "healthyeater123")  
   2. Create a secure password  
3. System Response: Immediate account creation with basic user privileges  
   Limitation: No password recovery feature exists yet \- users must remember their credentials

*Finding Low-Sodium Ingredients*

1. Action: Navigate to "Browse Ingredients" → "Advanced Filters"  
2. Input:  
   1. Set "Sodium" maximum to 50mg  
   2. Optional: Sort results A-Z  
3. System Response: Displays ingredients like cucumbers (1.8mg) and apples (0mg)  
   Limitation: Filters only work with exact numeric values, not ranges like "low" or "high"

*Filtering Ingredients by Multiple Nutritional Values*

1. Action: Navigate to "Ingredients" → "Advanced Nutritional Filter"  
2. Input:  
   1. Set multiple nutritional criteria:  
      1. Protein: Minimum 10g  
      2. Carbohydrates: Maximum 5g  
      3. Fat: Maximum 3g  
3. System Response: Displays ingredients like chicken breast (high protein, low carbs/fat) and spinach (low carbs/fat, moderate protein)  
4. Limitation: Users must input exact numeric values; no pre-set dietary profiles (e.g., "Keto-friendly") are available yet.

*Saving Favorite Recipes*

1. Action: Search for "Quinoa Salad" recipe and view details  
2. Input: Click "Add to Favorites" heart icon  
3. System Response: Recipe appears in "My Favorites" section  
   Justification: Requires login to personalize experience while preventing duplicate entries

*Filtering Recipes by Dietary Preferences*

1. Action: Navigate to "Recipes" → "Dietary Filters"  
2. Input:  
   1. Select dietary preferences:  
      1. "High Protein" (recipes with ≥20g protein per serving)  
      2. "Low Carb" (recipes with ≤10g carbs per serving)  
3. System Response: Displays recipes like grilled salmon with asparagus (high protein, low carb) and egg-white omelets  
   1. Justification: Combines nutritional calculations with ingredient exclusions for personalized results.  
   2. Limitation: Filters apply to entire recipes only, not individual servings or customizable portions.

*Submitting a New Recipe*

1. Action: Select "Contribute" → "Submit Recipe"  
2. Input:  
   1. Recipe name: "Avocado Toast"  
   2. Description: "Simple breakfast with healthy fats"  
   3. Add ingredients from database (avocado, whole wheat bread) with quantities  
3. System Response: "Submission received for admin approval" notification  
   Limitation: Only pre-approved ingredients can be used to ensure nutritional accuracy

*Admin Approving Content*

1. Action: Admin logs in to "Pending Approvals" dashboard  
2. Input:  
   1. Reviews submitted avocado toast recipe  
   2. Clicks "Approve" after verification  
3. System Response: Recipe becomes publicly searchable immediately  
   Security Justification: Two-tier system prevents incorrect or malicious submissions

*Key Limitations and Workarounds*  
The system prioritizes precision by displaying exact nutritional values (e.g., 5.3g of protein) to maintain scientific accuracy based on source datasets. Users can apply multiple nutritional filters (e.g., high-protein and low-carb), but the backend currently does not support natural-language descriptors like "high" or "low." Instead, users must specify exact numerical thresholds. Nutritional values for recipes are not stored in the database; they are calculated dynamically each time the relevant function is called. This approach reduces storage requirements without noticeably affecting performance. However, it also means that users cannot sort recipes by nutritional content, only by ingredients. While not ideal, a potential workaround in future updates could involve calculating nutritional information after a user selects a recipe. Another current limitation is the lack of functionality to exclude specific ingredients. This feature would be relatively straightforward to implement if development continues.

Engineering Documentation  
*Data Structures:*  
Database Schema:

* Users: Stores user credentials (userID, userName, userPassword)  
* Admins: Contains admin privileges (userID references Users)  
* IngredientItem: Comprehensive nutritional data (ingredientID, ingredientName, Calories\_per\_100g, Protein\_g, etc.)  
* PendingIngredientItem: Mirrors IngredientItem for submissions awaiting approval  
* Recipes: Recipe metadata (recipeID, recipeName, recipeDescription)  
* PendingRecipes: Recipes pending admin review  
* RecipeIngredients: Junction table linking recipes to ingredients with quantities  
* PendingRecipeIngredients: Temporary storage for ingredients in pending recipes  
* UserFavoriteIngredients and UserFavoriteRecipes: Many-to-many relationship tables for user favorites

Application Structure:  
The application follows a modular backend structure centered around a SQLite database (nutrition.db), with Main.py serving as the entry point to initialize connections and coordinate modules. Core functionality is organized into specialized query handlers: ingredient\_queries.py manages ingredient filtering and approvals, recipe\_queries.py handles recipe calculations and submissions, user\_queries.py governs authentication and favorites, and general\_queries.py provides developer-end tools. The jsons/ folder contains the .json files that are modified and then called by functions for the frontend application. Temporary SQL views optimize complex nutritional calculations. The supporting Data/ folder houses raw and processed datasets, and the Data\_population\_code/ folder contains population scripts, maintaining a clear separation between data initialization and application logic. The SQL/ folder contains the initial initialization code for the database tables. This structure balances separation of concerns with centralized database access, enabling scalable feature development and straightforward integration with future frontends.

Key Design Decisions:   
The system employs a modular architecture with query-specific files (ingredients, recipes, users) to separate concerns. For data integrity, an approval workflow implements a dual-table system (main \+ pending tables) with mandatory admin verification through is\_admin() checks. This adds complexity but ensures quality control. Frontend-backend decoupling is achieved via JSON interfaces where all complex functions accept file paths (e.g., submit\_recipe\_for\_approval(cursor, json\_path)). Complex queries leverage temporary views like RecipeNutritionView to reduce code repetition, though this introduces view cleanup requirements as a trade-off.

Setup and How to Run:  
	If you have all the same versions of the required libraries installed, you should be able to download the code from the GitHub repository and run it out of the box. If you're rebuilding the database from scratch, you’ll need to run the following line of code: sqlite3.connect(db\_path). This creates a database at the location specified by db\_path if it doesn’t already exist. Next, you’ll need to execute the SQL files within the Python environment using: cursor.executescript(open(r'SQL\_Commands\\table\_creation.sql').read())

You must do this for each SQL file to initialize all of the database tables.The data included with the project is already cleaned. However, if you're downloading the raw data directly from Kaggle, you will need to run csv\_cleaner.ipynb on each of the original data files. After that, execute each script in the Data\_population\_code/ folder, ensuring that all file paths and addresses are correctly set. At this point, the database should be fully populated. From here, you can call any of the functions from the Python files, and they should work within Main.py. Make sure you include the following after your imports:  
`connection = sqlite3.connect("nutrition.db")`  
`cursor = connection.cursor()`

And you should always end Main.py with:  
`connection.commit()`  
`connection.close()`

Proactive Planning:  
The system currently has several known issues, including SQL injection risks due to some queries using f-strings instead of parameterized queries (future mitigation in production from Flask ORM integration), performance considerations with on-demand recipe nutrition calculations (optimizable via caching for frequent queries), and data limitations such as no built-in portion size adjustments (a frontend workaround could handle scaling). Additionally, the system does not automatically check for duplicate ingredient or recipe submissions, relying instead on admin oversight during the approval process to maintain data integrity. Future improvements could include implementing duplicate detection logic, but the current design intentionally depends on manual verification to ensure accuracy while balancing development complexity. A notable design issues is that pendingIDs in approval tables (e.g., PendingRecipes, PendingIngredientItem) do not reset after items are approved or rejected, which simplifies tracking but could lead to sparse ID sequences over time. This trade-off prioritizes auditability and avoids the complexity of ID reclamation, though future iterations might address this with archival tables or reset logic for cleaner record-keeping.

*Engineering Retrospective*  
In terms of time management, I dedicated approximately five hours per week to the project. Since I worked independently, coordination with others wasn’t a concern, but I recognize that earlier disengagement from UI development, given time constraints, would have allowed me to focus more efficiently on core backend functionality. Additionally, seeking input from peers during the planning phase could have helped identify potential enhancements earlier, reducing the need for mid-project refactoring when new requirements emerged.
