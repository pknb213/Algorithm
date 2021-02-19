class Agent(object):
    def __init__(self, id, abc):
        self._id = id
        self._abc = abc
    def __str__(self):
        return str(self._id)

a = Agent(id=1, abc='a')

print(a)





