import spoonacular as sp
import requests
import json

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract"

querystring = {"url":"http://www.melskitchencafe.com/the-best-fudgy-brownies/"}

headers = {
    'x-rapidapi-key': "YOUR API KEY HERE",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()
print(data['title'])
#print(data['summary'])
#print(response.text)
