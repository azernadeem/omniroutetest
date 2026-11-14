from typing import Optional, List
from app.models.cryptocurrency import Cryptocurrency
from app.schemas.cryptocurrency import CryptocurrencyCreate

class CRUDCryptocurrency:
    def get_by_symbol(self, db, symbol: str) -> Optional[Cryptocurrency]:
        return db.query(Cryptocurrency).filter(Cryptocurrency.symbol == symbol).first()

    def create(self, db, obj_in: CryptocurrencyCreate) -> Cryptocurrency:
        db_obj = Cryptocurrency(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

cryptocurrency = CRUDCryptocurrency()