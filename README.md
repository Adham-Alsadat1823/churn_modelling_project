# Churn Detection API

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A machine learning-powered API for predicting customer churn using Random Forest and XGBoost models. The project leverages a dataset (`Churn_Modelling.csv`) to train models that predict whether a customer is likely to churn based on their attributes. The API is built with FastAPI, ensuring high performance and easy integration.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Churn Detection API is designed to predict customer churn for a banking institution. It uses machine learning models trained on historical customer data to provide predictions and probabilities of churn. The API supports two models: Random Forest and XGBoost, both tuned for optimal performance using RandomizedSearchCV. The project includes data preprocessing, exploratory data analysis (EDA), model training, and a FastAPI-based inference endpoint for real-time predictions.

## Features

- **Machine Learning Models**: Tuned Random Forest and XGBoost classifiers for churn prediction.
- **Data Preprocessing**: Handles categorical encoding, scaling, and imbalance using SMOTE and RandomUnderSampler.
- **FastAPI Integration**: High-performance API with CORS support and API key authentication.
- **Input Validation**: Uses Pydantic for robust input validation of customer data.
- **Comprehensive EDA**: Includes univariate and bivariate visualizations for data insights.
- **Modular Codebase**: Organized structure with separate modules for configuration, inference, and data models.

## Dataset

The dataset (`dataset/Churn_Modelling.csv`) contains customer information with the following features:

- **CreditScore**: Customer's credit score (integer).
- **Geography**: Customer's country (France, Germany, Spain).
- **Gender**: Customer's gender (Male, Female).
- **Age**: Customer's age (integer, 18-100).
- **Tenure**: Years as a customer (integer, 0-10).
- **Balance**: Account balance (float, >= 0).
- **NumOfProducts**: Number of bank products (integer, 1-4).
- **HasCrCard**: Has credit card (0-No, 1-Yes).
- **IsActiveMember**: Active member status (0-No, 1-Yes).
- **EstimatedSalary**: Estimated annual salary (float).
- **Exited**: Target variable indicating churn (0-No, 1-Yes).

The dataset has 10,000 entries with no missing values. The target variable (`Exited`) is imbalanced, with approximately 20.37% churn cases.

## Installation

### Prerequisites

- Python 3.12
- pip package manager
- Git (optional, for cloning the repository)

### Steps

1. **Clone the Repository** (or download the source code):
   ```bash
   git clone https://github.com/your-username/churn-detection-api.git
   cd churn-detection-api
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update the `.env` file with your `SECRET_KEY_TOKEN` (a secure API key).

5. **Verify Pretrained Models**:
   - Ensure the `models/` directory contains `preprocessor.pkl`, `forest_tuned.pkl`, and `xgb_tuned.pkl`. These are loaded in `utils/config.py`.

6. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## Usage

### Running the API

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Access the interactive API documentation at `http://127.0.0.1:8000/docs` to test endpoints.

### Making Predictions

Use the `/predict/forest` or `/predict/xgb` endpoints with a valid API key. Example request using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/predict/xgb" \
-H "X-API-KEY: ac2e2f592424c11d77c8e72dd2380e0d" \
-H "Content-Type: application/json" \
-d '{
  "CreditScore": 619,
  "Geography": "France",
  "Gender": "Female",
  "Age": 42,
  "Tenure": 2,
  "Balance": 0.0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 101348.88
}'
```

**Response**:
```json
{
  "churn_prediction": true,
  "churn_probability": 0.78
}
```

### Training Models

To retrain models, run the Jupyter notebook (`notebooks/notebook.ipynb`):
1. Ensure the dataset (`dataset/Churn_Modelling.csv`) is present.
2. Open the notebook in Jupyter:
   ```bash
   jupyter notebook notebooks/notebook.ipynb
   ```
3. Execute all cells to preprocess data, perform EDA, train models, and save them to the `models/` directory.

## API Endpoints

| Endpoint             | Method | Description                              | Authentication |
|----------------------|--------|------------------------------------------|---------------|
| `/`                  | GET    | Welcome message                          | None          |
| `/predict/forest`    | POST   | Predict churn using Random Forest        | API Key       |
| `/predict/xgb`       | POST   | Predict churn using XGBoost              | API Key       |

### Request Body (for `/predict/*`)

```json
{
  "CreditScore": int,
  "Geography": "France" | "Germany" | "Spain",
  "Gender": "Male" | "Female",
  "Age": int,
  "Tenure": int,
  "Balance": float,
  "NumOfProducts": int,
  "HasCrCard": 0 | 1,
  "IsActiveMember": 0 | 1,
  "EstimatedSalary": float
}
```

### Authentication

Include the `X-API-KEY` header with the value from the `.env` file (`SECRET_KEY_TOKEN`).

## Model Details

### Preprocessing
- **Categorical Features**: `Geography` and `Gender` are one-hot encoded.
- **Numerical Features**: Scaled using `StandardScaler`.
- **Imbalanced Data**: Handled using SMOTE for oversampling and RandomUnderSampler for undersampling.
- **Pipeline**: Combines preprocessing steps using `ColumnTransformer` and `Pipeline`.

### Models
- **Random Forest**:
  - Tuned using RandomizedSearchCV.
  - Saved as `models/forest_tuned.pkl`.
- **XGBoost**:
  - Tuned with parameters: `n_estimators`, `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`, `min_child_weight`.
  - Best F1-score: 0.631 (test), 0.861 (train).
  - Saved as `models/xgb_tuned.pkl`.

### Performance
- **XGBoost**:
  - Train F1-score: 0.861
  - Test F1-score: 0.631
- **Random Forest**: Performance metrics available in `notebooks/notebook.ipynb`.

## Project Structure

```
churn-detection-api/
├── dataset/
│   └── Churn_Modelling.csv
├── models/
│   ├── forest_tuned.pkl
│   ├── preprocessor.pkl
│   └── xgb_tuned.pkl
├── notebooks/
│   └── notebook.ipynb
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── CustomerData.py
│   ├── inference.py
│   └── __pycache__/
│       ├── config.cpython-312.pyc
│       ├── CustomerData.cpython-312.pyc
│       ├── inference.cpython-312.pyc
│       └── __init__.cpython-312.pyc
├── __pycache__/
│   └── main.cpython-312.pyc
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

### Notes on Structure
- **dataset/**: Contains the `Churn_Modelling.csv` file used for training and analysis.
- **models/**: Stores pretrained model files (`preprocessor.pkl`, `forest_tuned.pkl`, `xgb_tuned.pkl`).
- **notebooks/**: Contains the Jupyter notebook (`notebook.ipynb`) for EDA, preprocessing, and model training.
- **utils/**: Houses utility modules for configuration, data validation, and inference logic.
- **__pycache__/**: Automatically generated Python bytecode files, which can be ignored in version control.
- **.gitignore**: Ensures temporary files (e.g., `__pycache__`, `.env`) are excluded from version control.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure your code follows PEP 8 guidelines and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.