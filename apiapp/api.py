from ninja import NinjaAPI
from .endpoints.recipes import router as recipe_router
from .endpoints.ingredients import router as ingredient_router
from .endpoints.images import router as image_router

api = NinjaAPI()

api.add_router("/recipes/", recipe_router)
api.add_router("/ingredients/", ingredient_router)
api.add_router("/images/", image_router)
