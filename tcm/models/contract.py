from blinker import signal
from tcm.backends import get_pbe_info

on_c_create = signal('on_contract_create')
on_c_cancel = signal('on_contract_cancel')

class Contract:
    @classmethod
    def create_contract(cls, name, backend):
        print "contract %s will be created" %name
        c = Contract()
        c.backend = backend
        c.name = name
        c.active = True
        c.activated = False
        on_c_create.send(c, backend=c.backend)
        print "Contract %s created\n" %c.name
        return c
 
    def cancel(self):
        print "Contract %s is about to be cancelled" %self.name
        self.active = False
        on_c_cancel.send(self, backend=self.backend)
        print "Contract %s cancelled\n" %self.name

    def __iter__(self):
        yield 'name', self.name
        yield 'active', self.active
        yield 'activated', self.activated
        backend_info_f = get_pbe_info(self.backend)
        if callable(backend_info_f):
            yield 'backend', backend_info_f(self)
        else:
            yield 'backend', self.backend
