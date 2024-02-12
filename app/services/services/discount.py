"""
Discount service.
"""
import json
from decimal import Decimal

from app.core.config import settings
from app.database.models import Dish
from app.schemas import DishScheme


class DiscountService:

    dishes_discounts: dict[str, int]  # Where {ID: %discount}

    def __init__(self):
        self.dishes_discounts = self.load_discounts()

    @staticmethod
    def load_discounts():
        if val := settings.redis.get('dishes_discounts'):
            return json.loads(val)
        else:
            return {}

    async def aggregate_prices(self, dish: Dish | DishScheme) -> Dish | DishScheme:
        if discount_percent := self.dishes_discounts.get(str(dish.id)):
            decrement = Decimal(discount_percent / 100)
            dish.price = round(dish.price - (dish.price * decrement), 2)
        return dish
