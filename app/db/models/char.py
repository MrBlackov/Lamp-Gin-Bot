from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.enum_type.char import Gender
from app.db.models.item import ItemDB, KitDB, SkillDB
from app.db.models.map import LocationDB

class InventoryDB(Base):
    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id', ondelete='CASCADE'))
    exist: Mapped['ExistenceDB'] = relationship('ExistenceDB', uselist=False, lazy='select', cascade='all', back_populates='inventory')
    kit: Mapped[list[KitDB] | None] = relationship(KitDB, uselist=True, lazy='select', cascade='all, delete-orphan')
    items: Mapped[list[ItemDB] | None] = relationship(ItemDB, uselist=True, lazy='select', cascade='all, delete-orphan')

#class LocationDB(Base):
#    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id'))
    

class AttributePointDB(Base):
    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id', ondelete='CASCADE'))    
    exist: Mapped['ExistenceDB'] = relationship('ExistenceDB', uselist=False, lazy='select', cascade='all', back_populates='attibute_point')
    strength: Mapped[int] = mapped_column(default=0) # Сила
    dexterity: Mapped[int] = mapped_column(default=0) # Ловкость
    intelligence: Mapped[int] = mapped_column(default=0) # Интелект
    health: Mapped[int] = mapped_column(default=0) # Здоровье
    spirituality: Mapped[int] = mapped_column(default=0)
    speed_value: Mapped[int] = mapped_column(default=0)
    
    def add_skills(self, skills: list[SkillDB] | None):
        if skills:
            self.skill_tags = {skill.sketch_tag:skill for skill in skills} if skills else {}
            self.skills = [self.add_level(skill) for skill in skills] if skills else []
        return self

    def add_level(self, skill: SkillDB):
        formula = skill.sketch.level_formula
        if formula:
            if len(formula) > 0:
                if skill.sketch.tag in formula:
                    skill_level = [skill.level]
                    formula.remove(skill.sketch.tag)
                else:
                    skill_level = []
                for f in formula:
                    if self.skill_tags.get(f):
                        skill_level.append(self.add_level(self.skill_tags.get(f)).level)
                skill.level = self.action_point(skill_level)
        return skill    

    def action_point(self, points: list[int | float | list]) -> float | int:
        p = 0
        for point in points:
            if type(point) == int or type(point) == float:
                p += point
            elif type(point) == list:
                p += self.action_point(point)
        
        return p/len(points)

    @property
    def energy(self):
        return self.skill_tags.get('energy')
    
    def tag(self, tag: str):
        if tag == 'st':
            return self.strength
        elif tag == 'dx':
            return self.dexterity
        elif tag == 'iq':
            return self.intelligence
        elif tag == 'hp':
            return self.health

    
class ExistenceDB(Base): 
    people_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='CASCADE'), default=None)
    char: Mapped['CharacterDB'] = relationship('CharacterDB', uselist=False, lazy='select', cascade='all', back_populates='exist')
    
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50), default='')
    gender: Mapped[Gender] = mapped_column(default=Gender.M.value)
    age: Mapped[int]
    amount_life: Mapped[int]
    die: Mapped[bool] = mapped_column(default=False)
    
    inventory: Mapped[InventoryDB] = relationship(InventoryDB, uselist=False, lazy='joined', cascade='all, delete-orphan', back_populates='exist')
    attibute_point: Mapped[AttributePointDB] = relationship(AttributePointDB, uselist=False, lazy='joined', cascade='all, delete-orphan', back_populates='exist')   
    location_id: Mapped[int] = mapped_column(ForeignKey('locationdb.id'), default=1, nullable=True)
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
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


