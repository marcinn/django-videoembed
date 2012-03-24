class WrappersRegistry(object):
    def __init__(self):
        self._wrappers = []

    def register(self, wrapper):
        self._wrappers.append(wrapper())

    def unregister(self, wrapper):
        self._wrappers.remove(wrapper())

    def get_all(self):
        return self._wrappers[:]


wrappers = WrappersRegistry()

