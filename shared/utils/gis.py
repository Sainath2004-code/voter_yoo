from sqlalchemy import text
from sqlalchemy.orm import Session

class GISUtils:
    """
    Utility for geospatial queries and booth proximity indexing.
    Uses PostGIS functions via SQLAlchemy.
    """

    @staticmethod
    def find_nearest_booths(db: Session, lat: float, lng: float, limit: int = 5):
        """
        Find the nearest polling booths to a given coordinate.
        """
        query = text("""
            SELECT id, name, address, booth_no,
                   ST_Distance(location, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)) as distance
            FROM polling_booths
            ORDER BY location <-> ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)
            LIMIT :limit
        """)
        
        result = db.execute(query, {"lat": lat, "lng": lng, "limit": limit})
        return result.fetchall()

    @staticmethod
    def get_booth_coordinates(db: Session, booth_id: str):
        """
        Extract lat/lng from the geography column.
        """
        query = text("""
            SELECT ST_X(location::geometry) as lng, ST_Y(location::geometry) as lat
            FROM polling_booths
            WHERE id = :id
        """)
        return db.execute(query, {"id": booth_id}).fetchone()
