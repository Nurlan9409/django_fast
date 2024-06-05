from fastapi import APIRouter
from database import session, ENGINE
from schemas import ProductModel
from models import Product,Category
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
            'price':product.price
        }
        for products in product
    ]

    return jsonable_encoder(context)


@product_router.post("/create")
async def create(product: ProductModel):
    check_product_id = session.query(Product).filter(Product.id == product.id).first()
    check_category_id = session.query(Category).filter(Category.id == product.id).first()
    if check_product_id :
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Allready exists")
    elif check_category_id is not None :
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
    data = {
        "code": status.HTTP_201_CREATED,
        "message": "Product created",
        "data": jsonable_encoder(new_product)
    }

    return jsonable_encoder(data)


@product_router.get("/{product_id}")
async def get_product(product_id):
    check_product_id = session.query(Product).filter(Product.id == product_id).first()
    if check_product_id :
        data={
            "succes": True,
            "code": 200,
            "msg": "success",
            "data":{
                "id": check_product_id.id,
                "name": check_product_id.name,
                "description": check_product_id.description,
                "price": check_product_id.price,
                "category":{
                    "id": check_product_id.category_id,
                    "name": check_product_id.category.name,
                },
            },
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

@product_router.delete("/{product_id}")
async def delete_product(product_id):
    check_product_id = session.query(Product).filter(Product.id == product_id).first()
    if check_product_id :
        session.delete(check_product_id)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
