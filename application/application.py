from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk
import pprint
import io
import time
import random
import scipy
from app import logger


class Application:
    def __init__(self):
        self.window = Tk()
        self.df = pd.DataFrame
        self.ref_df = pd.DataFrame
        self.df_x = pd.DataFrame
        self.df_y = pd.DataFrame
        self.pathh = Entry(self.window)
        self.window.title("Visulization Tool")
        self.window.geometry("1200x800")
        self.frame1 = Frame(
            self.window,
            height=250,
            width=1200,
            highlightbackground="blue",
            highlightthickness=2,
        )
        self.frame1.pack(padx=5, pady=5, fill=None, expand=False)
        self.frame1.pack_propagate(0)

        self.frame2 = Frame(
            self.window,
            height=550,
            width=1200,
            highlightbackground="blue",
            highlightthickness=2,
        )
        self.frame2.pack(padx=5, pady=5, fill=None, expand=False)
        self.frame2.pack_propagate(0)
        self.buffer = io.StringIO()
        self.plot_list = []
        self.uni_plot_list = ["hist", "line", "box", "density"]
        self.bi_plot_list = ["scatter", "box", "area", "barh", "bar", "line"]
        self.group_plot_list = ["pie", "scatter", "barh", "box", "line", "area", "bar"]
        self.multi_plot_list = ["scatter", "area"]
        self.function = StringVar()
        self.subplot = StringVar()
        self.transpose = StringVar()
        self.fig = None
        self.bar = None

    def execute_app(self):
        """Function to  build the UI components"""
        logger.info("Executing App")

        button_open = Button(
            self.frame1, anchor="w", pady=5, text="Open File", command=self.openFile
        )
        button_open.place(x=1, y=1)
        button_open.pack_propagate(0)

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                logger.info("App closed successfully")
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        self.window.mainloop()

    def openFile(self):
        """To open the file and initialize the dataframe"""
        for widget in self.frame2.winfo_children():
            logger.info("Destroying frame 2 widgets")
            logger.info(widget.__str__())
            widget.destroy()

        tf = filedialog.askopenfilename(
            initialdir="C:/Users/MainFrame/Desktop/",
            title="Open Text file",
            filetypes=(
                ("Text Files", "*.csv"),
                ("Text Files", "*.dat"),
            ),
        )

        self.pathh.insert(END, tf)
        logger.info(f"CSV path {tf}")
        self.read_csv(tf)  # or tf = open(tf, 'r')

    def read_csv(self, file):
        """Function to read csv into dataframe"""
        error_label = Label(self.frame2, text="", width=40, height=40)
        error_label.place(x=1, y=1)
        error_label.pack(side=TOP, anchor=W)

        progressbar = ttk.Progressbar(self.frame1, orient=HORIZONTAL, length=200)
        progressbar.pack()
        progressbar.config(mode="indeterminate", value=50)

        progressbar.start()

        try:
            self.df = pd.read_csv(file)
        except Exception as err:
            logger.error(f"Error while reading CSV file {file} {err}")
            error_label.config(text=err)
            progressbar.destroy()
            return

        if self.df.size > 0:
            self.df = self.df.reset_index()
            self.df.info(buf=self.buffer)
            show_text = self.buffer.getvalue()
            error_label.config(text=show_text)
            progressbar.stop()
            progressbar.destroy()
            logger.info(f"file {file} read successfully displaying tools")
            self.show_tools()

    def show_tools(self):
        """Function to build frames and buttons"""
        if self.df.size == 0:
            logger.error(f"Size of data frame is 0 returning to the window loop")
            return

        cols = self.df.columns

        # Setting frame 1
        list_frame1 = Frame(
            self.frame1,
            height=200,
            width=120,
            highlightbackground="blue",
            highlightthickness=1,
        )
        list_frame1.place(x=80, y=1)
        list_frame1.pack_propagate(0)

        label_x = Label(list_frame1, text="Choose x", width=20, height=1)
        label_x.pack()
        yscrollbar_x = Scrollbar(list_frame1)
        yscrollbar_x.pack(side=RIGHT, fill=Y)
        xscrollbar_x = Scrollbar(list_frame1)
        xscrollbar_x.pack(side=BOTTOM, fill=X)
        list_x = Listbox(
            list_frame1,
            selectmode="multiple",
            yscrollcommand=yscrollbar_x.set,
            xscrollcommand=xscrollbar_x.set,
        )

        list_x.pack(expand=YES, fill="both")
        for num, item in enumerate(cols):
            list_x.insert(END, item)
            list_x.itemconfig(num, bg="lime")

        yscrollbar_x.config(command=list_x.yview)
        xscrollbar_x.config(command=list_x.xview)

        global var_x
        var_x = []

        def set_var_x(ls):
            global var_x
            var_x = list(ls)
            logger.info(f"Columns {var_x.__str__()} selected for frame 1")
            list_x.selection_clear(0, "end")

        button_x = Button(
            self.frame1, text="Set X", command=lambda: set_var_x(list_x.curselection())
        )
        button_x.place(x=115, y=210)
        button_x.pack_propagate(0)
        logger.info(f"Frame1 set")

        # Setting Frame 2
        list_frame2 = Frame(
            self.frame1,
            height=200,
            width=120,
            highlightbackground="blue",
            highlightthickness=1,
        )
        list_frame2.place(x=220, y=1)
        list_frame2.pack_propagate(0)
        label_y = Label(list_frame2, text="Choose y", width=20, height=1)
        label_y.pack()
        yscrollbar_y = Scrollbar(list_frame2)
        yscrollbar_y.pack(side=RIGHT, fill=Y)
        xscrollbar_y = Scrollbar(list_frame2)
        xscrollbar_y.pack(side=BOTTOM, fill=X)
        list_y = Listbox(
            list_frame2,
            selectmode="multiple",
            yscrollcommand=yscrollbar_y.set,
            xscrollcommand=xscrollbar_y.set,
        )
        list_y.pack(expand=YES, fill="both")
        for num, item in enumerate(cols):
            list_y.insert(END, item)
            list_y.itemconfig(num, bg="lime")

        yscrollbar_y.config(command=list_y.yview)
        xscrollbar_y.config(command=list_y.xview)
        global var_y
        var_y = []

        def set_var_y(ls):
            global var_y
            var_y = list(ls)
            logger.info(f"Columns {var_y.__str__()} selected for frame 2")
            list_y.selection_clear(0, "end")

        button_y = Button(
            self.frame1, text="Set Y", command=lambda: set_var_y(list_y.curselection())
        )
        button_y.place(x=255, y=210)
        button_y.pack_propagate(0)
        logger.info(f"frame 2 set")

        # Frame 3

        list_frame3 = Frame(
            self.frame1,
            height=200,
            width=120,
            highlightbackground="blue",
            highlightthickness=1,
        )

        list_frame3.place(x=360, y=1)
        list_frame3.pack_propagate(0)

        label_x = Label(list_frame3, text="Plots", width=20, height=1)
        label_x.pack()
        yscrollbar = Scrollbar(list_frame3)
        yscrollbar.pack(side=RIGHT, fill=Y)
        xscrollbar = Scrollbar(list_frame3)
        xscrollbar.pack(side=BOTTOM, fill=X)
        list_plots = Listbox(
            list_frame3,
            selectmode="single",
            yscrollcommand=yscrollbar.set,
            xscrollcommand=xscrollbar.set,
        )
        list_plots.pack(expand=YES, fill="both")
        list_plots.pack_propagate(0)

        yscrollbar.config(command=list_plots.yview)
        xscrollbar.config(command=list_plots.xview)

        global var_plot
        var_plot = []

        def set_var_plot(ls):
            global var_plot
            var_plot = list(ls)
            logger.info(f"plot {var_plot.__str__()} selected for frame 3")
            list_plots.selection_clear(0, "end")
            list_plots.delete(0, "end")
            button_plot["state"] = NORMAL
            button_plt["state"] = DISABLED

        def chk_plot(list_plotsp):
            list_plots.delete(0, "end")

            if len(var_x) < 1 and len(var_y) < 1:
                logger.error(f"select at least one x and y")
                messagebox.showerror("showerror", "select at least one x and y")

            elif (
                len(var_x) >= 1 and len(var_y) > 1 and self.function.get() == "group by"
            ):
                logger.info(f"Plots for multi plot getting populated")
                for num, item in enumerate(self.multi_plot_list):
                    logger.info(f"{item}")
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg="lime")
                self.plot_list = self.multi_plot_list
                button_plt["state"] = NORMAL

            elif (
                len(var_x) == 1
                and len(var_y) == 1
                and self.function.get() == "group by"
            ):
                logger.info(f"Plot for bi plot getting populated")
                for num, item in enumerate(self.bi_plot_list):
                    logger.info(f"{item}")
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg="lime")
                self.plot_list = self.bi_plot_list
                button_plt["state"] = NORMAL

            elif (len(var_x) == 0 and len(var_y) == 1) or (
                len(var_x) == 1 and len(var_y) == 0
            ):
                logger.info(f"Plot for uni plot getting populated")
                for num, item in enumerate(self.uni_plot_list):
                    logger.info(f"{item}")
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg="lime")
                self.plot_list = self.uni_plot_list
                button_plt["state"] = NORMAL
            elif (
                len(var_x) >= 1
                and len(var_y) >= 1
                and self.function.get() != "group by"
            ):
                logger.info(f"plots for group plot getting populated")
                for num, item in enumerate(self.group_plot_list):
                    logger.info(f"{item}")
                    list_plotsp.insert(END, item)
                    list_plotsp.itemconfig(num, bg="lime")
                self.plot_list = self.group_plot_list
                button_plt["state"] = NORMAL

            else:
                logger.error(
                    f"Plots did not get populated as selected items did not match any plot"
                )
                messagebox.showerror(
                    "showerror", "No options for plots are matched for selected x,y"
                )

        # button to check available plots
        button_chk_plt = Button(
            self.frame1,
            text="Check Available Plot",
            command=lambda: chk_plot(list_plots),
        )
        button_chk_plt.place(x=360, y=210)
        button_chk_plt.pack_propagate(0)

        fun_combobox = ttk.Combobox(self.frame1, textvariable=self.function)
        fun_combobox.place(x=500, y=1)
        fun_combobox.pack_propagate(0)
        fun_combobox.config(values=("sum", "avg", "min", "max", "count", "group by"))
        self.function.set("group by")

        logger.info(f"Function combo box set")

        subplot_combobox = ttk.Combobox(self.frame1, textvariable=self.subplot)
        subplot_combobox.place(x=500, y=50)
        subplot_combobox.pack_propagate(0)
        subplot_combobox.config(values=("normal", "subplot"))
        self.subplot.set("normal")
        logger.info(f"Subplot combo box set")

        tran_combobox = ttk.Combobox(self.frame1, textvariable=self.transpose)
        tran_combobox.place(x=500, y=100)
        tran_combobox.pack_propagate(0)
        tran_combobox.config(values=("transpose", "no transpose"))
        self.transpose.set("no transpose")
        logger.info(f"Transpose combo box set")

        button_plt = Button(
            self.frame1,
            text="Set Plot",
            command=lambda: set_var_plot(list_plots.curselection()),
        )
        button_plt.place(x=490, y=210)
        button_plt.pack_propagate(0)
        button_plt["state"] = DISABLED

        def control(var_xp, var_yp, var_plotp):
            if len(var_plotp) == 0:
                logger.info(f"Plot not selected")
                messagebox.showerror("showerror", "Select one plot")
                return

            self.plot_control(var_xp, var_yp, self.plot_list[var_plotp[0]])
            logger.info(f"Clearing the plot variables passing values to control")
            global var_x
            global var_y
            global var_plot
            var_x = []
            var_y = []
            var_plot = []
            self.function.set("group by")
            self.subplot.set("normal")
            self.transpose.set("no transpose")
            button_plt["state"] = DISABLED
            button_plot["state"] = DISABLED

        # ----------------------------------------
        button_plot = Button(
            self.frame1,
            anchor="e",
            pady=5,
            text="  PLOT  ",
            command=lambda: control(var_x, var_y, var_plot),
        )
        button_plot.place(x=1130, y=210)

        button_plot.pack_propagate(0)
        button_plot["state"] = DISABLED

    def plot_control(self, argsx, argsy, plot):
        logger.info(f"Destroying frame 2 widget before plotting")
        for widget in self.frame2.winfo_children():
            logger.info(f"{widget.__str__()}")
            widget.destroy()

        if self.function.get() != "group by":
            logger.info(f"Applying group by function")
            self.apply_function(argsx, argsy, self.function.get())
        else:
            logger.info(f"Continuing with normal data frame")
            self.ref_df = self.df

        if len(argsx) < 1 and len(argsy) < 1:
            logger.info(f"Select at least one x and y to get the plot")
            messagebox.showerror(
                "showerror", "Select at least one x and y to get the plot"
            )

        elif len(argsx) == 1 and len(argsy) == 1 and self.function.get() == "group by":
            self.bi_plot(argsx[0], argsy[0], plot)
            logger.info(f"Plotting bi plot")

        elif (len(argsx) == 0 and len(argsy) == 1) or (
            len(argsx) == 1 and len(argsy) == 0
        ):
            logger.info(f"Plotting uni plot")
            args = argsx[0] if len(argsx) > len(argsy) else argsy[0]
            self.uni_plot(args, plot)
        elif len(argsx) >= 1 and len(argsy) >= 1 and self.function.get() != "group by":
            logger.info(f"Plotting group plot")
            self.group_plot(argsx, argsy, plot)

        elif len(argsx) >= 1 and len(argsy) >= 1:
            logger.info(f"Plotting multi plot")
            self.multi_plot(argsx, argsy, plot)

        else:
            logger.info(f"No options matched for selected x and y")
            messagebox.showerror("showerror", "No options matched for selected x and y")

    def apply_function(self, col_x, col_y, fun):
        cols_y = []
        cols_x = []
        for i in col_y:
            cols_y.append(self.df.columns[i])

        for i in col_x:
            cols_x.append(self.df.columns[i])

        for val in cols_x:
            if val not in cols_y:
                cols_y.append(val)
        try:
            if fun == "sum":
                self.ref_df = self.df[cols_y].groupby(cols_x).sum()

            elif fun == "avg":
                self.ref_df = self.df[cols_y].groupby(cols_x).mean()
            elif fun == "min":
                self.ref_df = self.df[cols_y].groupby(cols_x).min()
            elif fun == "max":
                self.ref_df = self.df[cols_y].groupby(cols_x).max()
            elif fun == "count":
                self.ref_df = self.df[cols_y].groupby(cols_x).count()
        except:
            logger.error(f"Group by function did not work try again")
            messagebox.showerror(
                "showerror", "Group by function did not work try again"
            )

        if self.transpose.get() == "transpose":
            try:
                self.ref_df = self.ref_df.T
            except:
                logger.error(f"Transpose did not work")
                messagebox.showerror("showerror", "Transpose did not work")

    def uni_plot(self, args, plot):
        col_head = self.df.columns[args]
        for widget in self.frame2.winfo_children():
            widget.destroy()

        self.configure_plot()

        ax1 = self.fig.add_subplot(111)
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        try:
            if plot == "hist":
                self.df[col_head].plot(
                    kind=plot,
                    legend=True,
                    title=f"Histogram {col_head}",
                    xlabel=col_head,
                    ylabel="Frequency",
                    edgecolor="black",
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )
            elif plot == "density":
                self.df[col_head].plot(
                    kind="density",
                    legend=True,
                    title=f"Density {col_head}",
                    color=colors[random.randint(0, len(colors) - 1)],
                    xlabel=col_head,
                    ylabel="Density",
                    ax=ax1,
                )
            elif plot == "box":
                self.df[col_head].plot(
                    kind="box",
                    legend=True,
                    title=f"Box {col_head}",
                    color=colors[random.randint(0, len(colors) - 1)],
                    xlabel="",
                    ylabel=col_head,
                    ax=ax1,
                )
            elif plot == "line":
                self.df[col_head].plot(
                    kind=plot,
                    legend=True,
                    title=f"Line {col_head}",
                    xlabel=col_head,
                    ylabel="Value",
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )

        except Exception as error:
            logger.error(f"Error in  plot{error}")
            messagebox.showerror(
                "showerror",
                "Error in plotting selected variable, please try different plots or variables",
            )
            return
        try:
            self.draw()
        except Exception as error:
            logger.error(f"Error in drawing{error}")
            messagebox.showerror(
                "showerror",
                "Error in drawing the plot on canvas please try different plots or variables",
            )

    def bi_plot(self, argx, argy, plot):
        col_head_x = self.df.columns[argx]
        col_head_y = self.df.columns[argy]

        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.configure_plot()

        ax1 = self.fig.add_subplot(111)
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        try:
            if plot == "scatter":
                self.ref_df.plot(
                    kind=plot,
                    x=col_head_x,
                    y=col_head_y,
                    legend=True,
                    title=f"Scatter {col_head_y} VS {col_head_x}",
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )
            elif plot == "bar":
                self.ref_df.plot(
                    kind=plot,
                    x=col_head_x,
                    y=col_head_y,
                    edgecolor="black",
                    legend=True,
                    title=f"Bar {col_head_y} VS {col_head_x}",
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )
            elif plot == "barh":
                self.ref_df.plot(
                    kind=plot,
                    x=col_head_x,
                    y=col_head_y,
                    edgecolor="black",
                    legend=True,
                    title=f"Bar Horizontal {col_head_y} VS {col_head_x}",
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )
            elif plot == "box":
                self.ref_df.plot(
                    kind="box",
                    x=col_head_x,
                    y=col_head_y,
                    legend=True,
                    title=f"Box Horizontal {col_head_y} VS {col_head_x}",
                    color=colors[random.randint(0, len(colors) - 1)],
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                )
            elif plot == "line":
                self.ref_df.plot(
                    kind=plot,
                    x=col_head_x,
                    y=col_head_y,
                    legend=True,
                    title=f"Line {col_head_x} VS {col_head_y}",
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )
            elif plot == "area":
                self.ref_df.plot(
                    kind=plot,
                    x=col_head_x,
                    y=col_head_y,
                    legend=True,
                    title=f"Area {col_head_x} VS {col_head_y}",
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )

        except Exception as error:
            logger.error(f"Error in  plot{error}")
            messagebox.showerror(
                "showerror",
                "Error in plotting selected variable, please try different plots or variables",
            )
            return
        try:
            self.draw()
        except Exception as error:
            logger.error(f"Error in drawing{error}")
            messagebox.showerror(
                "showerror",
                "Error in drawing the plot on canvas please try different plots or variables",
            )

    def multi_plot(self, argx, argy, plot):
        col_head_x = [self.df.columns[x] for x in argx]
        col_head_y = [self.df.columns[x] for x in argy]

        for widget in self.frame2.winfo_children():
            widget.destroy()

        global new_ax_sub
        global fig
        global new_ax_nor

        if self.subplot.get() == "subplot":
            global new_ax_sub
            global fig

            fig, new_ax_sub = plt.subplots(
                nrows=len(argx), ncols=len(argy), figsize=(5, 5)
            )
            plt.subplots_adjust(hspace=0.5)
            new_ax_sub = new_ax_sub.ravel()

        else:
            global new_ax_nor
            fig, new_ax_nor = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))

        bar1 = FigureCanvasTkAgg(fig, self.frame2)

        fig.suptitle(
            f"All Plots {col_head_x.__str__()} VS {col_head_y.__str__()}) ",
            fontsize=18,
            y=0.95,
        )

        # loop through tickers and axes

        pointer = 0
        colors = ["b", "g", "r", "c", "m", "y", "k"]
        try:
            for x in col_head_x:
                for y in col_head_y:
                    # filter df for ticker and plot on specified axes
                    if self.subplot.get() != "subplot":
                        if plot == "scatter":
                            self.df.plot(
                                kind=plot,
                                x=x,
                                ax=new_ax_nor,
                                legend=True,
                                y=y,
                                s=0.2,
                                color=colors[random.randint(0, len(colors) - 1)],
                            )
                        elif plot == "area":
                            self.df.plot(
                                kind=plot,
                                x=x,
                                ax=new_ax_nor,
                                legend=True,
                                y=y,
                                color=colors[random.randint(0, len(colors) - 1)],
                            )

                    else:
                        if plot == "scatter":
                            self.df.plot(
                                kind=plot,
                                x=x,
                                ax=new_ax_sub[pointer],
                                y=y,
                                s=0.2,
                                color=colors[random.randint(0, len(colors) - 1)],
                                xlabel=x,
                                ylabel=y,
                            )
                        elif plot == "area ":
                            self.df.plot(
                                kind=plot,
                                x=x,
                                ax=new_ax_sub[pointer],
                                y=y,
                                color=colors[random.randint(0, len(colors) - 1)],
                                xlabel=x,
                                ylabel=y,
                            )

                        pointer += 1
                    bar1.draw()
        except Exception as error:
            logger.error(f"Error in  plot{error}")
            messagebox.showerror(
                "showerror",
                "Error in plotting selected variable, please try different plots or variables",
            )
            return

            # chart formatting

        bar1.get_tk_widget().config(width=1200, height=500)

        bar1.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(bar1, self.frame2)
        toolbar.update()
        bar1.get_tk_widget().pack()
        self.frame2.pack_propagate(1)

    def group_plot(self, argx, argy, plot):
        col_head_x = [self.df.columns[x] for x in argx]
        col_head_y = [self.df.columns[x] for x in argy]
        for widget in self.frame2.winfo_children():
            widget.destroy()

        self.configure_plot()

        ax1 = self.fig.add_subplot(111)
        colors = ["b", "g", "r", "c", "m", "y", "k"]

        try:
            if plot == "scatter":
                self.ref_df.reset_Index().plot(
                    kind=plot,
                    x=col_head_x,
                    y=col_head_y,
                    legend=True,
                    title=f"Scatter {col_head_y} VS {col_head_x}",
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                    color=colors[random.randint(0, len(colors) - 1)],
                )
            elif plot == "bar":
                self.ref_df.plot(
                    kind=plot,
                    legend=True,
                    title=f"Line {col_head_x} VS {col_head_y}",
                    label=True,
                    xlabel=col_head_x,
                    ylabel=col_head_y,
                    ax=ax1,
                )
            elif plot == "barh":
                self.ref_df.plot(
                    kind=plot,
                    legend=True,
                    title=f"Bar Horizontal {col_head_y} VS {col_head_x}",
                    ax=ax1,
                    label=True,
                )
            elif plot == "line":
                self.ref_df.plot(
                    kind=plot,
                    title=f"Line {col_head_x} VS {col_head_y}",
                    legend=True,
                    label=True,
                    ax=ax1,
                )
            elif plot == "pie":
                self.ref_df.plot(
                    kind=plot,
                    y=col_head_y[0],
                    title=f"{plot} chart {col_head_x} VS {col_head_y}",
                    label=True,
                    legend=True,
                    ax=ax1,
                )
            elif plot == "box":
                self.ref_df.plot(
                    kind="box",
                    legend=True,
                    label=True,
                    title=f"Box  {col_head_y} VS {col_head_x}",
                    color=colors[random.randint(0, len(colors) - 1)],
                    ax=ax1,
                )
            elif plot == "area":
                self.ref_df.plot(
                    kind=plot,
                    legend=True,
                    label=True,
                    title=f"Area {col_head_x} VS {col_head_y}",
                    ax=ax1,
                )
        except Exception as error:
            logger.error(f"Error in  plot{error}")
            messagebox.showerror(
                "showerror",
                "Error in plotting selected variable, please try different plots or variables",
            )
            return
        try:
            self.draw()
        except Exception as error:
            logger.error(f"Error in drawing{error}")
            messagebox.showerror(
                "showerror",
                "Error in drawing the plot on canvas please try different plots or variables",
            )

    def configure_plot(self):
        self.fig = plt.Figure(figsize=(5, 5), dpi=80)
        self.bar = FigureCanvasTkAgg(self.fig, self.frame2)

    def draw(self):
        self.bar.get_tk_widget().config(width=1200, height=500)
        self.bar.draw()
        self.bar.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(self.bar, self.frame2)
        toolbar.update()
        self.bar.get_tk_widget().pack()
        self.frame2.pack_propagate(1)
