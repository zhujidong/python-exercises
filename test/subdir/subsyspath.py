import sys
import os.path

def subsyspath():
    print( 'sub:', sys.path[0])
    print('dirname->>', os.path.dirname(__file__) )
    
if __name__ == '__main__':
    print( 'sub:', sys.path[0])
    print('dirname->>', os.path.dirname(__file__) )
    print( 'abspath->>',os.path.abspath(__file__) )