# lib/models/show.py
#!/usr/bin/env python3
from models.__init__ import CURSOR, CONN
from models.network import Network



class Show:
    all = {}

    def __init__(self, name, genre, network_id, ):
     
        self.name = name
        self.genre = genre
        self.network_id = network_id
      #add setters and getters for all attributes as property methods in both shows and networks
    
   
    @property
    def name(self):
        """Returns the name of the show."""
        return self._name
    
    @name.setter
    def name(self, name):
      if len(name) >= 20:
        raise ValueError("Name must 20 characters or less")
      else:
        self._name = name
    
    @property
    def genre(self):
        """Returns the name of the show."""
        return self._genre
    
    @genre.setter
    def genre(self, genre):
       if len(genre) >= 20:
        raise ValueError("Genre must 20 characters or less")
       else:
          self._genre = genre
     

    @property
    def network_id(self):
        return self._network_id
    
    @network_id.setter 
    def network_id(self, network_id):
        if type(network_id) is int and Network.find_by_id(network_id):
            self._network_id = network_id
        else:
            raise ValueError(
                "network_id must reference a network in the database")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY,
            name TEXT,
            genre TEXT,     
            network_id INTEGER REFERENCES networks(id))
      
            
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Show instances """
        sql = """
            DROP TABLE IF EXISTS shows;
        """
        CURSOR.execute(sql)
        CONN.commit()
   
    def save(self):
        """ Insert a new row with the name, genre values of the current Show object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO shows (name, genre, network_id)
                VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.genre, self.network_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, genre, network_id):
        """ Initialize a new Show instance and save the object to the database """
        show = cls(name, genre, network_id)
        show.name = name  # Calls the name setter for validation

        # Validate genre attribute using the setter
        show.genre = genre  # Calls the genre setter for validation

        # Validate network_id attribute using the setter
        show.network_id = network_id  # Calls the network_id setter for validation
    
          # Now create the Show instance after validation
        show.save()
        return show
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Show object per table row"""
        sql = """
            SELECT *
            FROM shows
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a Show object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        show = cls.all.get(row[0])
        if show:
            # ensure attributes match row values in case local instance was modified
            show.name = row[1]
            show.genre = row[2]
            show.network_id =row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            show = cls(row[1], row[2], row[3])
            show.id = row[0]
            cls.all[show.id] = show
        return show
    
    
    @classmethod
    def find_by_name(cls, name):
        """Return a Show object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM shows
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_id(cls, id):
        """Return a Shows object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM shows
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def delete(self):
        """Delete the table row corresponding to the current Show instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM shows
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None
    
   

    @classmethod #upfate this to a setter
    def network_id(self, network_id):
        if type(network_id) is int and Network.find_by_id(network_id):
            self._network_id = network_id
        else:
            raise ValueError(
                "network_id must reference a network in the database")
  
   