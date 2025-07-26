from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Relationships
    products = relationship("Product", back_populates="distribution_center")
    inventory_items = relationship("InventoryItem", back_populates="distribution_center")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    state = Column(String)
    street_address = Column(String)
    postal_code = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    traffic_source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    brand = Column(String, index=True)
    retail_price = Column(Float)
    department = Column(String)
    sku = Column(String, unique=True)
    distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))
    
    # Relationships
    distribution_center = relationship("DistributionCenter", back_populates="products")
    inventory_items = relationship("InventoryItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    sold_at = Column(DateTime, nullable=True)
    cost = Column(Float)
    product_category = Column(String)
    product_name = Column(String)
    product_brand = Column(String)
    product_retail_price = Column(Float)
    product_department = Column(String)
    product_sku = Column(String)
    product_distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))
    
    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    distribution_center = relationship("DistributionCenter", back_populates="inventory_items")
    order_item = relationship("OrderItem", back_populates="inventory_item", uselist=False)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)
    gender = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    num_of_item = Column(Integer)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), unique=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    returned_at = Column(DateTime, nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    inventory_item = relationship("InventoryItem", back_populates="order_item")

class Conversation(Base):
    """Stores conversation sessions between users and the AI"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False, default="New Conversation")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """Stores individual messages within a conversation"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    content = Column(Text, nullable=False)
    is_user = Column(Boolean, default=True)  # True for user, False for AI
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
