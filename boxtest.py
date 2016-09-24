import bananagui
from bananagui.base.layouts import BoxBase


class Base:

    def prepend(self, item):
        print("prepend:", item)

    def append(self, item):
        print("append:", item)

    def remove(self, item):
        print("remove:", item)


class Box(BoxBase, Base, bananagui.ObjectBase):

    def __repr__(self):
        return '<box %r>' % self[:]


class Item(bananagui.ObjectBase):

    parent = bananagui.Property('parent')
    value = bananagui.Property('value')

    def __init__(self, parent, value):
        self.raw_set('parent', parent)
        self.raw_set('value', value)

    def __repr__(self):
        return '<item %r>' % (self['value'],)


box = Box()
a,b,c,d,e,f,g,h,i,j = (Item(box, c) for c in 'abcdefghij')
