from pydantic import BaseModel, Field
from typing import Literal

class CustomerData(BaseModel):
    CreditScore: int = Field(description= "Credit score of the customer")
    Geography: Literal["France", "Germany", "Spain"] = Field(description= "customer's country")
    Gender: Literal["Male", "Female"] = Field(description= "customer's gender")
    Age: int = Field(description= "customer's age", ge= 18, le= 100)
    Tenure: int = Field(description= "years as a customer (0-10)", ge= 0, le= 10)
    Balance: float = Field(description= "account balance", ge= 0)
    NumOfProducts: int = Field(description= "number of bank products (1-4)", ge= 1, le= 4)
    HasCrCard: Literal[0, 1] = Field(description= "Has credit card (0-NO, 1-YES)")
    IsActiveMember: Literal[0, 1] = Field(description= "Active member status (0-NO, 1-YES)")
    EstimatedSalary: float = Field(description= "estimated annual salary")
    

