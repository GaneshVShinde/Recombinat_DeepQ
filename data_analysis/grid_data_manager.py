import os
import json
import pickle

class single_grid_obj_templet:
    def __init__(self):
        self.cell={'isHome': [],
         'isFood': [],
         'homePher': [],
         'foodPher': [],
         'homePherDropCount': [],
         'foodPherDropCount': []    
        }
    def append_cell_data(self,dic):
        self.cell['isHome'].append(dic['isHome'])
        self.cell['isFood'].append(dic['isFood'])
        self.cell['homePher'].append(dic['homePher'])
        self.cell['foodPher'].append(dic['foodPher'])
        self.cell['homePherDropCount'].append(dic['homePherDropCount'])
        self.cell['foodPherDropCount'].append(dic['foodPherDropCount'])

class grid_obj:
    def __init__(self,grid_size=(30,30)):
        self.grid=[[single_grid_obj_templet() 
          for i in range(grid_size[0])] 
         for j in range(grid_size[1])]
        
        self.grid_size = grid_size
        
    def append_cell(self,cell_list):
        for obj in cell_list:
            for i in range(len(obj["grid"])):
                for j in range(len(obj["grid"][i])):
                    self.grid[i][j].append_cell_data(obj["grid"][i][j])
    def serialize_data(self):
        cell_data = [[self.grid[i][j].cell for j in range(self.grid_size[1])]
                    for i in range(self.grid_size[0])
                    ]
        
        return cell_data
    
    def dump_obj(self,fl_name):
        with open(fl_name,'w+') as op:
            json.dump(self.serialize_data(),op)


def load_pickle_obj_list(file_name,bin,folder_to_Store):
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
                grid.append_cell(objs)
                grid.dump_obj(folder_name+"/_"+str(count)+".json")
                objs.clear()


            count += 1
        except EOFError:
            break
    #return objs