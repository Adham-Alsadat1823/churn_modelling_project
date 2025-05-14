from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from utils.inference import predict_new
from utils.config import APP_NAME, VERSION, SECRET_KEY_TOKEN
from fastapi.middleware.cors import CORSMiddleware
from utils.CustomerData import CustomerData
from utils.config import preprocessor, forest_model, xgb_model


app = FastAPI(title= APP_NAME, version= VERSION)
app.add_middleware(
    middleware_class= CORSMiddleware,
    allow_origins= ["*"],
    allow_methods= ["*"],
    allow_headers= ["*"]
)



@app.get("/", tags= ["General"])
async def home():
    return {
        "message": f"welcome to {APP_NAME} API v{VERSION}"
        }



API_KEY_HEADER = APIKeyHeader(name= "X-API-KEY")
async def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != SECRET_KEY_TOKEN:
        raise HTTPException(status_code= 401, detail= "you are not authorized to use this API")
    return api_key



@app.post("/predict/forest", tags= ["forest_prediction"])
async def predict_forest(data: CustomerData, api_key: str = Depends(verify_api_key))-> dict:
    try:
        result = predict_new(data= data, preprocessor= preprocessor, model= forest_model)
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))



@app.post("/predict/xgb", tags= ["xgb_prediction"])
async def predict_xgb(data: CustomerData, api_key: str = Depends(verify_api_key))-> dict:
    try:
        result = predict_new(data= data, preprocessor= preprocessor, model= xgb_model)
        return result
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))

