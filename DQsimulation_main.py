import json
import os
import pickle
import time


time_ = str(int(time.time()))

def create_recursive_dir(dir):
    pass


def case3(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    folder_name = path+"/data/1M/case_3/"
    # if not os.path.exists(folder_name):
    #     os.makedirs(folder_name)
    flName =folder_name+"case3_1M_"+time_+"_"+str(iter)+".dat"
    Forage_DQN.isIhIt_NN = True
    Forage_DQN.isPher_Lev_NN=True
    Forage_DQN.displaySize=0
    Forage_DQN.qDecayTill = 0
    Forage_DQN.time = 1000
    data=Forage_DQN.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()


def case3_JSON(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    folder_name = path+"/data/1M/case_3/"
    # if not os.path.exists(folder_name):
    #     os.makedirs(folder_name)
    flName =folder_name+"case3_1M_"+time_+"_"+str(iter)+".json"
    Forage_DQN.isIhIt_NN = True
    Forage_DQN.isPher_Lev_NN=True
    Forage_DQN.displaySize=0
    Forage_DQN.qDecayTill = 0
    Forage_DQN.time = 1000
    data=Forage_DQN.run(4.0)
    Forage_DQN.json_dumps(data,flName)


if __name__ == "__main__":
    import Forage_DQN # for all other cases
    # import external as Forage_DQN # to run case 6
    lst=list(range(8))
    n_process = 5 #number of process at a same time
    Forage_DQN.multiProcessSimulation(n_process,lst,case3_JSON)
