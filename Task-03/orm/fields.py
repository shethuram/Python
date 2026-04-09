class Field:
    def __init__(self, null=False, unique=False):
        self.null = null
        self.unique = unique
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not self.null and value is None:
            raise ValueError(f"{self.name} cannot be null")
        instance.__dict__[self.name] = value

    def get_sql(self):
        raise NotImplementedError    


class CharField(Field):
    def __init__(self, max_length=255, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def __set__(self, instance, value):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")

        if value and len(value) > self.max_length:
            raise ValueError(f"{self.name} exceeds max_length")

        super().__set__(instance, value)


    def get_sql(self):
        sql = f"VARCHAR({self.max_length})"
        if not self.null:
            sql += " NOT NULL"
        if self.unique:
            sql += " UNIQUE"
        return sql    


class IntegerField(Field):
    def __set__(self, instance, value):
        if value is not None and not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")

        super().__set__(instance, value)


    def get_sql(self):
        sql = "INTEGER"
        if not self.null:
            sql += " NOT NULL"
        return sql    
    

class ForeignKey(Field):
    def __init__(self, to, **kwargs):
        super().__init__(**kwargs)
        self.to = to   # referenced model

    def get_sql(self):
        return "INTEGER"   # stores id

    def __set__(self, instance, value):
        # allow setting object or id
        if isinstance(value, self.to):
            value = value.id
        super().__set__(instance, value)    