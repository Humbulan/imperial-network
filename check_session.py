#!/usr/bin/env python3
from app import app
from flask import session

with app.test_client() as client:
    # Login first
    client.post('/login', data={
        'email': 'admin@imperial.com',
        'password': 'admin123'
    })
    
    # Check session
    with client.session_transaction() as sess:
        print("Session contents:")
        for key, value in sess.items():
            print(f"  {key}: {value}")
