# project-6-Energy-prediction-ML

---


# 🔋 Seattle Building Energy & Emissions Prediction

This machine learning project predicts **site energy use** and **greenhouse gas (GHG) emissions** for **non-residential buildings** in Seattle. The goal is to support Seattle’s **2050 carbon neutrality plan** by identifying high-emission buildings using data-driven methods. The final model is deployed as a **REST API** using **BentoML** and **Google Cloud Run**.

---

## 📌 Project Overview

- **Client**: City of Seattle  
- **Dataset**: 2016 Seattle Building Energy Benchmarking  
- **Targets**:  
  - `SiteEnergyUse(kBtu)`  
  - `TotalGHGEmissions`
- **Key Feature Studied**: `ENERGYSTARScore`
- **Final Output**: An optimized model and cloud-deployed API

---

## 🎯 Objectives

- Predict energy consumption and emissions using building characteristics.
- Evaluate if `ENERGYSTARScore` improves prediction accuracy.
- Build a lightweight model suitable for production API.
- Reduce reliance on costly physical audits.

---

## 🧠 Machine Learning Models

| Model              | Type        | Used in |
|-------------------|-------------|---------|
| Linear Regression | Linear      | Baseline |
| Ridge Regression  | Linear + Regularization | Comparison |
| Decision Tree     | Non-linear  | Baseline |
| Random Forest     | Ensemble (Bagging) | Comparison |
| Gradient Boosting | Ensemble (Boosting) | ✅ Final model |

- Feature Engineering: Ratios (ElectricityRatio, SurfacePerFloor, etc.), `building_age`
- Log-Transformation: Applied to targets to reduce skew and improve stability
- Model Selection: Based on **R², RMSE, MAE, MAPE**
- Hyperparameter Tuning: Done using **GridSearchCV**

---

## ✅ Final Model

```text
Model: GradientBoostingRegressor (Log Transformed + Top Features)
R²:     0.85  
MAPE:   26.5%  
Features: PropertyGFATotal, ENERGYSTARScore, ElectricityRatio, etc.
```

---

## 🧰 Tech Stack

| Category        | Tools/Technologies            |
|----------------|-------------------------------|
| Language       | Python 3.10                    |
| ML Libraries   | scikit-learn, pandas, NumPy    |
| Visualization  | seaborn, matplotlib            |
| API Framework  | BentoML                        |
| Deployment     | Docker, Google Cloud Run       |
| Validation     | Pydantic                       |

---

## 🚀 Deployment Overview

This project includes a complete deployment pipeline:

1. **Trained ML model** saved with BentoML
2. **API logic** created using `service.py` with validation
3. **Containerized** with Docker using `bentofile.yaml`
4. **Deployed** to the cloud using **Google Cloud Run**

🔗 **Live Demo (API endpoint)**:  
[https://building-energy-api-752730965616.europe-west1.run.app](https://building-energy-api-752730965616.europe-west1.run.app)

📘 Swagger UI: `http://localhost:3000` (when served locally)

---

## 🧪 API Usage

### ✅ Valid Input Example

```json
{
  "PropertyGFATotal": 25000,
  "LargestPropertyUseType": "Office",
  "ENERGYSTARScore": 75,
  "PropertyGFABuilding_s": 20000,
  "ElectricityRatio": 0.6,
  "SurfacePerBuilding": 18000,
  "building_age": 25,
  "NaturalGasRatio": 0.2,
  "SurfacePerFloor": 6000,
  "NumberofFloors": 3,
  "SteamRatio": 0.1
}
```

### ❌ Invalid Input Triggers Validation Errors

```json
{
  "PropertyGFATotal": "twenty five thousand",
  "ENERGYSTARScore": "high",
  "NumberofFloors": "three",
  ...
}
```

BentoML returns `400 Bad Request` with clear validation error messages.

---

## 📁 Project Structure

```
seattle-building-energy-prediction/
├── notebooks/              # Jupyter Notebooks
│   └── modeling.ipynb
│
├── api/                    # API codebase
│   ├── service.py
│   └── bentofile.yaml
│
├── reports/                # Presentation slides, charts
│   └── slides.pdf
│
├── models/                 # Saved models via BentoML
├── data/                   # Cleaned dataset sample (if public)
├── requirements.txt        # Dependencies
├── README.md
└── .gitignore
```

---

## 📊 Key Insights

- Larger buildings → higher energy consumption and emissions.
- Property types like Hospitals and Data Centers emit the most.
- ENERGYSTARScore shows strong negative correlation with both targets.
- Removing ENERGYSTARScore caused ~14% increase in model error.
- Feature engineering (ratios + age) improved model performance.
- Top features were used to retrain a smaller, more accurate model.

---

## 📦 Installation

```bash
git clone https://github.com/your-username/seattle-building-energy-prediction.git
cd seattle-building-energy-prediction
pip install -r requirements.txt
```

To run the API locally:
```bash
python api/service.py
# Visit: http://localhost:3000
```

---

## 📝 Author

- 👨‍💻 Motasem 
- 🌐 
- 📧 motasemmkamz@gmail.com

---

## 📜 License

MIT License. Free to use, modify, and distribute.

---
```

---

Would you also like me to generate the `requirements.txt` and `bentofile.yaml` templates so you can push those to your repo too?
