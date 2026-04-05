from orm.models import Model
from orm.fields import CharField, IntegerField

class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()