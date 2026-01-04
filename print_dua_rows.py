from app.database import SessionLocal
from app.models.dua import DuaRequest
s=SessionLocal()
rows=s.query(DuaRequest).order_by(DuaRequest.id.desc()).limit(5)
for r in rows:
    print('ID:',r.id)
    print('generated_dua:',r.generated_dua)
    print('deepseek_response:',str(r.deepseek_response)[:400])
    print('---')
