def get_user_todos(user):
    return user.todo.all()


def get_friends_todos(user):
    friends = user.profile.friends.all()
    friends_todos = []
    for todos in map(lambda x: x.user.todo.all(), friends):
        '''map(lambda x: x.user.todo.all(), friends) - список содержаший по списку todo на каждого друга'''
        friends_todos.extend(todos)
    return friends_todos