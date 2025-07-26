import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Add the project root to the Python path
project_root = str(Path(__file__).parent.absolute())
sys.path.append(project_root)

from database import Base, engine
from utils.data_loader import (
    load_distribution_centers,
    load_users,
    load_products,
    load_inventory_items,
    load_orders,
    load_order_items
)

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        return True
    except SQLAlchemyError as e:
        print(f"Error creating database tables: {e}")
        return False

def load_data(data_dir: str):
    """Load data from CSV files into the database"""
    from sqlalchemy.orm import sessionmaker
    
    # Create a new session
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        # Load data in the correct order to respect foreign key constraints
        load_functions = [
            ("distribution_centers.csv", load_distribution_centers),
            ("users.csv", load_users),
            ("products.csv", load_products),
            ("inventory_items.csv", load_inventory_items),
            ("orders.csv", load_orders),
            ("order_items.csv", load_order_items)
        ]
        
        for filename, load_func in load_functions:
            file_path = os.path.join(data_dir, filename)
            if os.path.exists(file_path):
                print(f"\nProcessing {filename}...")
                load_func(db, file_path)
            else:
                print(f"\nWarning: {file_path} not found. Skipping...")
        
        print("\nData loading completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    # Load environment variables
    load_dotenv()
    
    # Get the data directory from environment variable or use default
    data_dir = os.getenv("DATA_DIR", os.path.join(project_root, "..", "data", "raw"))
    
    print("Starting database setup and data loading...")
    print(f"Using data directory: {data_dir}")
    
    # Create tables
    if not create_tables():
        print("Exiting due to errors during table creation.")
        sys.exit(1)
    
    # Load data
    if not load_data(data_dir):
        print("Exiting due to errors during data loading.")
        sys.exit(1)
    
    print("\nDatabase setup and data loading completed successfully!")

if __name__ == "__main__":
    main()
