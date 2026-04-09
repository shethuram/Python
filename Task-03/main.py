from models.user import User
from models.post import Post


def main():
    print("\n========== DROP TABLES ==========")
    Post.drop_table()
    User.drop_table()

    print("\n========== CREATE TABLES ==========")
    User.create_table()
    Post.create_table()

    print("\n========== INSERT USERS ==========")
    u1 = User(name="Ram", age=21)
    u1.save()

    u2 = User(name="Ajay", age=25)
    u2.save()

    u3 = User(name="Kiran", age=30)
    u3.save()

    print("\n========== INSERT POSTS ==========")
    p1 = Post(title="Post 1", user=u1)
    p1.save()

    p2 = Post(title="Post 2", user=u1)
    p2.save()

    p3 = Post(title="Post 3", user=u2)
    p3.save()

    print("\n========== ALL USERS ==========")
    for u in User.all():
        print(u)

    print("\n========== ALL POSTS ==========")
    for p in Post.all():
        print(p)

    print("\n========== FOREIGN KEY ==========")
    print("Post.user (id):", p1.user)

    print("\n========== REVERSE RELATION ==========")
    for p in u1.posts:   #  injected by metaclass
        print(p)

    print("\n========== FILTER ==========")
    for u in User.filter(age__gte=25).all():
        print(u)

    print("\n========== CHAIN QUERY ==========")
    for u in User.filter(age__gte=21).order_by("-name").all():
        print(u)

    print("\n========== POSTS OF USER ==========")
    for p in Post.filter(user=u1.id).all():
        print(p)

    print("\n========== DELETE ==========")
    u2.delete()

    print("\n========== USERS AFTER DELETE ==========")
    for u in User.all():
        print(u)

    print("\n========== TRUNCATE POSTS ==========")
    Post.truncate_table()
    print(Post.all())

    print("\n========== DROP TABLES ==========")
    Post.drop_table()
    User.drop_table()


if __name__ == "__main__":
    main()