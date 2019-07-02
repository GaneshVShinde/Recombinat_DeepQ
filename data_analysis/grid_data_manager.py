import os
import json
import pickle
import enum

class cell_data_points(enum.Enum):
    homePher = 0
    foodPher = 1
    homePherDropCount = 2
    foodPherDropCount = 3



class agent_data_points(enum.Enum):
        hasFood =0
        foodCount= 1
        pherTime= 2
        action= 3
        food= 4
        x =5
        y =6
class single_grid_obj_templet:
    def __init__(self):
        self.cell={#'isHome': [],
         #'isFood': [],
         'homePher': [],
         'foodPher': [],
         'homePherDropCount': [],
         'foodPherDropCount': []    
        }
    def append_cell_data(self,dic):
       # self.cell['isHome'].append(dic['isHome'])
       # self.cell['isFood'].append(dic['isFood'])
        self.cell['homePher'].append(dic[cell_data_points.homePher.value])
        self.cell['foodPher'].append(dic[cell_data_points.foodPher.value])
        self.cell['homePherDropCount'].append(dic[cell_data_points.homePherDropCount.value])
        self.cell['foodPherDropCount'].append(dic[cell_data_points.foodPherDropCount.value])

class single_agent_obj_templet:
    def __init__(self):
            #hasFood 0
            #foodCount 1
            #pherTime 2
            #action 3
            #food 4
            # x 5
            # y 6
        self.agent={'hasFood': [],
         'foodCount': [],
         'pherTime': [],
         'action': [],
         'food': [],
         'x': [],
         'y':[]   
        }

    def append_agent_data(self,lst):
        self.agent['hasFood'].append(lst[agent_data_points.hasFood.value])
        self.agent['foodCount'].append(lst[agent_data_points.foodCount.value])
        self.agent['pherTime'].append(lst[agent_data_points.pherTime.value])
        self.agent['action'].append(lst[agent_data_points.action.value])
        self.agent['food'].append(lst[agent_data_points.food.value])
        self.agent['x'].append(lst[agent_data_points.x.value])
        self.agent['y'].append(lst[agent_data_points.y.value])




class grid_obj:
    def __init__(self,grid_size=(30,30)):
        self.grid=[[single_grid_obj_templet() 
          for i in range(grid_size[0])] 
         for j in range(grid_size[1])]
        
        self.grid_size = grid_size
        
    def append_cell(self,cell_list):
        for obj in cell_list:
            for i in range(len(obj[0])):
                for j in range(len(obj[0][i])):
                    self.grid[i][j].append_cell_data(obj[0][i][j])
    def serialize_data(self):
        cell_data = [[self.grid[i][j].cell for j in range(self.grid_size[1])]
                    for i in range(self.grid_size[0])
                    ]
        
        return cell_data
    
    def dump_obj(self,fl_name):
        with open(fl_name,'w+') as op:
            json.dump(self.serialize_data(),op)

    # def load_json_obj(self)


class agent_obj:
    def __init__(self,n_agent=10):
        self.agents = [single_agent_obj_templet() for i in range(n_agent)]
        self.n_agent = n_agent
        
    def append_agent(self,agent_list):
        for obj in agent_list:
            for i in range(len(obj[1])):
                self.agents[i].append_agent_data(obj[1][i])

    def serialize_agent_data(self):
        agent_data = [self.agents[i].agent for i in range(self.n_agent)]
        
        return agent_data
    
    def dump_agent_obj(self,fl_name):
        with open(fl_name,'w+') as op:
            json.dump(self.serialize_agent_data(),op)

def dump_data(dic_t ,fl_name):
    with open(fl_name,'w+') as op:
        json.dump(dic_t,op)


def load_pickle_obj_list(file_name,bin):
    f = open(file_name,"rb+")
    objs = []
    count = 1
    #create_dir
    folder_name=os.path.splitext(file_name)[0]

    try:  
        os.mkdir(folder_name)
    except OSError:  
        print ("Creation of the directory %s failed" % folder_name)
    else:  
        print ("Successfully created the directory %s " % folder_name)

    while 1:
        try:

            objs.append(pickle.load(f))
            if count%bin == 0:
                grid=grid_obj()
                agents = agent_obj()
                grid.append_cell(objs)
                agents.append_agent(objs)
                data={"grid":grid.serialize_data() ,"agent":agents.serialize_agent_data()}
                dump_data(data,folder_name+"/_"+str(count)+".json")
                objs.clear()


            count += 1
        except EOFError:
            break
    #return objs