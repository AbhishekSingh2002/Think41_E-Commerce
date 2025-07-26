import pandas as pd
from sqlalchemy.orm import Session
from models.models import DistributionCenter, User, Product, InventoryItem, Order, OrderItem
from datetime import datetime

def parse_date(date_str):
    """Parse date string to datetime object"""
    if pd.isna(date_str):
        return None
    try:
        return datetime.strptime(str(date_str), '%m/%d/%Y %H:%M')
    except ValueError:
        try:
            return datetime.strptime(str(date_str), '%Y-%m-%d %H:%M:%S')
        except:
            return None

def load_distribution_centers(db: Session, file_path: str):
    """Load distribution centers data from CSV to database"""
    print("Loading distribution centers...")
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        db_dist_center = DistributionCenter(
            id=row['id'],
            name=row['name'],
            latitude=row['latitude'],
            longitude=row['longitude']
        )
        db.add(db_dist_center)
    
    db.commit()
    print(f"Loaded {len(df)} distribution centers")

def load_users(db: Session, file_path: str):
    """Load users data from CSV to database"""
    print("Loading users...")
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        db_user = User(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            age=row['age'],
            gender=row['gender'],
            state=row['state'],
            street_address=row['street_address'],
            postal_code=str(row['postal_code']),
            city=row['city'],
            country=row['country'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            traffic_source=row['traffic_source'],
            created_at=parse_date(row['created_at'])
        )
        db.add(db_user)
    
    db.commit()
    print(f"Loaded {len(df)} users")

def load_products(db: Session, file_path: str):
    """Load products data from CSV to database"""
    print("Loading products...")
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        db_product = Product(
            id=row['id'],
            name=row['name'],
            category=row['category'],
            brand=row['brand'],
            retail_price=row['retail_price'],
            department=row['department'],
            sku=row['sku'],
            distribution_center_id=row['distribution_center_id']
        )
        db.add(db_product)
    
    db.commit()
    print(f"Loaded {len(df)} products")

def load_inventory_items(db: Session, file_path: str):
    """Load inventory items data from CSV to database"""
    print("Loading inventory items...")
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        db_inv_item = InventoryItem(
            id=row['id'],
            product_id=row['product_id'],
            created_at=parse_date(row['created_at']),
            sold_at=parse_date(row['sold_at']),
            cost=row['cost'],
            product_category=row['product_category'],
            product_name=row['product_name'],
            product_brand=row['product_brand'],
            product_retail_price=row['product_retail_price'],
            product_department=row['product_department'],
            product_sku=row['product_sku'],
            product_distribution_center_id=row['product_distribution_center_id']
        )
        db.add(db_inv_item)
    
    db.commit()
    print(f"Loaded {len(df)} inventory items")

def load_orders(db: Session, file_path: str):
    """Load orders data from CSV to database"""
    print("Loading orders...")
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        db_order = Order(
            id=row['order_id'],
            user_id=row['user_id'],
            status=row['status'],
            gender=row['gender'],
            created_at=parse_date(row['created_at']),
            returned_at=parse_date(row['returned_at']),
            shipped_at=parse_date(row['shipped_at']),
            delivered_at=parse_date(row['delivered_at']),
            num_of_item=row['num_of_item']
        )
        db.add(db_order)
    
    db.commit()
    print(f"Loaded {len(df)} orders")

def load_order_items(db: Session, file_path: str):
    """Load order items data from CSV to database"""
    print("Loading order items...")
    df = pd.read_csv(file_path)
    
    for _, row in df.iterrows():
        db_order_item = OrderItem(
            id=row['id'],
            order_id=row['order_id'],
            user_id=row['user_id'],
            product_id=row['product_id'],
            inventory_item_id=row['inventory_item_id'],
            status=row['status'],
            created_at=parse_date(row['created_at']),
            shipped_at=parse_date(row['shipped_at']),
            delivered_at=parse_date(row['delivered_at']),
            returned_at=parse_date(row['returned_at'])
        )
        db.add(db_order_item)
    
    db.commit()
    print(f"Loaded {len(df)} order items")
