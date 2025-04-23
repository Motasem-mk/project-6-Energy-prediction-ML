# Import required libraries
import pandas as pd  # For transforming input into DataFrames
import bentoml  # For packaging and serving models
from bentoml.io import JSON  # For defining input/output types

# This ensures the user cannot send invalid values or malformed requests
from pydantic import BaseModel, confloat, conint, constr  # For validating request data
import os  # For setting local server port

# 1. Define the expected input format using Pydantic
# This ensures users can't send malformed data to the API
# Each field is type-checked and validated before it reaches the model
class BuildingData(BaseModel):
    # SiteEnergyUse(kBtu)-related features
    PropertyGFATotal: confloat(gt=0)  # Must be positive
    LargestPropertyUseType: constr(min_length=1)  # Must be a non-empty string
    ENERGYSTARScore: conint(ge=0, le=100)  # Must be between 0 and 100
    PropertyGFABuilding_s: confloat(gt=0)  # Must be positive
    ElectricityRatio: confloat(ge=0, le=1)  # Must be between 0 and 1
    SurfacePerBuilding: confloat(gt=0)  # Must be positive

    # GHGEmission-related features
    building_age: conint(ge=0) = None
    NaturalGasRatio: confloat(ge=0, le=1) = None
    SurfacePerFloor: confloat(gt=0) = None
    NumberofFloors: conint(gt=0) = None
    SteamRatio: confloat(ge=0, le=1) = None

# 2. Load trained models from BentoML model store
# Runners allow the models to be served asynchronously and efficiently
energy_model_runner = bentoml.sklearn.get("energy_predictor_model:latest").to_runner()
ghg_model_runner = bentoml.sklearn.get("ghg_predictor_model:latest").to_runner()

# 3. Define BentoML service  
svc = bentoml.Service("building_energy_service", runners=[energy_model_runner, ghg_model_runner])

# 4. Define API endpoint using decorators
# Accepts validated JSON input, returns predictions as JSON output
@svc.api(input=JSON(pydantic_model=BuildingData), output=JSON())
async def predict(input_data: BuildingData):
    # 5. Convert validated input to dictionary
    input_dict = input_data.dict()

    try:
        # 6. Prepare DataFrame for SiteEnergyUse model
        energy_df = pd.DataFrame([{
            'PropertyGFATotal': input_dict['PropertyGFATotal'],
            'LargestPropertyUseType': input_dict['LargestPropertyUseType'],
            'ENERGYSTARScore': input_dict['ENERGYSTARScore'],
            'PropertyGFABuilding(s)': input_dict['PropertyGFABuilding_s'],
            'ElectricityRatio': input_dict['ElectricityRatio'],
            'SurfacePerBuilding': input_dict['SurfacePerBuilding'],
        }])

        # 7. Prepare DataFrame for GHG model
        ghg_df = pd.DataFrame([{
            'ElectricityRatio': input_dict['ElectricityRatio'],
            'PropertyGFATotal': input_dict['PropertyGFATotal'],
            'ENERGYSTARScore': input_dict['ENERGYSTARScore'],
            'LargestPropertyUseType': input_dict['LargestPropertyUseType'],
            'PropertyGFABuilding(s)': input_dict['PropertyGFABuilding_s'],
            'SurfacePerBuilding': input_dict['SurfacePerBuilding'],
            'building_age': input_dict.get('building_age'),
            'NaturalGasRatio': input_dict.get('NaturalGasRatio'),
            'SurfacePerFloor': input_dict.get('SurfacePerFloor'),
            'NumberofFloors': input_dict.get('NumberofFloors'),
            'SteamRatio': input_dict.get('SteamRatio'),
        }])

        # 8. Run predictions asynchronously using both model runners
        energy_pred = await energy_model_runner.async_run(energy_df)
        ghg_pred = await ghg_model_runner.async_run(ghg_df)

        # 9. Return prediction results as JSON
        return {
            "predicted_SiteEnergyUse(kBtu)": energy_pred[0],
            "predicted_TotalGHGEmissions": ghg_pred[0]
        }

    # 10.Handle prediction errors gracefully
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

# 11. Local development entry point
# This allows us to run `python service.py` and test locally on http://localhost:3000
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000)) # Default port is 3000
    bentoml.serve(svc, port=port)




