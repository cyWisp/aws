{
  "Comment" : 
    "Input should look like {'tea':'green'} with double quotes instead of single.",
  "StartAt": "MakeTea",
  "States" : {
    "MakeTea": {
      "Type": "Choice",
      "Choices": [
        {"Variable":"$.tea","StringEquals":"green","Next":"Green"},
        {"Variable":"$.tea","StringEquals":"black","Next":"Black"}
      ],
      "Default": "Error"
    },
    "Green": { "Type": "Pass", "End": true, "Result": "Green tea" },
    "Black": { "Type": "Pass", "End": true, "Result": "Black tea" },
    "Error": { "Type": "Pass", "End": true, "Result": "Bad input" }
  }
}

