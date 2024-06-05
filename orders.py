from models import Order, User, Product
from schemas import OrderModel
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from database import session, ENGINE

session = session(bind=ENGINE)


order_router = APIRouter(prefix="/orders")

@order_router.get('/')
async def orders():
    orders = session.query(Order).all()
    context = [
        {
            "id": order.id,
            "user_id":
                {
                "id": order.user_id,
               'first_name':order.user.first_name,
                'last_name':order.user.last_name,
                'username':order.user.username,
                'email':order.user.email,
                'is_staff':order.user.is_staff,
                'is_active':order.user.is_active,
                },
            "product_id": {
                'id':order.product_id,
                'name':order.product.name,
                'category':{
                    'id':order.product.category.id,
                    'name':order.product.category.name,
                }
            },
        }
        for order in orders
    ]
    return jsonable_encoder(context)

# @order_router.post("/create")


@order_router.post('/create')
async def create(order: OrderModel):
    check_order = session.query(Order).filter(Order.id == order.id).first()
    check_user_id = session.query(User).filter(User.id == order.user_id).first()
    check_product_id = session.query(Product).filter(Product.id == order.product_id).first()

    if check_order:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already exis")

    elif check_user_id and check_product_id:
        new_order = Order(
            id=order.id,
            user_id=order.user_id,
            product_id=order.product_id,
            count=order.count,
            order_status=order.order_status
        )
        session.add(new_order)
        session.commit()
        data = {
            "code": 201,
            "msg": "success"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id or product_id allr exis")



@order_router.get('/id')
async def get_order_id(id:int):
    check_order = session.query(Order).filter(Order.id == id).first()
    if check_order:
        data = {
            "succes":True,
            "code":200,
            "msg":"success",
            "data":{
            'id':check_order.id,
            'user':{
                id:check_order.user_id,
                'first_name':check_order.user.first_name,
                'last_name':check_order.user.last_name,
                'username':check_order.user.username,
                'price':check_order.price,
                'email':check_order.user.email,
                'is_staff':check_order.user.is_staff,
                'is_active':check_order.user.is_active,
            },
                'product':{
                    'id':check_order.product_id,
                    'name':check_order.product.name,
                    'proce':check_order.product.proce,
                    'category':{
                        'id':check_order.product.category.id,
                        'name':check_order.product.category.name
                    },
                },
                'count':check_order.count,
                'status':check_order.order_status,
                'total':check_order.product.price*check_order.count,
                'promocode':(check_order.product.price*check_order.count)*0.9,
        },
        },
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id allready exis")

@order_router.delete("/delete")
async def delete_order(id:int):
    check_order = session.query(Order).filter(Order.id == id).first()
    if check_order:
        session.delete(check_order)
        session.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)