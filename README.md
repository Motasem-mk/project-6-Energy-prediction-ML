# Project 6 — Building Energy Consumption Prediction

## Project Overview

This project was completed as part of the **OpenClassrooms Data Engineer path**.

The objective is to predict the energy consumption and greenhouse gas emissions of non-residential buildings in Seattle.

The project uses the **Seattle 2016 Building Energy Benchmarking dataset** and focuses on two prediction targets:

* `SiteEnergyUse(kBtu)` — total energy consumption;
* `TotalGHGEmissions` — greenhouse gas emissions.

The project also evaluates whether `ENERGYSTARScore` is useful for prediction and whether the city should continue collecting it.

---

## Business Context

The City of Seattle aims to become carbon neutral by 2050.

Energy audits are expensive, so the goal is to build machine learning models that can estimate energy consumption and CO₂ emissions using building characteristics such as:

* building size;
* building use type;
* construction year;
* number of floors;
* surface ratios;
* energy source ratios;
* ENERGY STAR score.

The final model is exposed through an API prototype using BentoML, allowing users to send building information and receive predictions in real time.

---

## Repository Structure

```text
.
├── README.md
├── 1_Analysis_Cleaning_EDA_21_04_2025.ipynb
├── 2_Modeling1_SiteEnergyUse(kBtu)_21_04_2025.ipynb
├── 3_Modeling2_TotalGHGEmissions_21_04_2025.ipynb
├── 4_Modeling3_TotalGHGEmissions-WitouthEnergyScore_21_04_2025.ipynb
├── 2016_Building_Energy_Benchmarking.csv
├── building_data_modelling.csv
├── save_models.py
├── service.py
├── bentofile.yaml
├── requirements.txt
└── presentation/
    └── Abualqumboz_5_project_6_Energy_Prediction.pptx
```

---

## Main Project Steps

### 1. Exploratory Data Analysis

The first notebook focuses on data exploration and cleaning.

Main steps:

* loading the Seattle building energy dataset;
* filtering non-residential buildings;
* removing irrelevant or highly missing columns;
* handling missing values;
* removing non-compliant records;
* analyzing target distributions;
* detecting and removing outliers;
* studying relationships between building characteristics, energy use and GHG emissions.

---

### 2. Feature Engineering

Several new features were created to improve model performance:

* `SteamRatio`;
* `ElectricityRatio`;
* `NaturalGasRatio`;
* `SurfacePerBuilding`;
* `SurfacePerFloor`;
* `ParkingRatio`;
* `BuildingRatio`;
* `building_age`.

The project avoids data leakage by not using direct energy consumption variables that would only be known after measuring the target.

---

### 3. Energy Consumption Modeling

The second notebook focuses on predicting:

```text
SiteEnergyUse(kBtu)
```

Several supervised regression models were tested:

* Linear Regression;
* Ridge Regression;
* Decision Tree;
* Random Forest;
* Gradient Boosting Regressor.

The final selected approach uses:

* log transformation of the target;
* top feature selection;
* Gradient Boosting Regressor;
* hyperparameter tuning with GridSearchCV.

The final model achieved strong performance, with the tuned Gradient Boosting model giving the best results.

---

### 4. GHG Emissions Modeling

The third notebook focuses on predicting:

```text
TotalGHGEmissions
```

The modeling approach is similar:

* feature engineering;
* log transformation of the target;
* model comparison;
* Gradient Boosting Regressor;
* hyperparameter tuning;
* top feature selection.

The project also tests the impact of removing `ENERGYSTARScore` from the model.

The results show that removing `ENERGYSTARScore` reduces model performance, which supports the recommendation that Seattle should continue collecting and using this variable.

---

### 5. API Deployment with BentoML

The second part of the project exposes the trained model through an API using BentoML.

Main files:

| File               | Description                                             |
| ------------------ | ------------------------------------------------------- |
| `save_models.py`   | Saves the trained models into the BentoML model store   |
| `service.py`       | Defines the BentoML API service and prediction endpoint |
| `bentofile.yaml`   | Defines the BentoML build and deployment configuration  |
| `requirements.txt` | Lists the required Python dependencies                  |

The API accepts building characteristics as input and returns predictions for:

* energy consumption;
* greenhouse gas emissions.

---

## Input Validation

The API uses Pydantic to validate input data.

This prevents users from sending incoherent values, such as:

* text values instead of numeric values;
* invalid ENERGY STAR scores;
* invalid building age;
* invalid number of floors.

If invalid data is sent, the API rejects the request with a clear validation error.

---

## Local API Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Save the models

```bash
python save_models.py
```

### 3. Serve the API locally

```bash
bentoml serve service:svc
```

### 4. Open Swagger UI

```text
http://localhost:3000
```

Swagger UI can be used to test the prediction endpoint directly from the browser.

---

## Example API Input

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

## Example API Response

```json
{
  "predicted_SiteEnergyUse(kBtu)": 13.82921000250296,
  "predicted_TotalGHGEmissions": 3.613707555306789
}
```

---

## BentoML Build and Docker Containerization

The Bento service can be built with:

```bash
bentoml build
```

Then containerized with:

```bash
bentoml containerize building_energy_service:<bento_tag>
```

The Docker image contains:

* the BentoML service;
* the saved ML models;
* the Python dependencies;
* the API logic;
* the input validation logic.

---

## Cloud Deployment

The project was tested for deployment on **Google Cloud Run**.

The general deployment workflow is:

1. build the BentoML service;
2. containerize the service with Docker;
3. tag the Docker image;
4. push the image to Google Container Registry;
5. deploy the image to Cloud Run;
6. test the deployed API through HTTPS and Swagger UI.

The live endpoint may no longer be active in order to avoid unnecessary cloud costs.

---

## Main Results

### Energy consumption prediction

The best model for `SiteEnergyUse(kBtu)` was:

```text
Gradient Boosting Regressor with log target, top features and hyperparameter tuning
```

Key selected features included:

* `PropertyGFATotal`;
* `LargestPropertyUseType`;
* `ENERGYSTARScore`;
* `PropertyGFABuilding_s`;
* `ElectricityRatio`;
* `SurfacePerBuilding`.

### GHG emissions prediction

The best model for `TotalGHGEmissions` was also based on:

```text
Gradient Boosting Regressor with log target, top features and hyperparameter tuning
```

The analysis showed that `ENERGYSTARScore` has a strong impact on prediction quality.

---

## Recommendation

Seattle should continue collecting and using `ENERGYSTARScore`.

This variable improves prediction performance and captures energy-efficiency information that is not fully represented by other structural building features.

---

## Technologies Used

* Python
* Pandas
* NumPy
* scikit-learn
* Matplotlib
* Seaborn
* Jupyter Notebook
* GradientBoostingRegressor
* GridSearchCV
* BentoML
* Pydantic
* Docker
* Google Cloud Run

---

## Project Deliverables

This repository contains:

* exploratory data analysis notebook;
* energy consumption modeling notebook;
* GHG emissions modeling notebook;
* GHG emissions modeling without `ENERGYSTARScore`;
* trained model saving script;
* BentoML API service;
* BentoML deployment configuration;
* project presentation;
* datasets used for modeling.

---

## Author

Motasem Abualqumboz

Data Engineer 
