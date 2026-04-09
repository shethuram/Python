from orm.models import Model
from orm.fields import CharField, ForeignKey
from models.user import User

class Post(Model):
    title = CharField(max_length=200)
    user = ForeignKey(User)