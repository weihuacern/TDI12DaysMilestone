from graphviz import Digraph

if __name__ == '__main__':
  
  dot = Digraph(filename='ds_classification.gv', comment='The classification of data structure')
  dot.node('Collection')
  dot.node('Linear')
  dot.node('Nonlinear')
  dot.edge('Collection', 'Linear')
  dot.edge('Collection', 'Nonlinear')

  #Linear branch
  dot.node('GeneralizedIndexing')
  dot.node('DirectAccess')
  dot.node('SequentialAccess')
  dot.edge('Linear', 'GeneralizedIndexing')
  dot.edge('Linear', 'DirectAccess')
  dot.edge('Linear', 'SequentialAccess')

  dot.node('Dictionary')
  dot.node('HashTable')
  dot.edge('GeneralizedIndexing', 'Dictionary')
  dot.edge('GeneralizedIndexing', 'HashTable')
  dot.node('Array')
  dot.node('Record')
  dot.node('File')
  dot.edge('DirectAccess', 'Array')
  dot.edge('DirectAccess', 'Record')
  dot.edge('DirectAccess', 'File')
  dot.node('List')
  dot.node('Stack')
  dot.node('Queue')
  dot.edge('SequentialAccess', 'List')
  dot.edge('SequentialAccess', 'Stack')
  dot.edge('SequentialAccess', 'Queue')
  #dot.node('')
  #dot.edge('', '')

  #Nonlinear branch
  dot.node('Hierarchical')
  dot.node('Group')
  dot.edge('Nonlinear', 'Hierarchical')
  dot.edge('Nonlinear', 'Group')

  dot.node('Tree')
  dot.node('Heap')
  dot.node('Set')
  dot.node('Graph')
  dot.edge('Hierarchical', 'Tree')
  dot.edge('Hierarchical', 'Heap')
  dot.edge('Group', 'Set')
  dot.edge('Group', 'Graph')
  #print(dot.source)
  dot.format = 'png'
  dot.view()
  #dot.render('.', view=True)
