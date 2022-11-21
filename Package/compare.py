
from dreqPy import dreq
import os
import collections

refVersion = '01.00.31'
mode = "file"
if mode == "http":
  import urllib2
  ref = 'http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/%s/dreqPy/docs/dreq.xml' % refVersion
  refi = 'http://proj.badc.rl.ac.uk/svn/exarch/CMIP6dreq/tags/%s/dreqPy/docs/dreq2Defn.xml' % refVersion
  reqi = urllib2.Request(refi)
  response = urllib2.urlopen(reqi)
  the_pagei = response.read()

  req = urllib2.Request(ref)
  response = urllib2.urlopen(req)
  the_page = response.read()
  strings = True

else:
  strings = False
  the_page = '/data/svn/exarch/CMIP6dreq/tags/%s/dreqPy/docs/dreq.xml' % refVersion
  the_pagei = '/data/svn/exarch/CMIP6dreq/tags/%s/dreqPy/docs/dreq2Defn.xml' % refVersion


print( the_page )
print( the_pagei )
dq = dreq.loadDreq( dreqXML=the_page, configdoc=the_pagei, strings=strings, manifest=None )
print( "Current" )
dqc = dreq.loadDreq()

print( 'Comparing version %s with current' % refVersion )

s0 = set( dqc.coll.keys() )
s1 = set( dq.coll.keys() )
if len( s1.difference( s0 ) ) > 0:
  print( 'Sections omitted in current: %s' % str( s1.difference( s0 ) ) )
else:
  print( 'No sections removed' )
if len( s0.difference( s1 ) ) > 0:
  print( 'Sections new in current: %s' % str( s0.difference( s1 ) ) )
else:
  print( 'No sections added' )

ss = s0.intersection( s1 )
dtdall = dict()
for s in sorted( list(ss) ):
  lchange = len( dqc.coll[s].items ) - len( dq.coll[s].items )
  new = {i for i in dqc.coll[s].items if i.uid not in dq.inx.uid}
  dlab = set()
  dtd = set()
  dother = set()
  for i in dqc.coll[s].items:
    if i.uid in dq.inx.uid:
      i1 = dq.inx.uid[i.uid]
      if i.label != i1.label:
        dlab.add( i.uid )
      if i.title != i1.title or ('description' in i.__dict__ and i.description != i1.description):
        if 'description' in i.__dict__:
          dtd.add( (i.label,i.title,i.description,i1.label,i1.title,i1.description,'%s%s%s' % (i.label==i1.label,i.title==i1.title,i.description==i1.description) ) )
        else:
          dtd.add( (i.label,i.title,"",i1.label,i1.title,"",'%s%s' % (i.label==i1.label,i.title==i1.title) ) )
      for k in i._a.keys():
         if i.__dict__.get(k,None) != i1.__dict__.get(k,None):
           dother.add( i.uid )
     
  lnew = len( list( new ) )
  ldlab = len( list( dlab ) )
  ltd = len( list( dtd ) )
  if ltd > 0:
    dtdall[s] = dtd
  lother = len( list( dother ) )
  print( 'Section %16s: changes:: length %4s; records %4s; label %4s; t/d %4s; other %4s' % (s,lchange,lnew,ldlab,ltd,lother) )
  for i in new:
    print( '%s: %s [%s]' % (i.uid, i.label, i.title) )
  ##if len( dq.coll[s].items ) == len( dqc.coll[s].items ):
    ##print( "Section %s: length unchanged -- %s" % (s,len( dqc.coll[s].items ) )
  ##elif len( dq.coll[s].items ) < len( dqc.coll[s].items ):
    ##print( "Section %s: expanded %s to %s" % (s,len( dq.coll[s].items ), len( dqc.coll[s].items ))
  ##else:
    ##print "Section %s: shrunk %s to %s" % (s,len( dq.coll[s].items ), len( dqc.coll[s].items ))


if len(dtdall.keys()) > 0:
  oo = open('title_description_changes.csv', 'w' )
  for k in sorted( dtdall.keys() ):
     for t in dtdall[k]:
       oo.write( '\t'.join( t ) + '\n' )
  oo.close()
    


