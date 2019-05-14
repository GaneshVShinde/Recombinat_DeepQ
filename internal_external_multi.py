import cellular
import random
import math
import qlearn
#import matplotlib.pyplot as plt
import backprop
import pickle
import os.path
from multiprocessing import Pool
import json
# Simulation Parameters

map='food.txt'
height=30
width=30

antCount=10
time=100000

dispersionRate=0.04     # rate of spread of pheromone
evaporationRate=0.99    # rate of disappearance of pheromone

#remember 1 ---5
#remember -1 ---6

# Mixed Case
actions=[0,1,2,3,4,5,6]    # set to [2,3,4] for not structure generation

# Purely External
#actions=[0,1,2,3,4]    # set to [2,3,4] for not structure generation

posReward=10			# reward for completing a trip
negReward=-1            # reward for moving

qEpsilon=0.1			# Q-Learning exploration rate
qLambda=0.95			# Q-Learning future discount rate
qAlpha=0.2				# Q-Learning learning rate
qDecayTill=0           #Q decay till


displaySize=10			# how big to make the display (set to 0 for no display)


learningRate=0.01
nnHidden=5
updateTimes=100
trainingTimes=10
memStaet=[]

agentsDict = {}
# for tracking how often different actions are chosen
count=[0,0,0,0,0,0,0]

isPher_Lev_NN =True
isIhIt_NN=False

class Cell:
  def __init__(self):
    self.isHome=0
    self.isFood=0
    self.homePher=0
    self.foodPher=0
  def update(self,around):
    htotal=0
    ftotal=0
    for c in around:
      htotal+=c.homePher
      ftotal+=c.foodPher
    havg=htotal/len(around)
    favg=ftotal/len(around)
    self.homePher+=(havg-self.homePher)*dispersionRate
    self.foodPher+=(favg-self.foodPher)*dispersionRate
    self.homePher*=evaporationRate
    self.foodPher*=evaporationRate
    if self.homePher>1: self.homePher=1
    if self.foodPher>1: self.foodPher=1
    if self.homePher<0.001: self.homePher=0
    if self.foodPher<0.001: self.foodPher=0

  def colour(self):
    if self.isHome: return '#FF0000'     # red
    if self.isFood: return '#0000FF'     # blue
    # if it isn't one of these two cases, we need to make a colour that's
    # a combination of red and blue
    r=min(self.homePher,1)
    b=min(self.foodPher,1)
    retVal = '#%02x00%02x'%(int(r*255),int(b*255))
    return retVal

  def copy(self,other):
    self.isHome=other.isHome
    self.isFood=other.isFood
    self.homePher=other.homePher
    self.foodPher=other.foodPher
  def load(self,text):
    self.isHome=0
    self.isFood=0
    if text=='H': self.isHome=1
    if text=='F': self.isFood=1

class Agent(cellular.Agent):
  def __init__(self,mem,isPher_Lev_NN=True,isIhIt_NN=False,actions=[0,1,2,3,4,5,6]):
    self.hasFood=0
    self.foodCount=0
    self.pherTime=0
    self.ai=qlearn.QLearn(epsilon=qEpsilon,lambd=qLambda,alpha=qAlpha)
    self.decayTill = qDecayTill
    self.isPher_Lev_NN=isPher_Lev_NN
    self.isIhIt_NN =isIhIt_NN
    if self.isIhIt_NN and self.isPher_Lev_NN :
      self.internal=backprop.NN(5,7,1)
    else:
      self.internal = backprop.NN(3,3,1)
    self.ai.setActions(actions)
    self.actionList=[]
    self.foodArray=[]
    self.mem=mem
    #self.MemState=[]
  
  def getmemState(self,pher_Lev=True,IhIt=False,):
      states=[]
      if self.isIhIt_NN:
        states.append(-1)
        states.append(-1)
        here = self.getLocation()
        if here.isHome:states[0]=1
        if here.isFood:states[1]=1
      if self.isPher_Lev_NN:
        states.append(((2*self.getHomePherLevel())/3 )- 1)
        states.append(((2*self.getFoodPherLevel())/3 )- 1)
      states.append(self.internal.ao[0])
      return states

  def update(self):
    here=self.getLocation()

    reward=negReward
    # change state if we've reached what we are looking for
    #when reached to home and reached to target this turned around nature should emergent
    self.foodArray.append(0)
    if self.hasFood:
      if here.isHome:
        self.hasFood=0
        self.turnAround()
        self.foodCount+=1
        self.foodArray[len(self.foodArray)-1]=1
        reward=posReward
    else:
      if here.isFood:
        self.hasFood=1
        self.turnAround()
    if self.pherTime<5:
        self.pherTime+=1

    # Mixed Case
    #what is use of this loop? may be some what randomizing memory
    for i in range(updateTimes):
       i=self.getmemState()
       self.internal.update(i)

    #why mem is sometimes 2,3
    mem=round((self.internal.ao[0]+1.0)*self.mem/2)
    #self.MemState.append({"state":self.getmemState(),"memory":mem})
    #mem=int(self.internal.ao[0])

    # Mixed Case
    state=(self.getHomePherLevel(),self.getFoodPherLevel(),self.pherTime,mem)

    # External Case
    #state=(self.getHomePherLevel(),self.getFoodPherLevel(),self.pherTime)

    self.ai.learn(state,reward)
    choice=self.ai.do(state)
    self.actionList.append(choice)

    if self.world.age>100:
      count[choice]+=1

    if choice==0:
      self.dropHomePher()
    elif choice==1:
      self.dropFoodPher()
    elif choice==2:
      self.followHomePher()
    elif choice==3:
      self.followFoodPher()
    elif choice==4:
      self.moveRandomly()
    elif choice==5:
      self.doChange(-1)
    elif choice==6:
      self.doChange(1)



  def dropFoodPher(self):
    here=self.getLocation()
    here.foodPher+=0.2
    self.pherTime=0
  def dropHomePher(self):
    here=self.getLocation()
    here.homePher+=0.2
    self.pherTime=0
  def getPherLevel(self,p):
    if p==0: return 0
    elif p<0.1: return 1
    elif p<0.25: return 2
    else: return 3
  def getFoodPherLevel(self):
    return self.getPherLevel(self.getLocation().foodPher)
  def getHomePherLevel(self):
    return self.getPherLevel(self.getLocation().homePher)

  def followFoodPher(self):
    c=self.getCellAhead()
    self.turn(-1)
    l=self.getCellAhead()
    self.turn(2)
    r=self.getCellAhead()
    self.turn(-1)


    if c.isFood: c=1
    else: c=c.foodPher
    if l.isFood: l=1
    else: l=l.foodPher
    if r.isFood: r=1
    else: r=r.foodPher

    self.followPher(l,c,r)
  def followHomePher(self):
    c=self.getCellAhead()
    self.turn(-1)
    l=self.getCellAhead()
    self.turn(2)
    r=self.getCellAhead()
    self.turn(-1)

    if c.isHome: c=1
    else: c=c.homePher
    if l.isHome: l=1
    else: l=l.homePher
    if r.isHome: r=1
    else: r=r.homePher

    self.followPher(l,c,r)
  def followPher(self,l,c,r):
    m=(l,c,r)
    max_m=max(m)
    max_ind=[]
    for i in range(len(m)):
      if max_m == m[i]:
        max_ind.append(i)
    i = random.choice(max_ind)
    if i == 0:
      self.turnLeft()
    elif i == 2:
      self.turnRight()
    self.goForward()

  def moveRandomly(self):
    self.turn(random.choice([0,1,-1]))
    self.goForward()

  def colour(self):
    if self.hasFood: return '#0000FF'   # blue
    else: return '#FF0000'              # red
  
  def doChange(self,value):
    i=self.getmemState()
    for x in range(trainingTimes):
      self.internal.trainOne(i,[value],learningRate)




