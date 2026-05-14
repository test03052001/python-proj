from sqlalchemy.orm import Session

from app.models import Product
from app.repositories.categories import CategoryRepository
from app.repositories.products import ProductRepository
from app.schemas.products import ProductCreate, ProductUpdate
from app.services.exceptions import ConflictError, NotFoundError


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.products = ProductRepository(db)
        self.categories = CategoryRepository(db)

    def list_products(
        self,
        offset: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> list[Product]:
        return self.products.list(offset=offset, limit=limit, active_only=active_only)

    def get_product(self, product_id: int) -> Product:
        product = self.products.get(product_id)
        if product is None:
            raise NotFoundError("Product not found")
        return product

    def create_product(self, payload: ProductCreate) -> Product:
        if self.products.get_by_sku(payload.sku):
            raise ConflictError("A product with this SKU already exists")
        if self.categories.get(payload.category_id) is None:
            raise NotFoundError("Category not found")

        product = Product(**payload.model_dump())
        self.products.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product_id: int, payload: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        changes = payload.model_dump(exclude_unset=True)

        if "category_id" in changes and self.categories.get(changes["category_id"]) is None:
            raise NotFoundError("Category not found")

        for field, value in changes.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product
