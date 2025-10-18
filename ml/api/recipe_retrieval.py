from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  
app = FastAPI()


SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY") 
BASE_URL = "https://api.spoonacular.com/recipes"


class IngredientsRequest(BaseModel):
    ingredients: list[str]

'''
на вход принимает список продуктов 
{
  "ingredients": [
    "tomato", "meat", "carrot"
  ]
}

на выход дает:
-айди рецепта в базе Spoonacular
Можно использовать потом, чтобы запросить подробную информацию об этом блюде через другой ендпоинт
- Название блюда
- Ссылка на фото блюда
- Список всех ингредиентов, которые нужны для приготовления.
- Пошаговое описание приготовления 
- Сколько времени занимает готовка
- Сколько порций получится

 {
      "id": 639632,
      "title": "Classic Ragu",
      "image": "https://img.spoonacular.com/recipes/639632-556x370.jpg",
      "ingredients": [
        "1 1/2 pounds peeled, seeded, pureed fresh tomatoes or 1 large can of peeled tomatoes",
        "1 small carrot, finely diced",
        "1 rib of celery, finely diced",
        "cooked tagliatelle",
        "1 clove of garlic",
        "1/4 lb ground sausage",
        "1/2 lb ground veal",
        "olive oil",
        "1 medium onion, finely diced",
        "salt & pepper"
      ],
      "instructions": "<ol><li>In a pot add a couple glugs of olive oil &amp; saut clove of garlic until brown then discard.</li><li>On medium heat saut veggies slowly for about 10 minutes - so they are not brown but translucent.</li><li>Raise the heat slightly &amp; add in meat - breaking up the pieces with a wooden spoon.</li><li>Season with salt &amp; pepper.</li><li>Add tomatoes &amp; half a glass of water.</li><li>Bring up to boil.</li><li>Lower to a very low simmer for 2.5 hours stirring occasionally.</li><li>Toss with your favorite pasta.</li><li>If sauce becomes too thick, add a little pasta water.</li></ol>",
      "readyInMinutes": 180,
      "servings": 6
    }
        
'''

@app.post("/recipes")
async def get_recipes(data: IngredientsRequest, number: int = Query(3, ge=1, le=20)):
    params = {
        "ingredients": ",".join(data.ingredients),
        "number": number,
        "apiKey": SPOONACULAR_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/findByIngredients", params=params)
        response.raise_for_status()
        recipes_data = response.json()

        if not recipes_data:
            raise HTTPException(status_code=404, detail="Рецепты не найдены")

        recipes = []
        for recipe in recipes_data:
            recipe_id = recipe["id"]
            detail_params = {"apiKey": SPOONACULAR_API_KEY}
            detail_response = await client.get(f"{BASE_URL}/{recipe_id}/information", params=detail_params)
            detail_response.raise_for_status()
            detail = detail_response.json()

            recipes.append({
                "id": recipe_id,
                "title": detail["title"],
                "image": detail["image"],
                "ingredients": [ing["original"] for ing in detail["extendedIngredients"]],
                "instructions": detail.get("instructions") or "Инструкции отсутствуют",
                "readyInMinutes": detail.get("readyInMinutes"),
                "servings": detail.get("servings")
            })

    return {"recipes": recipes}

