from django.shortcuts import get_object_or_404
from ninja.pagination import paginate, PageNumberPagination
from ninja import Router
from typing import List

from ..schemas.Image import ImageCreate, ImageRead
from ..schemas.Ingredient import IngredientCreate, IngredientRead
from ..schemas.Recipe import RecipeCreate, RecipeRead

from ..models import Recipe

router = Router(tags=["recipes"])

def recipe_to_schema(request, recipe):
    return RecipeRead(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        instructions=recipe.instructions,
        diet_type=recipe.diet_type,
        meal_type=recipe.meal_type,
        meal_category=recipe.meal_category,
        preparation_time=recipe.preparation_time,
        cooking_time=recipe.cooking_time,
        difficulty_level=recipe.difficulty_level,
        video_url=recipe.video_url,
        rating=recipe.rating,
        number_of_servings=recipe.number_of_servings,
        ingredients=[
            IngredientRead.from_orm(i)
            for i in recipe.ingredients.all()
        ],
        images=[
            ImageRead(
                id=i.id,
                filename=i.filename,
                content_type=i.content_type,
                size=i.size,
                url=request.build_absolute_uri(f"/api/images/{i.id}/raw/"),
                thumbnail_url=request.build_absolute_uri(f"/api/images/{i.id}/thumb/") if i.thumbnail else None,
            )
            for i in recipe.images.all()
        ]
    )


# -------------------- Recipe CRUD --------------------
@router.post("/", response=RecipeRead)
def create_recipe(request, data: RecipeCreate):
    recipe = Recipe.objects.create(**data.dict(exclude={"ingredients", "images"}))

    # Add ingredients
    for ing in data.ingredients:
        recipe.ingredients.create(**ing.dict())

    # Add images
    for img in data.images:
        recipe.images.create(**img.dict())

    # Convert nested objects for response
    recipe.ingredients.all()
    recipe.images.all()
    return recipe

@router.get("/", response=List[RecipeRead])
@paginate(PageNumberPagination)
def list_recipes(request):
    recipes = Recipe.objects.all()
    return [recipe_to_schema(request, r) for r in recipes]

@router.get("/{recipe_id}", response=RecipeRead)
def get_recipe(request, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return recipe_to_schema(request, recipe)

# why the DTO is the Create and update
@router.put("/{recipe_id}", response=RecipeRead)
def update_recipe(request, recipe_id: int, data: RecipeCreate):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    for field, value in data.dict(exlude={"ingredients","images"}).items():
        setattr(recipe, field, value)
    recipe.save()
    # optional: update or skip ingredients/images
    return recipe

@router.delete("/{recipe_id}")
def delete_recipe(request, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return {"success": True}

#related images
@router.post("/{recipe_id}/images", response=ImageRead)
def add_image(request, recipe_id: int, image: ImageCreate):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    img = recipe.images.create(**image.dict())
    return ImageRead(
        id=img.id,
        filename=img.filename,
        content_type=img.content_type,
        size=img.size,
        url=f"/api/images/{img.id}/raw/",
        thumbnail_url=f"/api/images/{img.id}/thumb/" if img.thumbnail else None,
    )

@router.get("/{recipe_id}/images", response=List[ImageRead])
def list_images_for_recipe(request, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return [
        ImageRead(
            id=img.id,
            filename=img.filename,
            content_type=img.content_type,
            size=img.size,
            url=f"/api/images/{img.id}/raw/",
            thumbnail_url=f"/api/images/{img.id}/thumb/" if img.thumbnail else None,
        )
        for img in recipe.images.all()
    ]

#related ingredients
@router.post("/{recipe_id}/ingredients", response=IngredientRead)
def add_ingredient(request, recipe_id: int, ingredient: IngredientCreate):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return recipe.ingredients.create(**ingredient.dict())

@router.get("/{recipe_id}/ingredients",response=List[IngredientRead])
def list_ingredients_for_recipe(request, recipe_id: int):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return recipe.ingredients.all()

                                                                                                                                                                                                        