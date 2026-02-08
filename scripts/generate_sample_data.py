"""
Sample data generation script for ChurnGuard AI
Creates synthetic customer and transaction data for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.database_models import Customer, Transaction


def generate_sample_data(num_customers=100):
    """Generate sample customers and transactions"""
    db = SessionLocal()
    
    try:
        print(f"Generating {num_customers} sample customers...")
        
        first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", 
                      "Tom", "Anna", "James", "Emma", "Robert", "Olivia", "William"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                     "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson"]
        
        customers = []
        for i in range(num_customers):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            
            # Create customer with random metrics
            customer = Customer(
                external_id=f"CUST-{1000+i}",
                email=email,
                name=name,
                total_orders=random.randint(1, 50),
                total_spent=round(random.uniform(50, 5000), 2),
                avg_order_value=round(random.uniform(20, 500), 2),
                days_since_last_order=random.randint(0, 365),
                order_frequency=round(random.uniform(0.1, 10), 2),
                email_open_rate=round(random.uniform(0, 1), 2),
                email_click_rate=round(random.uniform(0, 0.5), 2),
                sms_engagement_rate=round(random.uniform(0, 1), 2),
                app_sessions=random.randint(0, 100)
            )
            
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        print(f"Created {num_customers} customers")
        
        # Generate transactions for some customers
        print("Generating sample transactions...")
        transaction_count = 0
        
        for customer in customers[:50]:  # Generate transactions for first 50 customers
            num_transactions = random.randint(1, 10)
            
            for j in range(num_transactions):
                days_ago = random.randint(1, 365)
                transaction_date = datetime.utcnow() - timedelta(days=days_ago)
                
                transaction = Transaction(
                    customer_id=customer.id,
                    external_id=f"TXN-{transaction_count+1000}",
                    amount=round(random.uniform(20, 500), 2),
                    items_count=random.randint(1, 10),
                    discount_amount=round(random.uniform(0, 50), 2),
                    transaction_date=transaction_date,
                    status="completed"
                )
                
                db.add(transaction)
                transaction_count += 1
        
        db.commit()
        print(f"Created {transaction_count} transactions")
        print("Sample data generation complete!")
        
    except Exception as e:
        print(f"Error generating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    generate_sample_data(100)
