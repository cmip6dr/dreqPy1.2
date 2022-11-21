
import dreq

vc = dreq.loadDreq( dreqXML='vocab.xml',configdoc='out/vocabDefn.xml' )


print ( vc.coll.keys() )
print ( vc.coll['institute'].attDefn.keys() )
for r in  vc.coll['institute'].items:
   print ( '%20s: %s [%s]' % (r.label,r.description,r.isni) )
