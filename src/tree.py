'''
@author: Antonin Duroy
'''

from json.encoder import JSONEncoder

class SpinTree():
    """ Tree representation of a spin
    """
    
    def __init__(self, or_=False, and_=False, value=None):
        self.children = []
        self.value = value
        self.or_ = or_
        self.and_ = and_
        self.__check_parameters()
    
    def __check_parameters(self):
        """ Values must be set under certain conditions
        """
        if self.or_ and self.and_:
            raise ValueError('Cannot get both `AND` and `OR` conditions set to True.')
        if not self.or_ and not self.and_ and self.value is None:
            raise ValueError('Value must be set.')
    
    def add_child(self, child):
        """ Add a new branch to the current tree
        """
        self.children.append(child)
    
    def to_string(self, depth=0):
        """ Convert the Spin, represented as a tree, to a printable string
        """
        s = ""
        if self.value is not None:
            s += self.value
        elif self.or_:
            s += "OR"
        elif self.and_:
            s += "AND"
        depth += 1
        for child in self.children:
            s += '\n'+'__'*depth+child.to_string(depth)
        return s
    
    def to_dict(self):
        """ Convert the Spin, represented as a tree, to a Python dictionary
        """
        d = {}
        if self.value is not None:
            d["value"] = self.value
        
        if not self.children:
            return d
        
        if self.or_:
            attr_ = "or"
        elif self.and_:
            attr_ = "and"
        d[attr_] = []
        
        for child in self.children:
            d[attr_].append(child.to_dict())
        return d
        
    def to_json(self):
        """ Convert the Spin, represented as a tree, to a JSON string
        """
        return JSONEncoder().encode(self.to_dict())
    
    def __repr__(self):
        return self.to_string()