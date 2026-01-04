from database import SessionLocal, Base, engine
from models import Video

Base.metadata.create_all(bind=engine)
db = SessionLocal()

videos = [
    Video(title='Prayer Tips', youtube_id='video1', channel='Islamic', duration='10:00', description='Prayer guidance'),
    Video(title='Quran Study', youtube_id='video2', channel='Quran', duration='15:00', description='Quran learning'),
    Video(title='Ramadan Guide', youtube_id='video3', channel='Ramadan', duration='20:00', description='Ramadan tips'),
]

for v in videos:
    db.add(v)
    db.commit()

count = db.query(Video).count()
print(f'Videos added: {count}')
db.close()
