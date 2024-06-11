# lib/models/network.py
from models.__init__ import CURSOR, CONN

class Network:
    all = {}

    def __init__(self, name, location, id="None"):
        self.name = name
        self.location = location
        self._id = id

    def __repr__(self):
        return f"<Network {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Network instances """
        sql = """
            CREATE TABLE IF NOT EXISTS networks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Network instances """
        sql = """
            DROP TABLE IF EXISTS networks;
        """
        CURSOR.execute(sql)
        CONN.commit()   

    def save(self):
        """ Insert a new row with the name, location values of the current Networks object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO networks (name, location)
                VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        """ Initialize a new Network instance and save the object to the database """
        network = cls(name, location)
        network.save()
        return network
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Network object per table row"""
        sql = """
            SELECT *
            FROM networks
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def instance_from_db(cls, row):
        """Return a Network object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        network = cls.all.get(row[0])
        if network:
            # ensure attributes match row values in case local instance was modified
            network.name = row[1]
            network.location = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            network = cls(row[1], row[2])
            network.id = row[0]
            cls.all[network.id] = network
        return network
    
    @classmethod
    def find_by_id(cls, id):
        """Return a Networkls object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM networks
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
   
    def delete(self):
        """Delete the table row corresponding to the current Network instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM networks
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None