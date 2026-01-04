"""
Initialize Quran database with embeddings
Run this once to populate the database
"""
import asyncio
from services_quran_embeddings import QuranVectorService

async def main():
    print("=" * 60)
    print("INITIALIZING QURAN VERSE DATABASE WITH EMBEDDINGS")
    print("=" * 60)
    success = await QuranVectorService.initialize_database()
    if success:
        print("\n✓ Database initialized successfully!")
        print("The app is now ready to use semantic search!")
    else:
        print("\n✗ Database initialization failed")

if __name__ == "__main__":
    asyncio.run(main())
