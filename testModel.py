from model.model import Model
myModel = Model()

myModel.buildGraph(2014)

print(myModel.getGraphDetails())
print(myModel.getArcoMax())

