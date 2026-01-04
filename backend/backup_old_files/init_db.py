from database import SessionLocal, Base, engine
from models import Video

# Create fresh tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Add videos
db = SessionLocal()
videos = [
    Video(title='Prayer Tips',youtube_id='vid1',channel='Islamic',duration='10:00',description='Prayer guide',thumbnail_url='https://img.youtube.com/vi/vid1/max.jpg'),
    Video(title='Quran Study',youtube_id='vid2',channel='Quran',duration='15:00',description='Quran study',thumbnail_url='https://img.youtube.com/vi/vid2/max.jpg'),
    Video(title='Ramadan Guide',youtube_id='vid3',channel='Ramadan',duration='20:00',description='Ramadan tips',thumbnail_url='https://img.youtube.com/vi/vid3/max.jpg'),
]
for v in videos:
    db.add(v)
db.commit()
print('OK')
db.close()
