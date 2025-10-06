from django.shortcuts import get_object_or_404
from ninja import Router
from typing import List
from ..models import Ingredient, Recipe
from ..schemas.Ingredient import IngredientCreate, IngredientRead

router = Router(tags=["ingredients"])

# Get a single ingredient
@router.get("/{ingredient_id}", response=IngredientRead)
def get_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return ingredient  # Pydantic schema will map automatically (from_attributes=True)

# List all ingredients or filter by recipe
@router.get("/", response=List[IngredientRead])
def list_ingredients(request, recipe_id: int = None):
    if recipe_id:
        ingredients = Ingredient.objects.filter(recipe_id=recipe_id)
    else:
        ingredients = Ingredient.objects.all()
    return ingredients

# Create a new ingredient for a recipe
@router.post("/recipes/{recipe_id}", response=IngredientRead)
def create_ingredient(request, recipe_id: int, data: IngredientCreate):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredient = Ingredient.objects.create(recipe=recipe, **data.dict())
    return ingredient

# Update an existing ingredient
@router.put("/{ingredient_id}", response=IngredientRead)
def update_ingredient(request, ingredient_id: int, data: IngredientCreate):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    for field, value in data.dict().items():
        setattr(ingredient, field, value)
    ingredient.save()
    return ingredient

# Delete an ingredient
@router.delete("/{ingredient_id}")
def delete_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    ingredient.delete()
    return {"success": True}

