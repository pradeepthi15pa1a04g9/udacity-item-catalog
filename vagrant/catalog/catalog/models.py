from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

# Association table needed to create many-to-many relationship
# between items and tags
association_table = Table('item_tag', Base.metadata,
    Column('item_id', Integer, ForeignKey('item.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    tags = relationship(
        'Tag',
        # Using secondary means that entries in the association table are
        # automatically deleted when an tag is removed from an item or an
        # item is removed from a tag.
        secondary=association_table, 
        back_populates="items")

    def __repr__(self):
        """Method to provide pretty printing for items"""
        return "<Item: %s>" % self.name

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    items = relationship(
        'Item',
        secondary=association_table,
        back_populates="tags")

    def __repr__(self):
        """Method to provide pretty printing for tags"""
        return "<Tag: %s>" % self.name