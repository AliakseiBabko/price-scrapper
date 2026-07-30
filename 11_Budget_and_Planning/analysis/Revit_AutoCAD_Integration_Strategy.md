# Integration Strategy: Bridging the Database with Revit & AutoCAD

You mentioned an interest in moving from cloud-based initial sketches (Homestyler) to professional local software like Revit or AutoCAD, and populating those models with the real-world material data and pricing you are collecting in your `scraper.db`.

Here is the architectural strategy for achieving this integration.

## 1. The Workflow: Homestyler -> AutoCAD -> Revit
Since you are already using 3D.homestyler.com for quick ideation, the most logical pipeline is:
1. **Homestyler (Ideation)**: Create rough sketches, determine room volumes, and get a feel for the space.
2. **AutoCAD (2D Drafting)**: Export the Homestyler project as a `.DWG` file. Open this in AutoCAD to refine exact dimensions, layer out plumbing and electrical schematics, and finalize the 2D floor plan.
3. **Revit (3D BIM & Data Integration)**: Import the refined AutoCAD `.DWG` into Revit as a base layer. Build the 3D walls, floors, and components directly on top of the DWG traces. Revit is where the true "data connection" happens.

## 2. Connecting `scraper.db` to Revit (The BIM Approach)
Revit is a Building Information Modeling (BIM) tool, meaning every 3D object (a wall, a sofa, a tile) is basically a database row with 3D geometry attached. 

To bridge your `scraper.db` with Revit, you can use **Dynamo** (Revit's built-in visual programming tool) or **pyRevit** (a Python environment for Revit).

### The Implementation Steps:
1. **Define Parameters in Revit**: Add custom Shared Parameters to your Revit project (e.g., `Actual_Price`, `Supplier_URL`, `Material_SKU`).
2. **Query the Database**: Write a Python script inside Revit (using `pyRevit` or a Dynamo Python node) that connects directly to your local `c:\Users\User\Documents\price-scrapper\scraper.db` file using the standard `sqlite3` library.
3. **Map the Data**: Match the elements in Revit to the database. For example, if you place a generic "Sofa" family in Revit, you can assign it a parameter `ItemID = 105`. The Python script queries `scraper.db` for ID 105, retrieves the exact price, manufacturer, and dimensions, and automatically updates the Revit object's parameters.
4. **Automated Schedules**: Once the data is in Revit, you can generate Revit "Schedules" (automated tables) that calculate the exact total cost of the room based on the actual 3D volumes combined with your scraped pricing data.

## 3. Connecting to AutoCAD (The 2D Approach)
If you prefer to stay in AutoCAD, you can still bridge the data, though it is slightly more manual.
1. **CSV Export**: Write a small Python script in your `price-scrapper` environment that exports relevant tables from `scraper.db` into a `.CSV` or Excel file.
2. **Data Links**: Use AutoCAD's **Data Link** feature to embed that Excel file directly onto your drawing sheets.
3. **Attribute Extraction**: You can map AutoCAD block attributes to this table, allowing you to generate Bill of Materials (BOM) directly on the blueprint.

## Next Steps
For now, continue building your material database and Wiki. Once you have your `.DWG` export from Homestyler, we can write the Python scripts required to inject your SQLite data directly into your CAD/BIM environment.
