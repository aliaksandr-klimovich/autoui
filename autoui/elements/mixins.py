from autoui.elements.abstract import Element


class Fillable(object):
    """
    Mixin class ``Fillable`` for ``Element`` class.
    Those methods should be compatible,
    i.e. data, obtained with ``get_state`` method, should be capable to pass to ``fill`` method without exceptions.
    """
    stop_propagation = False

    def _get_names(self):
        """
        Returns names (strings) of class and instance attributes that are instance of ``Element`` class.
        """
        names = set()
        for element_name in self.__class__.__dict__:
            if isinstance(self.__class__.__dict__[element_name], Element):
                names.add(element_name)
        for element_name in self.__dict__:
            if isinstance(self.__dict__[element_name], Element) and element_name not in ('_instance', '_owner'):
                names.add(element_name)
        return names

    def fill(self, data, stop=False):
        """
        Recursively fills all elements with data.
        :param data: dictionary to fill with keys as elements names and values as fillable data
        :param stop: reserved for stop recursion
        """
        if stop:
            return
        _names = self._get_names()
        for _k, _v in data.items():
            if _v is not None and _k in _names:
                if self.stop_propagation:
                    getattr(self, _k).find().fill(_v, stop=True)
                else:
                    getattr(self, _k).find().fill(_v)

    def get_state(self, stop=False):
        """
        :return:  dict with state data, compatible with ``fill`` method
        :param stop: reserved for stop recursion
        """
        if stop:
            return
        _names = self._get_names()
        state = {}
        for name in _names:
            if self.stop_propagation:
                s = getattr(self, name).find().get_state(stop=True)
                if s is not None:
                    state[name] = s
            else:
                state[name] = getattr(self, name).find().get_state()
        return state
