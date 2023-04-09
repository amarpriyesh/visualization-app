from tkinter import *

class Components1:

    def __init__(self):
        pass
        

    def create_filter(self,ws,yscrollcommand,xscrollcommand):
        list_filter = Listbox(ws, selectmode = "single",yscrollcommand=yscrollcommand, xscrollcommand=xscrollcommand)
        list_filter.pack(
          expand = YES, fill = "both")
        list_filter.pack_propagate(0)
        
        # for num,item in enumerate(list_columns):
      
        #     list_filter.insert(END, item)
        #     list_filter.itemconfig(num, bg = "lime")

        return list_filter
   

