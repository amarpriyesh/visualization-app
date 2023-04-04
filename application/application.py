from tkinter import *
from tkinter import filedialog
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from tkinter import ttk

class Application:  

    def __init__(self):
        self.window = Tk()
        self.df = pd.DataFrame
        self.pathh = Entry(self.window)



    def openFile(self):
        """To open the file and initialize the dataframe"""

        tf = filedialog.askopenfilename(
            initialdir="C:/Users/MainFrame/Desktop/", 
            title="Open Text file", 
            filetypes=(("Text Files", "*.csv"),)
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

        
        
        self.window.title('Plotting in Tkinter')
    
        self.window.geometry("700x700")
        frame1 = ttk.Frame(self.window)
        frame1.config(height=100,width=600)

        frame2 = ttk.Frame(self.window)
        frame2.config(height=600,width=700)
        
        # button that displays the plot
        plot_button = Button(frame1, 
                            command = lambda: self.plot(frame2),
                            height = 2, 
                            width = 10,
                            text = "Plot")
        
    
        
        # place the button 
        # in main window
        plot_button.pack()
        
        Button(frame1,
        text="Open File", 
        command=self.openFile
        ).pack()

        frame1.pack()
        frame2.pack()

    
        # run the gui
        self.window.mainloop()


    def read_csv(self,file):
        """Function to read csv into dataframe"""
        
        print(file)
        self.df = pd.read_csv(file)
        print(self.df.head(10))

        