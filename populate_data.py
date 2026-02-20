from app import app, db, User, Order, Payment
from Crypto.Hash import SHA256
from datetime import datetime, timedelta
import random

def hash_password(password):
    return SHA256.new(password.encode()).hexdigest()

with app.app_context():
    print("📊 Populating Imperial Network with test data...")
    
    # Get admin user
    admin = User.query.filter_by(email='admin@imperial.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@imperial.com',
            password=hash_password('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
    
    # Create test users
    test_users = [
        {'username': 'village1', 'email': 'village1@test.com', 'role': 'user'},
        {'username': 'village2', 'email': 'village2@test.com', 'role': 'user'},
        {'username': 'village3', 'email': 'village3@test.com', 'role': 'user'},
    ]
    
    for user_data in test_users:
        if not User.query.filter_by(email=user_data['email']).first():
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=hash_password('test123'),
                role=user_data['role']
            )
            db.session.add(user)
            print(f"✅ Created user: {user_data['username']}")
    
    db.session.commit()
    
    # Create test orders and payments
    users = User.query.all()
    payment_methods = ['verified_yoco', 'mobile_money', 'bank_transfer']
    
    for user in users:
        # Create 3-7 random orders per user
        for i in range(random.randint(3, 7)):
            days_ago = random.randint(0, 30)
            order_date = datetime.utcnow() - timedelta(days=days_ago)
            
            order = Order(
                order_number=f"ORD-{order_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                customer_id=user.id,
                description=f"Test order #{i+1} for {user.username}",
                amount=round(random.uniform(50, 500), 2),
                status=random.choice(['pending', 'completed', 'processing']),
                created_at=order_date
            )
            db.session.add(order)
            
            # Create payment for some orders
            if random.choice([True, False]):
                payment = Payment(
                    payment_id=f"PAY-{order_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    user_id=user.id,
                    amount=order.amount,
                    payment_method=random.choice(payment_methods),
                    status='completed',
                    created_at=order_date + timedelta(hours=random.randint(1, 24))
                )
                db.session.add(payment)
    
    db.session.commit()
    
    # Show statistics
    print("\n📈 Database Statistics:")
    print(f"   Users: {User.query.count()}")
    print(f"   Orders: {Order.query.count()}")
    print(f"   Payments: {Payment.query.count()}")
    print(f"   Total Revenue: R{db.session.query(db.func.sum(Payment.amount)).scalar() or 0:.2f}")
    print("\n✅ Test data populated successfully!")
