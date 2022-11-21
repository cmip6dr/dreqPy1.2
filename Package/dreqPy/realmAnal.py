
import collections
from dreqPy import dreq

dq = dreq.loadDreq()

cc0 = collections.defaultdict( set )
cc1 = collections.defaultdict( set )
cc2 = collections.defaultdict( set )
def add( item, r ):
  cc0[r].add( item.uid )
  cc1[r].add( item.vid )
  cc2[r].add( dq.inx.uid[ item.vid ].sn )

for i in dq.coll['CMORvar'].items:
  r = i.modeling_realm
  if r.find( ' ' ) == -1:
    add( i, r )
  else:
    for x in r.split():
      add( i, x )


for k in sorted( cc0.keys() ):
  print k, len( cc0[k] ), len( cc1[k] ), len( cc2[k] )
