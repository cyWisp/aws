{
  "StartAt": "CreateOrder",
  "States": {
    "CreateOrder": {
      "Type": "Pass",
      "Result": { 
        "Order" :  {
          "Customer" : "Alice",
          "Product" : "Coffee",
          "Billing" : { "Price": 10.0, "Quantity": 4.0 }
        }
      },
      "Next": "CalculateAmount"
    },
    "CalculateAmount": {
      "Type": "Pass",
      "Result": 40.0,
      "ResultPath": "$.Order.Billing.Amount",
      "OutputPath": "$.Order.Billing",
      "End": true
    }
  }
}

