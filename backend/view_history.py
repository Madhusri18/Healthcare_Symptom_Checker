from database import SessionLocal, SymptomRecord

db = SessionLocal()
records = db.query(SymptomRecord).all()

for record in records:
    print(f"ID: {record.id}")
    print(f"Symptoms: {record.symptoms}")
    print(f"Analysis: {record.analysis[:200]}...\n")  # show preview
db.close()
