import bentoml
import joblib

# Load models from local files
energy_model = joblib.load("models/GradientBoosting_SiteEnergyUse(kBtu).joblib")
ghg_model = joblib.load("models/GradientBoosting_TotalGHGEmissions.joblib")

# Save models with BentoML
bentoml.sklearn.save_model("energy_predictor_model", energy_model)
bentoml.sklearn.save_model("ghg_predictor_model", ghg_model)
