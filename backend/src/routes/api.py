from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from decimal import Decimal
import json

from src.utils.redis_cache import get_cache, set_cache, delete_cache
from src.models.models import Cart, User, Product, Order
from src.config import settings
from src.database import get_db
from src.rabbitmq.rabbitmq_producer import publish_message
from src.schemas import (
    CartItem, CartResponse, UserCreate, UserLogin, UserResponse,
    ProductCreate, ProductResponse, OrderCreate, OrderResponse
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Security utils
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Auth endpoints
@router.post("/register", response_model=dict, tags=["auth"])
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        is_admin=user_data.is_admin,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    publish_message("user_events", f"New user registered: {new_user.email}")
    return {
        "message": "User created successfully",
        "user": UserResponse.from_orm(new_user).dict()
    }

@router.post("/login", response_model=dict, tags=["auth"])
def login(user_data: UserLogin, db: Session = Depends(get_db), response: Response = None) -> dict:
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(
        key="token", value=access_token, httponly=True,
        max_age=7 * 24 * 60 * 60, path="/", samesite="lax", secure=False
    )
    publish_message("login_events", f"User logged in: {user.email}")
    return {
        "message": "Login successful",
        "user": UserResponse.from_orm(user).dict()
    }

@router.get("/users/me", response_model=UserResponse, tags=["auth"])
def get_current_user_profile(current_user: User = Depends(get_current_user)) -> UserResponse:
    cached_user = get_cache(f"user_profile:{current_user.id}")
    if cached_user:
        return UserResponse.parse_raw(cached_user)
    user_data = UserResponse.from_orm(current_user)
    set_cache(f"user_profile:{current_user.id}", user_data.json())
    return user_data

@router.get("/users", response_model=list[UserResponse], tags=["users"], dependencies=[Depends(admin_required)])
def get_users(db: Session = Depends(get_db)) -> list[User]:
    return db.query(User).all()

@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> UserResponse:
    cache_key = f"user:{user_id}"
    cached_user = get_cache(cache_key)
    if cached_user:
        return UserResponse.parse_raw(cached_user)
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    user_data = UserResponse.from_orm(user)
    set_cache(cache_key, user_data.json())
    return user_data

@router.post("/products", response_model=dict, tags=["products"], dependencies=[Depends(admin_required)])
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)) -> dict:
    existing_product = db.query(Product).filter(Product.name == product_data.name).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product exists")
    new_product = Product(
        name=product_data.name,
        price=Decimal(str(product_data.price)),
        description=product_data.description,
        stock=product_data.stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    delete_cache("all_products")
    publish_message("product_events", f"New product created: {new_product.name}")
    return {
        "message": "Product created",
        "product": ProductResponse.from_orm(new_product).dict()
    }

@router.get("/products", response_model=list[ProductResponse], tags=["products"])
def get_products(db: Session = Depends(get_db)) -> list[ProductResponse]:
    cached_products = get_cache("all_products")
    if cached_products:
        return [ProductResponse.parse_raw(prod) for prod in json.loads(cached_products)]
    products = db.query(Product).all()
    products_serialized = [ProductResponse.from_orm(p).json() for p in products]
    set_cache("all_products", json.dumps(products_serialized))
    return [ProductResponse.from_orm(p) for p in products]

@router.post("/orders", response_model=dict, tags=["orders"])
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    # Don't use with db.begin() as it needs explicit commit
    product = db.query(Product).with_for_update().get(order_data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < order_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    new_order = Order(
        product_id=product.id,
        user_id=current_user.id,
        quantity=order_data.quantity
    )
    
    product.stock -= order_data.quantity
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    publish_message("order_events", f"User {current_user.id} placed order for product {product.id} (qty: {order_data.quantity})")
    return {
        "message": "Order created",
        "order": OrderResponse.from_orm(new_order).dict()
    }

@router.post("/cart/add", response_model=dict, tags=["cart"])
def add_to_cart(cart_item: CartItem, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    product = db.query(Product).get(cart_item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    cart_item_db = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.product_id == cart_item.product_id
    ).first()
    
    if cart_item_db:
        cart_item_db.quantity += cart_item.quantity
    else:
        cart_item_db = Cart(
            user_id=current_user.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(cart_item_db)
    
    db.commit()
    delete_cache(f"cart:{current_user.id}")
    publish_message("cart_events", f"User {current_user.id} added product {product.id} to cart.")
    return {"message": "Product added to cart"}

@router.get("/cart", response_model=list[CartResponse], tags=["cart"])
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[CartResponse]:
    cache_key = f"cart:{current_user.id}"
    cached_cart = get_cache(cache_key)
    if cached_cart:
        return [CartResponse.parse_raw(item) for item in json.loads(cached_cart)]
    
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    serialized = [CartResponse.from_orm(item).json() for item in cart_items]
    set_cache(cache_key, json.dumps(serialized))
    return [CartResponse.from_orm(item) for item in cart_items]

@router.get("/healthy")
async def health_check() -> dict:
    return {"status": "healthy"}

@router.get("/test-redis", tags=["utils"])
async def test_redis():
    test_key = "test_key"
    test_value = "Hello from Redis!"
    
    # Try to set a value
    set_result = set_cache(test_key, test_value)
    
    # Try to get the value back
    get_result = get_cache(test_key)
    
    return {
        "set_success": set_result,
        "get_result": get_result,
        "working": get_result == test_value
    }