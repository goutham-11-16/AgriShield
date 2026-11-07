"""
Database Initializer & Seed Script for AgriShield
Creates tables and seeds master crops and pilot reference data.
"""
import asyncio
from backend.app.db.session import engine, Base, AsyncSessionLocal
from backend.app.models.entities import Crop
from backend.app.services.crop_service import CROPS_DATABASE

async def init_database():
    print("Creating database schema...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Schema created successfully.")
    
    async with AsyncSessionLocal() as session:
        # Check if crops already seeded
        from sqlalchemy import select
        result = await session.execute(select(Crop))
        existing = result.scalars().all()
        
        if not existing:
            print("Seeding master crops for Tamil Nadu pilot...")
            for c in CROPS_DATABASE:
                crop_obj = Crop(
                    id=c["crop_id"],
                    crop_name=c["crop_name"],
                    crop_name_ta=c["crop_name_ta"],
                    category=c["category"],
                    growth_duration_days=c["duration_days"],
                    water_requirement_mm=c["water_req_mm"],
                    ideal_soil_ph_min=c["min_ph"],
                    ideal_soil_ph_max=c["max_ph"],
                    average_yield_per_acre_kg=c["avg_yield_kg_per_acre"],
                    average_cost_per_acre=c["avg_cost_per_acre"]
                )
                session.add(crop_obj)
            await session.commit()
            print("Crops seeded successfully.")
        else:
            print(f"Database already contains {len(existing)} crops.")

if __name__ == "__main__":
    asyncio.run(init_database())
