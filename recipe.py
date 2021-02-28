import spoonacular as sp
import requests
import json

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract"

querystring = {"url":"http://www.melskitchencafe.com/the-best-fudgy-brownies/"}

headers = {
    'x-rapidapi-key': "6149e1a2d1mshf54b509e116c55dp17a0bdjsn9eba0c1caa76",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
