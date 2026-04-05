from models.user import User

# create
User.create_table()

# insert
User(name="Ram", age=21).save()
User(name="Ajay", age=25).save()

# view
print(User.all())

# truncate (delete all rows)
User.truncate_table()
print(User.all())   # []

# drop table
User.drop_table()