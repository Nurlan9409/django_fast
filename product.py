from fastapi import APIRouter
from database import session, ENGINE
from schemas import ProductModel
from models import Product
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


session = session(bind=ENGINE)

product_router = APIRouter(prefix="/product")


@product_router.get("/")
async def product_list(status_code=status.HTTP_200_OK):
    product= session.query(Product).all()
    context = [
        {
            "id": products.id,
            "name": products.name,
        }
        for products in product
    ]

    return jsonable_encoder(context)


@product_router.post("/create")
async def create(product: ProductModel):
    check_product = session.query(Product).filter(Product.id == product.id).first()
    if check_product:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Allready exists")

    new_product = Product(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,

    )
    session.add(new_product)
    session.commit()

    return product


