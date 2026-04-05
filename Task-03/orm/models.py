from orm.db import get_connection
from orm.queryset import QuerySet
from orm.fields import Field, ForeignKey

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
       
        # collect fields
        fields = {}

        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value

        # create class
        new_class = super().__new__(cls, name, bases, attrs)

        # attach metadata
        new_class._meta = {
            "table_name": name.lower(),
            "fields": fields
        }

        #  setup reverse relations for ForeignKey
        for field_name, field in fields.items():
            if isinstance(field, ForeignKey):
                related_model = field.to
                related_name = f"{name.lower()}s"   # e.g. posts

                # avoid overriding if already exists
                if not hasattr(related_model, related_name):

                    def getter(self, field_name=field_name, model=new_class):
                        return model.filter(**{field_name: self.id}).all()

                    setattr(related_model, related_name, property(getter))

        return new_class
    

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for field_name in self._meta["fields"]:
            if field_name in kwargs:   #  only set if provided
                setattr(self, field_name, kwargs[field_name])

    def __repr__(self):
        field_values = ", ".join(
            f"{k}={getattr(self, k)!r}" for k in self._meta["fields"]
        )
        return f"{self.__class__.__name__}({field_values})"
    

    @classmethod
    def create_table(cls):
        fields_sql = []

        # add id field
        fields_sql.append("id INTEGER PRIMARY KEY AUTOINCREMENT")

        # add other fields
        for name, field in cls._meta["fields"].items():
            field_sql = f"{name} {field.get_sql()}"
            fields_sql.append(field_sql)

        # build full SQL
        sql = f"""
        CREATE TABLE IF NOT EXISTS {cls._meta['table_name']} (
            {", ".join(fields_sql)}
        );
        """

        print("SQL:", sql.strip())

        # execute
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()

        print(f"Table '{cls._meta['table_name']}' created.")


    def save(self):
        table = self._meta["table_name"]
        fields = self._meta["fields"]

        column_names = []
        values = []
        placeholders = []

        for name in fields:
            value = getattr(self, name)

            # skip None values (optional behavior)
            if value is not None:
                column_names.append(name)
                values.append(value)
                placeholders.append("?")

        # build SQL
        columns_str = ", ".join(column_names)
        placeholders_str = ", ".join(placeholders)

        sql = f"""
        INSERT INTO {table} ({columns_str})
        VALUES ({placeholders_str});
        """

        print("SQL:", sql.strip(), "VALUES:", values)

        # execute
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)

        # get auto id
        self.id = cursor.lastrowid

        conn.commit()
        conn.close()

        print(f"Record saved: {self}")    


    def delete(self):
        if not hasattr(self, "id"):
            raise ValueError("Object has no id, cannot delete")

        table = self._meta["table_name"]

        sql = f"DELETE FROM {table} WHERE id = ?;"
        values = [self.id]

        print("SQL:", sql, "VALUES:", values)

        from orm.db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)

        conn.commit()
        conn.close()

        print(f"Deleted: {self}")        

    @classmethod
    def all(cls):
        from orm.queryset import QuerySet
        return QuerySet(cls).all()    
    
    
    @classmethod
    def filter(cls, **kwargs):
        return QuerySet(cls).filter(**kwargs)    
    
    @classmethod
    def drop_table(cls):
        table = cls._meta["table_name"]

        sql = f"DROP TABLE IF EXISTS {table};"
        print("SQL:", sql)

        from orm.db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        conn.commit()
        conn.close()

        print(f"Table '{table}' dropped.")


    @classmethod
    def truncate_table(cls):
        table = cls._meta["table_name"]

        sql = f"DELETE FROM {table};"
        print("SQL:", sql)

        from orm.db import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        conn.commit()
        conn.close()

        print(f"Table '{table}' truncated (all rows deleted).")    
    


