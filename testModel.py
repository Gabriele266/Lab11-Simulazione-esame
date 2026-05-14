from model.model import Model

model=Model()

model.buildGraph('Rock')

print(model.getNumNodi())
print(model.getNumEdges())
print(model.getBestArtist())
