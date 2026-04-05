from orm.db import get_connection

class QuerySet:
    def __init__(self, model):
        self.model = model
        self.filters = []
        self.ordering = None

    def filter(self, **kwargs):
        for key, value in kwargs.items():
            if "__" in key:
                field, op = key.split("__")
            else:
                field, op = key, "eq"

            self.filters.append((field, op, value))

        return self    
    
    def order_by(self, field):
        if field.startswith("-"):
            self.ordering = (field[1:], "DESC")
        else:
            self.ordering = (field, "ASC")

        return self

    def _build_where(self):
        clauses = []
        values = []

        op_map = {
            "eq": "=",
            "gte": ">=",
            "lte": "<=",
            "gt": ">",
            "lt": "<"
        }

        for field, op, value in self.filters:
            sql_op = op_map.get(op, "=")
            clauses.append(f"{field} {sql_op} ?")
            values.append(value)

        return " AND ".join(clauses), values


    def all(self):
        table = self.model._meta["table_name"]

        sql = f"SELECT * FROM {table}"

        where_clause, values = self._build_where()

        if where_clause:
            sql += f" WHERE {where_clause}"

        if self.ordering:
            field, direction = self.ordering
            sql += f" ORDER BY {field} {direction}"

        sql += ";"

        print("SQL:", sql, "VALUES:", values)

        # execute
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)

        rows = cursor.fetchall()
        conn.close()

        # convert rows → objects
        results = []
        field_names = ["id"] + list(self.model._meta["fields"].keys())

        for row in rows:
            data = {}

            for i, field in enumerate(field_names):
                data[field] = row[i]

            obj = self.model(**data)   #  pass data directly
            results.append(obj)

        return results