import pandas as pd
from .CustomerData import CustomerData


def predict_new(data: CustomerData, preprocessor, model):

    ## to DF
    df= pd.DataFrame([data.dict()])

    ## transform
    data_transformed = preprocessor.transform(df)

    ## predict
    y_pred = model.predict(data_transformed)
    y_proba = model.predict_proba(data_transformed)

    ## return
    return {
        "churn_prediction": bool(y_pred[0]),
        "churn_probability": float(y_proba[0][1])
    }





