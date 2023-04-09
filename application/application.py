from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from tkinter import ttk
import pprint
import io
import time
import random
import scipy
from application import components1


class Application:  

    def __init__(self):
        self.window = Tk()
        self.df = pd.DataFrame
        self.ref_df = pd.DataFrame
        self.df_x = pd.DataFrame
        self.df_y = pd.DataFrame
        self.pathh = Entry(self.window)
        self.window.title('Visulization Tool')
        self.window.geometry("1200x800")
        self.frame1 = Frame(self.window,height=250,width=1200,highlightbackground="blue", highlightthickness=2)
        self.frame1.pack(padx=5, pady=5,fill=None, expand=False)
        self.frame1.pack_propagate(0)
        
        self.frame2 = Frame(self.window,height=550,width=1200,highlightbackground="blue", highlightthickness=2)
        self.frame2.pack(padx=5, pady=5, fill=None, expand=False)
        self.frame2.pack_propagate(0)
        self.buffer = io.StringIO()
        self.plot_list = []
        self.uni_plot_list = ['hist','line','box', 'density']
        self.bi_plot_list = ['scatter','box','area','barh','bar','line']
        self.group_plot_list = ['pie','scatter','barh','box','line','area','bar']
        self.multi_plot_list = ['scatter','area']
        self.function = StringVar()
        self.subplot = StringVar()
        self.transpose = StringVar()
       
       

    def openFile(self):
        """To open the file and initialize the dataframe"""
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()

        tf = filedialog.askopenfilename(
            initialdir="C:/Users/MainFrame/Desktop/", 
            title="Open Text file", 
            filetypes=(("Text Files", "*.csv"),("Text Files", "*.dat"),)
            )
        
        self.pathh.insert(END, tf)
        print(tf)

        self.read_csv(tf)  # or tf = open(tf, 'r')
        

    def plot(self,frame):
        """Function to plot the graph"""
        
    
        # the figure that will contain the plot
        fig = plt.Figure(figsize = (5, 5),
                    dpi = 100)
    
        # list of squares
        bar1 = FigureCanvasTkAgg(fig, frame)
        
    
    
        # adding the subplot
        ax1 = fig.add_subplot(111)
        patient_gl = self.df[["PtID", "Gl"]]
        df1 = patient_gl.groupby('PtID').mean()
        df1.plot(kind='bar', legend=True,ax=ax1,title="Glucose level vs Patients")

        
        bar1.draw()
    
        # placing the canvas on the Tkinter window
        bar1.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.window)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        bar1.get_tk_widget().pack()


        

    

       
        
      
    
        # plotting the graph	
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        # canvas = FigureCanvasTkAgg(fig,
        #                            master = window)  
       
    
        # # placing the canvas on the Tkinter window
        # canvas.get_tk_widget().pack()
    
        # # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(canvas,
        #                                window)
        # toolbar.update()
    
        # # placing the toolbar on the Tkinter window
        # canvas.get_tk_widget().pack()

    def execute_app(self):
        """Function to  build the UI"""

       
        
        # button that displays the plot
        # plot_button = Button(self.frame1, 
        #                     command = lambda: self.plot(frame2),
        #                     height = 2, 
        #                     width = 10,
        #                     text = "Plot")
        
        # self.frame2.pack()
        
        # # place the button 
        # # in main window
        # plot_button.pack()
        
        button_open = Button(self.frame1,anchor='w',pady=5,
        text="Open File", 
        command=self.openFile
        )
        button_open.place(x=1,y=1)
        button_open.pack_propagate(0)
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        self.window.mainloop()
        self.window.mainloop()


    def read_csv(self,file):
        """Function to read csv into dataframe"""
        print(file)
        error_label = Label(self.frame2,text="",width=40,height=40)
        error_label.place(x=1,y=1)
        error_label.pack( side= TOP, anchor=W)

        progressbar=ttk.Progressbar(self.frame1,orient=HORIZONTAL, length = 200)
        progressbar.pack()
        progressbar.config(mode = 'indeterminate',value=50)
       
        progressbar.start()

        

        try:
            self.df = pd.read_csv(file)
        except Exception as err:
            error_label.config(text=err)
            progressbar.destroy()
            return
    
        if(self.df.size > 0):
            self.df=self.df.reset_index()
            #self.ref_df = df.copy()
            self.df.info(buf = self.buffer)
            show_text = self.buffer.getvalue()



            # show_text = pprint.pformat(show_text,indent=14,width=120)
            # show_text = show_text.join(pprint.pformat(self.df.head(10),indent=4))
            
            error_label.config(text=show_text)
            progressbar.stop()
            progressbar.destroy()
            self.show_tools()

    def show_tools(self):
        if self.df.size == 0:
            return
        
        cols = self.df.columns

        tuple_x =()
        tuple_y =()
       
      
       
        
        list_frame1 = Frame(self.frame1,height=200,width=120,highlightbackground="blue", highlightthickness=1)
        list_frame1.place(x=80,y=1)
        list_frame1.pack_propagate(0)
        #list_frame1.pack(padx=5, pady=5, fill=None, expand=False)
       
        label_x = Label(list_frame1,text="Choose x",width=20,height=1)
        label_x.pack()
        yscrollbar_x = Scrollbar(list_frame1)
        yscrollbar_x.pack(side = RIGHT, fill = Y)
        xscrollbar_x = Scrollbar(list_frame1)
        xscrollbar_x.pack(side = BOTTOM, fill = X)
        list_x = Listbox(list_frame1, selectmode = "multiple", 
               yscrollcommand = yscrollbar_x.set, xscrollcommand = xscrollbar_x.set )
        #list_x.bind('aaa',lambda : tuple_x(list_x.curselection()))
        list_x.pack(
          expand = YES, fill = "both")
        for num,item in enumerate(cols):
            list_x.insert(END, item)
            list_x.itemconfig(num, bg = "lime")
  

        yscrollbar_x.config(command = list_x.yview)
        xscrollbar_x.config(command = list_x.xview)

        global var_x
        var_x=[]
        def set_var_x(ls):
            global var_x
            var_x=list(ls)
            list_x.selection_clear(0, 'end')
        button_x= Button(self.frame1,text="Set X",
        command=lambda: set_var_x(list_x.curselection()))
        button_x.place(x=115,y=210)
        button_x.pack_propagate(0)
        


        #---------------------------------------
        list_frame2 = Frame(self.frame1,height=200,width=120,highlightbackground="blue", highlightthickness=1)
        list_frame2.place(x=220,y=1)
        list_frame2.pack_propagate(0)
        #list_frame1.pack(padx=5, pady=5, fill=None, expand=False)
       
        label_y = Label(list_frame2,text="Choose y",width=20,height=1)
        label_y.pack()
        yscrollbar_y = Scrollbar(list_frame2)
        yscrollbar_y.pack(side = RIGHT, fill = Y)
        xscrollbar_y = Scrollbar(list_frame2)
        xscrollbar_y.pack(side = BOTTOM, fill = X)
        list_y = Listbox(list_frame2, selectmode = "multiple", 
               yscrollcommand = yscrollbar_y.set, xscrollcommand = xscrollbar_y.set)
        list_y.pack(
          expand = YES, fill = "both")
        for num,item in enumerate(cols):
      
            list_y.insert(END, item)
            list_y.itemconfig(num, bg = "lime")
  

        yscrollbar_y.config(command = list_y.yview)
        xscrollbar_y.config(command = list_y.xview)
        global var_y
        var_y=[]
        def set_var_y(ls):
            global var_y
            var_y=list(ls)
            list_y.selection_clear(0, 'end')
        button_y= Button(self.frame1,text="Set Y",
        command=lambda: set_var_y(list_y.curselection()))
        button_y.place(x=255,y=210)
        button_y.pack_propagate(0)



        #---------------------------------------

        list_frame3 = Frame(self.frame1,height=200,width=120,highlightbackground="blue", highlightthickness=1)

        list_frame3.place(x=360,y=1)
        list_frame3.pack_propagate(0)
        #list_frame1.pack(padx=5, pady=5, fill=None, expand=False)
       
        label_x = Label(list_frame3,text="Plots",width=20,height=1)
        label_x.pack()
        yscrollbar = Scrollbar(list_frame3)
        yscrollbar.pack(side = RIGHT, fill = Y)
        xscrollbar = Scrollbar(list_frame3)
        xscrollbar.pack(side = BOTTOM, fill = X)
        list_plots = components1.Components1().create_filter(list_frame3,yscrollbar.set,xscrollbar.set)
        # list_plots = Listbox(list_frame3, selectmode = "single", 
        #        yscrollcommand = yscrollbar.set, xscrollcommand = xscrollbar.set)
        # list_plots.pack(
        #   expand = YES, fill = "both")
        
        # for num,item in enumerate(self.plot_list):
      
        #     list_plots.insert(END, item)
        #     list_plots.itemconfig(num, bg = "lime")
  

        yscrollbar.config(command = list_plots.yview)
        xscrollbar.config(command = list_plots.xview)




        global var_plot
        var_plot =[] 
        def set_var_plot(ls):
            global var_plot
            print(ls)
            var_plot=list(ls)
            print(type(var_plot))
            print(var_plot)
            list_plots.selection_clear(0, 'end')
            list_plots.delete(0, 'end')
            button_plot["state"] = NORMAL
            button_plt["state"] = DISABLED

            

        
        # for num,item in enumerate(self.plot_list):
      
        #     list_plots.insert(END, item)
        #     list_plots.itemconfig(num, bg = "lime")
        def chk_plot(list_plotsp):
            list_plots.delete(0, 'end')

            if len(var_x)<1 and len(var_y)<1 :
                messagebox.showerror("showerror", "select at least one x and y")
                
            elif len(var_x)>=1 and len(var_y)>1 and self.function.get() == 'group by':
                for num,item in enumerate(self.multi_plot_list):
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg = "lime")
                self.plot_list = self.multi_plot_list
                button_plt["state"] = NORMAL
            
                
    
            elif len(var_x)==1 and len(var_y)==1 and self.function.get() == 'group by':
                for num,item in enumerate(self.bi_plot_list):
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg = "lime")
                self.plot_list = self.bi_plot_list
                button_plt["state"] = NORMAL

            elif (len(var_x)==0 and len(var_y)==1) or (len(var_x)==1 and len(var_y)==0) :
                for num,item in enumerate(self.uni_plot_list):
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg = "lime")
                self.plot_list = self.uni_plot_list
                button_plt["state"] = NORMAL
            elif (len(var_x)>=1 and len(var_y)>=1 and self.function.get() != 'group by'):
                    for num,item in enumerate(self.group_plot_list):
                        list_plotsp.insert(END, item)
                        list_plotsp.itemconfig(num, bg = "lime")
                    self.plot_list = self.group_plot_list
                    button_plt["state"] = NORMAL
                

                
            
            else :
                messagebox.showerror("showerror","No options for plots are matched for selected x,y")
               

            


        button_chk_plt= Button(self.frame1,text="Check Available Plot",
        command=lambda: chk_plot(list_plots))
        button_chk_plt.place(x=360,y=210)
        button_chk_plt.pack_propagate(0)
       

    #-------------------------------------------------


        


        
        fun_combobox = ttk.Combobox(self.frame1, textvariable=self.function)
        fun_combobox.place(x=500,y=1)
        fun_combobox.pack_propagate(0)
        fun_combobox.config(values=('sum','avg','min','max','count','group by'))
        self.function.set('group by')

        


        subplot_combobox = ttk.Combobox(self.frame1, textvariable=self.subplot)
        subplot_combobox.place(x=500,y=50)
        subplot_combobox.pack_propagate(0)
        subplot_combobox.config(values=('normal','subplot'))
        self.subplot.set('normal')

        tran_combobox = ttk.Combobox(self.frame1, textvariable=self.transpose)
        tran_combobox.place(x=500,y=100)
        tran_combobox.pack_propagate(0)
        tran_combobox.config(values=('transpose','no transpose'))
        self.transpose.set('no transpose')



        button_plt= Button(self.frame1,text="Set Plot",
        command=lambda: set_var_plot(list_plots.curselection()))
        button_plt.place(x=490,y=210)
        button_plt.pack_propagate(0)
        button_plt["state"] = DISABLED







        def control(var_xp,var_yp,var_plotp):
            self.plot_control(var_xp,var_yp,self.plot_list[var_plotp[0]])
            global var_x
            global var_y
            global var_plot
            var_x = []
            var_y = []
            var_plot = []
            self.function.set('group by')
            button_plt["state"] = DISABLED
            button_plot["state"] = DISABLED



        #----------------------------------------
        button_plot= Button(self.frame1,anchor='e',pady=5,
        text="  PLOT  ",
        command=lambda: control(var_x,var_y,var_plot))
        button_plot.place(x=1130,y=210)

        button_plot.pack_propagate(0)
        button_plot["state"] = DISABLED

        
    def apply_function(self,col_x,col_y,fun):

        cols_y = []
        cols_x = []
        for i in col_y:
            cols_y.append(self.df.columns[i])
        
        for i in col_x:
            cols_x.append(self.df.columns[i])

        for val in cols_x:
            if val not in cols_y:
                cols_y.append(val)
        print(cols_y)
        try:
            if fun == 'sum':
                self.ref_df= self.df[cols_y].groupby(cols_x).sum()

            elif fun == 'avg':
                self.ref_df= self.df[cols_y].groupby(cols_x).mean()
            elif fun == 'min':
                self.ref_df= self.df[cols_y].groupby(cols_x).min()
            elif fun == 'max':
                self.ref_df= self.df[cols_y].groupby(cols_x).max()
            elif fun == 'count':
                self.ref_df= self.df[cols_y].groupby(cols_x).count()
        except:
            print("function did not work")


        if self.transpose.get()=='transpose':
            self.ref_df = self.ref_df.T
            print(self.ref_df)

        
        
       
            



    
    def plot_test(self,x,y):
        cols = self.df.columns
        print(type(x))
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        
        fig = plt.Figure(figsize = (5, 5),
                    dpi = 80)
    
        # list of squares
        bar1 = FigureCanvasTkAgg(fig, self.frame2)
        
    
    
        # adding the subplot
        ax1 = fig.add_subplot(1,1,1)
        var1 = ""
        for j in x:
            if cols[j] != None:
                var1 = cols[j]
                break


        #df1 = self.df[var1]
        print("Printing variable")
        print(var1)

      
        
        self.df.plot(kind='scatter',y=var1,x='index', legend=True,ax=ax1,title="Glucose level vs Patients")

        
        
       
        
        bar1.get_tk_widget().config(width=1200,height=500)
        bar1.draw()

        bar1.get_tk_widget().pack()
    
        # placing the canvas on the Tkinter window
        
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.frame2)
        toolbar.update()
        
    
        # placing the toolbar on the Tkinter window
        
        
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)

    def plot_control(self,argsx,argsy,plot):
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        print(argsx)
        print(argsy)
        if self.function.get() != 'group by':
            self.apply_function(argsx,argsy,self.function.get())
        else:
            self.ref_df=self.df
        print(argsx)
        print(argsy)
        print(plot)
        if len(argsx)<1 and len(argsy)<1:
            messagebox.showerror("showerror","Select at least one x and y to get the plot")
            
        
        elif len(argsx)==1 and len(argsy)==1 and self.function.get() == 'group by':
            self.bi_plot(argsx[0],argsy[0],plot)
            print("reacing bi")
        elif (len(argsx)==0 and len(argsy)==1) or (len(argsx)==1 and len(argsy)==0) :
            args = argsx[0] if len(argsx) > len(argsy) else argsy[0]
            print(args)
            self.uni_plot(args,plot)
        elif (len(argsx)>=1 and len(argsy)>=1 and self.function.get() != 'group by'):
           
            self.group_plot(argsx,argsy,plot)
           
        
        elif len(argsx)>=1 and len(argsy)>=1:
            print("smulti")

            self.multi_plot(argsx,argsy,plot)
            
        else :
            messagebox.showerror("showerror","No options matched for selected x and y")
            
        
    
    def uni_plot(self,args,plot):
        col_head = self.df.columns[args]
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        
        fig = plt.Figure(figsize = (5, 5),
                    dpi = 80)
        
        bar1 = FigureCanvasTkAgg(fig, self.frame2)

        ax1 = fig.add_subplot(111)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        try:
            if plot=='hist':
                self.df[col_head].plot(kind=plot, legend=True,title=f"Histogram {col_head}" ,xlabel=col_head,ylabel="Frequency",edgecolor='black',ax=ax1,color=colors[random.randint(0,len(colors)-1)])
            elif plot=='density':
                self.df[col_head].plot(kind='density', legend=True,title=f"Density {col_head}" ,color=colors[random.randint(0,len(colors)-1)],xlabel=col_head,ylabel="Density",ax=ax1)
            elif plot =='box':
                self.df[col_head].plot(kind='box', legend=True,title=f"Box {col_head}" ,color=colors[random.randint(0,len(colors)-1)],xlabel="",ylabel=col_head,ax=ax1)
            elif plot=='line':
                self.df[col_head].plot(kind=plot, legend=True,title=f"Line {col_head}" ,xlabel=col_head,ylabel="Value",ax=ax1,color=colors[random.randint(0,len(colors)-1)])
           
        except Exception as error:
            messagebox.showerror("showerror",error)
          
            # error_label.config(text=f"Argument {col_head} type does not support histogram")
            # error_label.pack_propagate(0)
            return
        bar1.get_tk_widget().config(width=1200,height=500)
        bar1.draw()

        bar1.get_tk_widget().pack()
    
        # placing the canvas on the Tkinter window
        
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.frame2)
        toolbar.update()
        
    
        # placing the toolbar on the Tkinter window
        
        
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)


    def bi_plot(self,argx,argy,plot):
        print("reaching bi")
        print(argx)
        print(argy)
        print(plot)
        col_head_x = self.df.columns[argx]
        col_head_y = self.df.columns[argy]
        print(col_head_x)
        print(col_head_y)
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        
        fig = plt.Figure(figsize = (5, 5),
                    dpi = 80)
        
        bar1 = FigureCanvasTkAgg(fig, self.frame2)



        ax1 = fig.add_subplot(111)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        try:
            if plot=='scatter':
                self.ref_df.plot(kind=plot,x=col_head_x,y=col_head_y, legend=True,title=f"Scatter {col_head_y} VS {col_head_x}" ,xlabel=col_head_x,ylabel=col_head_y,ax=ax1,color=colors[random.randint(0,len(colors)-1)])
            elif plot=='bar':
                self.ref_df.plot(kind=plot,x=col_head_x,y=col_head_y, edgecolor='black',legend=True,title=f"Bar {col_head_y} VS {col_head_x}" ,xlabel=col_head_x,ylabel=col_head_y,ax=ax1,color=colors[random.randint(0,len(colors)-1)])
            elif plot=='barh':
                self.ref_df.plot(kind=plot,x=col_head_x,y=col_head_y,edgecolor='black', legend=True,title=f"Bar Horizontal {col_head_y} VS {col_head_x}" ,xlabel=col_head_x,ylabel=col_head_y,ax=ax1,color=colors[random.randint(0,len(colors)-1)])
            elif plot =='box':
                self.ref_df.plot(kind='box',x=col_head_x,y=col_head_y, legend=True,title=f"Box Horizontal {col_head_y} VS {col_head_x}" ,color=colors[random.randint(0,len(colors)-1)],xlabel=col_head_x,ylabel=col_head_y,ax=ax1)
            elif plot=='line':
                self.ref_df.plot(kind=plot,x=col_head_x,y=col_head_y, legend=True,title=f"Line {col_head_x} VS {col_head_y}" ,xlabel=col_head_x,ylabel=col_head_y,ax=ax1,color=colors[random.randint(0,len(colors)-1)])
            elif plot=='area':
                self.ref_df.plot(kind=plot,x=col_head_x,y=col_head_y, legend=True,title=f"Area {col_head_x} VS {col_head_y}" ,xlabel=col_head_x,ylabel=col_head_y,ax=ax1,color=colors[random.randint(0,len(colors)-1)])
        
        except Exception as error:
            messagebox.showerror("showerror",error)
            
            # error_label.config(text=f"Argument {col_head} type does not support histogram")
            # error_label.pack_propagate(0)
            return
        bar1.get_tk_widget().config(width=1200,height=500)
        bar1.draw()

        bar1.get_tk_widget().pack()
    
        # placing the canvas on the Tkinter window
        
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.frame2)
        toolbar.update()
        
    
        # placing the toolbar on the Tkinter window
        
        
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)
    
    def multi_plot(self,argx,argy,plot):

        col_head_x = [self.df.columns[x] for x in argx]
        col_head_y = [self.df.columns[x] for x in argy]
        print(col_head_x)
        print(col_head_y)
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        

        global new_ax_sub
        global fig
        global new_ax_nor
       
        
       

        if self.subplot.get() == 'subplot':
            global new_ax_sub
            global fig

            fig, new_ax_sub = plt.subplots(nrows=len(argx), ncols=len(argy), figsize=(5, 5))
            plt.subplots_adjust(hspace=0.5)
            new_ax_sub= new_ax_sub.ravel()
            
        else:
            global new_ax_nor
            fig, new_ax_nor = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
            


        bar1 = FigureCanvasTkAgg(fig, self.frame2)
        
        fig.suptitle(f"All Plots {col_head_x.__str__()} VS {col_head_y.__str__()}) ", fontsize=18, y=0.95)

        # loop through tickers and axes
    
        pointer=0
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        try:
            for x in col_head_x:
            
                for y in col_head_y:
                
                # filter df for ticker and plot on specified axes
                    if self.subplot.get() != 'subplot':
                    
                        if plot == 'scatter':
                            self.df.plot(kind=plot, x=x,ax=new_ax_nor,legend=True,y=y,s=0.2 ,color=colors[random.randint(0,len(colors)-1)])
                        elif  plot == 'area': 
                            self.df.plot(kind=plot, x=x,ax=new_ax_nor,legend=True,y=y,color=colors[random.randint(0,len(colors)-1)])
                    
                        
                    else:
                        
                        if plot == 'scatter':

                            self.df.plot(kind=plot, x=x,ax=new_ax_sub[pointer],y=y,s=0.2 ,color=colors[random.randint(0,len(colors)-1)],xlabel=x,ylabel=y)
                        elif plot == 'area ':
                            self.df.plot(kind=plot, x=x,ax=new_ax_sub[pointer],y=y ,color=colors[random.randint(0,len(colors)-1)],xlabel=x,ylabel=y)
                        
                        pointer +=1
                    bar1.draw()
        except Exception as error:
            messagebox.showerror("showerror",error)

            

            # chart formatting
        
        

    

        bar1.get_tk_widget().config(width=1200,height=500)
        

        bar1.get_tk_widget().pack()
    
        # placing the canvas on the Tkinter window
        
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.frame2)
        toolbar.update()
        
    
        # placing the toolbar on the Tkinter window
        
        
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)

    def group_plot(self,argx,argy,plot):
        print("reaching group")
        print(argx)
        print(argy)
        print(plot)
        col_head_x = [self.df.columns[x] for x in argx]
        col_head_y = [self.df.columns[x] for x in argy]
        print(col_head_y)
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        
        fig = plt.Figure(figsize = (5, 5),
                    dpi = 80)
        
        bar1 = FigureCanvasTkAgg(fig, self.frame2)

        ax1 = fig.add_subplot(111)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        print(self.ref_df)

        try:
            if plot=='scatter':
                self.ref_df.reset_Index().plot(kind=plot,x=col_head_x,y=col_head_y, legend=True,title=f"Scatter {col_head_y} VS {col_head_x}" ,xlabel=col_head_x,ylabel=col_head_y,ax=ax1,color=colors[random.randint(0,len(colors)-1)])
            elif plot=='bar':
                self.ref_df.plot(kind=plot,legend=True,title=f"Line {col_head_x} VS {col_head_y}" ,label=True,xlabel=col_head_x,ylabel=col_head_y,ax=ax1)
            elif plot=='barh':
                self.ref_df.plot(kind=plot, legend=True,title=f"Bar Horizontal {col_head_y} VS {col_head_x}",ax=ax1,label=True)
            elif plot=='line':
                self.ref_df.plot(kind=plot,title=f"Line {col_head_x} VS {col_head_y}" ,legend=True,label=True,ax=ax1)
            elif plot == 'pie':
                self.ref_df.plot(kind=plot,y=col_head_y[0],title=f"{plot} chart {col_head_x} VS {col_head_y}",label=True,legend=True,ax=ax1)
            elif plot =='box':
                self.ref_df.plot(kind='box', legend=True,label=True,title=f"Box  {col_head_y} VS {col_head_x}" ,color=colors[random.randint(0,len(colors)-1)],ax=ax1)
            elif plot=='area':
                self.ref_df.plot(kind=plot, legend=True,label=True,title=f"Area {col_head_x} VS {col_head_y}" ,ax=ax1)
        except Exception as error:
            messagebox.showerror("showerror",error)
            # error_label.config(text=f"Argument {col_head} type does not support histogram")
            # error_label.pack_propagate(0)
            return
        bar1.get_tk_widget().config(width=1200,height=500)
        bar1.draw()

        bar1.get_tk_widget().pack()
    
        # placing the canvas on the Tkinter window
        
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.frame2)
        toolbar.update()
        
    
        # placing the toolbar on the Tkinter window
        
        
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)

    def uni_plot1(self,argsx,argsy,args):
        cols = self.df.columns
        for widget in self.frame2.winfo_children():
            print(widget.__str__())
            widget.destroy()
        
        fig = plt.Figure(figsize = (5, 5),
                    dpi = 80)
        
        bar1 = FigureCanvasTkAgg(fig, self.frame2)

        ax1 = fig.add_subplot(111)
        print("axis")
        print(ax1)
        plt.title('Relation between age,bmi and charges')
        plt.xlabel('age and bmi')
        plt.ylabel('charges')
        plt.legend('True')

        row = 1
        col = 1

        if(len(args)%2==0):
            col = len(args)//2
            row = len(args)//col
        else:
            col = len(args)//2 + 1
            row = len(args)//col +1



       
        
        

        
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        
        
        
        for num,var in enumerate(args):
            
            #self.df.plot(kind='scatter',y=var1,x='index', legend=True,ax=ax1,title="Glucose level vs Patients")

            #plt.scatter(self.df['index'],self.df[cols[var]], c=colors[len(args)%8], marker=(len(args)%10)+1, label=cols[var])
            # ax1.plot(kind='scatter'
            #          ,yscale=self.df[cols[var]],xscale=self.df['index'], legend=True,title="Glucose level vs Patients" )
            # ax.set_xlim([0, 1])
            # ax.set_ylim([0, 1])
  
            # ax.set_title('matplotlib.axes.Axes.plot() example 2')
            
            ax1.scatter(self.df['index'],self.df[cols[var]], c=colors[num%8])

        
            
            
        
               
        
        # list of squares
        
        
    
    
        # adding the subplot
        
            
        

        

        bar1.get_tk_widget().config(width=1200,height=500)
        bar1.draw()

        bar1.get_tk_widget().pack()
    
        # placing the canvas on the Tkinter window
        
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(bar1,
                                    self.frame2)
        toolbar.update()
        
    
        # placing the toolbar on the Tkinter window
        
        
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)


        
        





       

       
        
        
        
        
        

        


        

        
    


    

            


        