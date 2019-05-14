import json
import os
import pickle
import time

##Current ongoing simulation has problem that IhIt extention belongs to HpTp
# def simulate(iter):
#     relative = "../"
#     path=os.path.abspath(relative)
#     print("iter:",iter)
#     flName =path+"/Experiments/2_IhIt_"+str(iter)+".json"
#     #fl = open(flName,'wb+')
#     internal_external_multi.isIhIt_NN = True
#     internal_external_multi.isPher_Lev_NN=False
#     internal_external_multi.displaySize=0
#     internal_external_multi.time = 200000
#     data=internal_external_multi.run(32.0)
#     #pickle.dump(data,fl)
#     #fl.close()
#     with open(flName, 'w') as fp:
#         json.dump(data, fp,sort_keys=True)

# def simulate2(iter):
#     relative = "../"
#     path=os.path.abspath(relative)
#     print("iter:",iter)
#     flName =path+"/Experiments/2_HpTp_Ih_It_"+str(iter)+".json"
#     #fl = open(flName,'wb+')
#     internal_external_multi.isIhIt_NN = True
#     internal_external_multi.isPher_Lev_NN=True
#     internal_external_multi.displaySize=0
#     internal_external_multi.time = 200000
#     data=internal_external_multi.run(32.0)
#     #pickle.dump(data,fl)
#     #fl.close()
#     with open(flName, 'w') as fp:
#         json.dump(data, fp,sort_keys=True)

time_ = str(int(time.time()))

def case0(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/1M/case_0/case0_1M_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = False
    internal_external_multi.isPher_Lev_NN=False
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0
    internal_external_multi.time = 1000000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)


def case1(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/1M/case_1/case1_1M_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = False
    internal_external_multi.isPher_Lev_NN=True
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0
    internal_external_multi.time = 1000000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)

def case2(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/1M/case_2/case2_1M_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = True
    internal_external_multi.isPher_Lev_NN=False
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0
    internal_external_multi.time = 1000000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)

def case3(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/1M/case_3/case3_1M_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = True
    internal_external_multi.isPher_Lev_NN=True
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0
    internal_external_multi.time = 1000000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)

def case4(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/case_4/case4_5L_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = False
    internal_external_multi.isPher_Lev_NN=False
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0
    internal_external_multi.time = 500000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)

def case5(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/case_5/case5_5L_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = True
    internal_external_multi.isPher_Lev_NN=True
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0.04
    internal_external_multi.time = 500000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)

def case6(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/case_6/case6_2L_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = False
    internal_external_multi.isPher_Lev_NN=False
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0
    internal_external_multi.time = 200
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)

def case7(iter):
    relative = "./"
    path=os.path.abspath(relative)
    print("iter:",iter)
    flName =path+"/data/1M/case_7/case7_1M_"+time_+"_"+str(iter)+".dat"
    internal_external_multi.isIhIt_NN = False
    internal_external_multi.isPher_Lev_NN=False
    internal_external_multi.displaySize=0
    internal_external_multi.qDecayTill = 0.04
    internal_external_multi.time = 1000000
    data=internal_external_multi.run(4.0)
    fl = open(flName,'wb+')
    pickle.dump(data,fl)
    fl.close()
    #internal_external_multi.pickleDumpToTheFile(flName,data)
    # with open(flName, 'w') as fp:
    #     json.dump(data, fp,sort_keys=True)



if __name__ == "__main__":
    import internal_external_multi # for all other cases
    # import external as internal_external_multi # to run case 6
    lst=list(range(20))
    internal_external_multi.multiProcessSimulation(10,lst,case1)