def run(mem):
#if __name__=='__main__':
  global isPher_Lev_NN,isIhIt_NN
  world=cellular.World(Cell,width,height)
  world.load(map)

  # figure out where to put the ants (they should start at home)
  homes=[]
  for i in range(width):
    for j in range(height):
      if world.grid[i][j].isHome: homes.append((i,j))
  for i in range(antCount):
    ant=Agent(mem,isPher_Lev_NN,isIhIt_NN,actions=actions)
    i,j=random.choice(homes)
    world.addAgent(ant,x=i,y=j)

  if displaySize:
    world.display(size=displaySize)

  countList=[]
  data=[]

  # run the simulation
  for i in range(time):
    world.update()

    if i%100==99:
      totalFood=0.0
      for a in world.agents:
        totalFood+=a.foodCount
        a.foodCount=0
      data.append(totalFood/antCount)
      countList.append(list(count))
      for j in range(len(count)): count[j]=0

  r={'trips':data,'count':countList}
  #temprory removing action list
  agentsDict
  agents=[{"actions":agent.actionList,"food":agent.foodArray,"q":agent.ai.q} for agent in world.agents ]
  # food =[agent.foodArray for agent in world.agents]
  # #memList = [agent.MemState for agent in world.agents]
  # r['actions']=actionList
  # r['food']= food
  r['agents'] =agents 
  
#  agents = {}
#  fl = None
#  for i in range(len(world.agents)):
#    agents[i]={"historyA":world.agents[i].ai.historyA,"historyS":world.agents[i].ai.historyS,"Q":world.agents[i].ai.q}
#
#  agentsDict[datetime.datetime.today().strftime('%Y-%m-%d-%R-%S')] = agents
#  print("len agentsDic:",len(agentsDict))
  return r

#run()




#objToDump should be dict
def pickleDumpToTheFile(flName,objToDump):
  fl = None
  if os.path.exists(flName):
      fl = open(flName,'rb+')
      oldObjData=pickle.load(fl)
      objToDump.update(oldObjData)
  else:
      fl = open(flName,"wb+")
  pickle.dump(objToDump,fl)
  fl.close()

def multiProcessSimulation(nProcess,lst_args,func_ToProcess):
    p= Pool(nProcess)
    result = p.map(func_ToProcess,lst_args)
    p.close()
    p.join()




if __name__=='__main__':
  #print(run())
  def simulate(memState):
      #ts =  myTime.time()
      print(memState)
      flName ="Data/multi2/MemoryMap_multi"+str(memState)+".dat"
      fl = open(flName,'wb+')
      for i in range(1000):
        print(i," iter","mem",memState)
        data=run(memState)
        #print(data)
        pickle.dump(data,fl)
      fl.close()
  """ code commented bellow because to test with 48 mem 100000"""
  def simulate2(iter):
    print("iter:",iter)
    flName ="Data/FreeRiders/Data_WithRandom/Data2_"+str(iter)+".json"
    #fl = open(flName,'wb+')
    data=run(48.0)
    #pickle.dump(data,fl)
    #fl.close()
    with open(flName, 'w') as fp:
      json.dump(data, fp,sort_keys=True)
  lst=list(range(4))
  # memList=[16.0,28.0,32.0,48.0,64.0]
  # #[memList.append(float(m)) for m in range(24,40,4)]
  p= Pool()
  result = p.map(simulate2,lst)
  p.close()
  p.join()

#  for memState in memList:
#      p=multiprocessing.Pool()
#      p=multiprocessing.Process(target=simulate,args=(memState,))
#      p.start()

  
#  pickleDumpToTheFile(flName,dt)
