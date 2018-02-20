# UpdatingObject and UpdatingProperty
import bananagui


class VeryBasicToot(bananagui.UpdatingObject):

    def __init__(self):
        self.updated = 0
        self._toot = 'lol'

    @bananagui.UpdatingProperty.updater_with_attr('_toot')
    def toot(self):
        self.updated += 1


class UpdatingToot(VeryBasicToot):

    def __init__(self):
        super().__init__()
        self.wants_toot = False

    def needs_updating(self):
        return self.wants_toot


def test_needs_updating():
    toot = VeryBasicToot()
    assert toot.toot == 'lol'
    assert toot.updated == 0
    toot.toot = 'new toot'
    assert toot.updated == 1

    toot = UpdatingToot()
    assert toot.toot == 'lol'

    toot.toot = 'even newer toot'
    assert toot.updated == 0

    toot.wants_toot = True
    toot.toot = 'damn new toot!'
    assert toot.updated == 1


class BoringToot(bananagui.UpdatingObject):

    def __init__(self):
        self.toot_log = []

    def _log_appender(string):
        def result(self, *args):
            self.toot_log.append(string)
            if args:
                assert string == 'set' and args == ('blah',)
            return 'from ' + string
        result.__doc__ = string + ' doc'
        return result

    _set = _log_appender('set')
    _old_get = _log_appender('old get')
    _new_get = _log_appender('new get')
    _delete = _log_appender('delete')
    _update = _log_appender('update')

    # fake decorating
    toot = bananagui.UpdatingProperty(_old_get)
    toot = toot.setter(_set)
    toot = toot.getter(_new_get)
    toot = toot.deleter(_delete)
    toot = toot.updater(_update)


def test_f_attributes():
    # skip fset, its behaviour is an implementation detail (see docstring)
    assert BoringToot.toot.fget is BoringToot._new_get
    assert BoringToot.toot.fdel is BoringToot._delete
    assert BoringToot.toot.fupdate is BoringToot._update


def test_boring_ways_to_make_updating_objects():
    toot = BoringToot()
    assert not toot.toot_log

    assert toot.toot == 'from new get'
    toot.toot = 'blah'
    del toot.toot
    assert toot.toot_log == ['new get', 'set', 'update', 'delete']

    # make sure fset=None works
    prop = bananagui.UpdatingProperty()
    prop.getter(print)
    prop.deleter(print)
    prop.updater(print)
    assert prop.fget is None


def test_docs():
    def foo():
        """foo docstring"""

    def bar():
        """bar docstring"""

    def mysterious():   # no docstring
        pass

    # getter() sets the docstring, just like with builtin property
    prop = bananagui.UpdatingProperty()
    assert prop.__doc__ is None
    prop = prop.setter(foo).getter(bar).deleter(foo).updater(foo)
    assert prop.__doc__ == 'bar docstring'

    prop = bananagui.UpdatingProperty(foo)
    assert prop.__doc__ == foo.__doc__
    prop = prop.setter(bar).getter(bar).deleter(bar).updater(bar)
    assert prop.__doc__ == foo.__doc__

    assert bananagui.UpdatingProperty(mysterious).__doc__ is None
    assert bananagui.UpdatingProperty(foo, doc='tada!').__doc__ == 'tada!'

    bupuwa = bananagui.UpdatingProperty.updater_with_attr
    assert bupuwa('wat')(mysterious).__doc__ is None
    assert bupuwa('wat')(foo).__doc__ == 'foo docstring'
    assert bupuwa('wat', doc='override!')(foo).__doc__ == 'override!'
