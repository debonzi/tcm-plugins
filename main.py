import json

import tcm.backends

from tcm.models.contract import Contract

def pprint(obj):
    print json.dumps(dict(obj),
                     indent=2,
                     #sort_keys=True,
                 )
    
 
if __name__ == '__main__':
    print '#########################################################'
    c1 = Contract.create_contract("Contract_1", 'smt')
    pprint(c1)
    c1.cancel()
    pprint(c1)
    print '#########################################################'

    print '#########################################################' 
    c2 = Contract.create_contract("Contract_2", 'telmex')
    pprint(c2)
    c2.cancel()
    pprint(c2)
    print '#########################################################'

    print '#########################################################'
    c3 = Contract.create_contract("Contract_3", 'net')
    pprint(c3)
    c3.cancel()
    pprint(c3)
    print '#########################################################'

