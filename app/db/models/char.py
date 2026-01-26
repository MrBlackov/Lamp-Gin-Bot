from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.enum_type.char import Gender
from app.db.models.item import ItemDB

class SavingDB(Base):
    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id'))
    penny: Mapped[int] = mapped_column(default=0)

class InventoryDB(Base):
    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id'))
    items: Mapped[list[ItemDB] | None] = relationship(ItemDB, uselist=True, lazy='select', cascade='all, delete-orphan')

#class LocationDB(Base):
#    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id'))
    

class AttributePointDB(Base):
    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id'))
    strength: Mapped[int]
    dexterity: Mapped[int]
    intelligence: Mapped[int]
    health: Mapped[int]
    spirituality: Mapped[int] = mapped_column(default=0)
    speed_value: Mapped[int] = mapped_column(default=0)
    
    @property
    def speed(self):
        return (self.dexterity + self.health)/4 + self.speed_value

class ExistenceDB(Base): 
    people_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id'), default=None)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50), default='')
    gender: Mapped[Gender] = mapped_column(default=Gender.M.value)
    age: Mapped[int]
    amount_life: Mapped[int]
    saving: Mapped[SavingDB] = relationship(SavingDB, uselist=False, lazy='joined', cascade='all, delete-orphan')
    inventory: Mapped[InventoryDB] = relationship(InventoryDB, uselist=False, lazy='joined', cascade='all, delete-orphan')
    attibute_point: Mapped[AttributePointDB] = relationship(AttributePointDB, uselist=False, lazy='joined', cascade='all, delete-orphan')   
#    location: Mapped[LocationDB] = relationship(LocationDB, uselist=False, lazy='joined')  
    die: Mapped[bool] = mapped_column(default=False)
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            raise ValueError(f"This character({self.id}) hasn't first name")
        
#class NpcDB(Base):
#    exist: Mapped[ExistenceDB] = relationship(ExistenceDB, uselist=False, lazy='joined', primaryjoin="foreign(ExistenceDB.people_id) == NpcDB.id",)

class CharacterDB(Base):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('userdb.id'))
    exist: Mapped[ExistenceDB] = relationship(ExistenceDB, 
                                              uselist=False, 
                                              lazy='joined', 
                                              cascade='all, delete-orphan', primaryjoin="foreign(ExistenceDB.people_id) == CharacterDB.id")
    description: Mapped[str | None] = mapped_column(String(1000), default=None)


