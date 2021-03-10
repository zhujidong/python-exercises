import os.path

print('dirname->>', os.path.dirname(__file__) )
print( 'basename->>',os.path.basename(__file__) )

print( 'abspath->>',os.path.abspath(__file__) )
print( 'dirname(abspath)->>',os.path.dirname(os.path.abspath(__file__)) )
print( '2dirname(abspath)->>',os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ) )

print( 'pathjoin', os.path.join(os.path.dirname(__file__),'addpath','andothers') )