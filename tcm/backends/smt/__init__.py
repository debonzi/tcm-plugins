from blinker import signal

from tcm.backends.decorators import backend_handler

@backend_handler
def created(sender, backend):
    sender.activated = True
    print "\tSMT handles %s creation" %sender.name
 
@backend_handler
def cancelled(sender, backend):
    sender.activated = False
    print "\tSMT handles %s cancel" %sender.name

signal('on_contract_create').connect(created)
signal('on_contract_cancel').connect(cancelled)
