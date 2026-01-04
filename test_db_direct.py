#!/usr/bin/env python3
"""Direct database test without API"""

import sys
sys.path.insert(0, '/c/Users/cheeh/Desktop/webservice ramadan')

from app.database import SessionLocal, engine
from app.models.imam import Imam, Consultation, Base

# Create tables
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created!")

# Test adding an imam directly to database
print("\nAdding test imam to database...")
db = SessionLocal()
try:
    # Create new imam
    new_imam = Imam(
        name="Test Imam",
        specializations="general,fiqh",
        email="test@example.com",
        consultation_methods="phone",
        languages="English,Arabic"
    )
    db.add(new_imam)
    db.commit()
    db.refresh(new_imam)
    print(f"SUCCESS: Added imam with ID {new_imam.id}")
    
    # Query back
    imams = db.query(Imam).all()
    print(f"Total imams in DB: {len(imams)}")
    for imam in imams:
        print(f"  - ID {imam.id}: {imam.name}")
        
finally:
    db.close()

print("\nDone!")
