import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, DISABLED, LEFT, NORMAL, RIGHT, TOP, W, X, END, Y
from tkinter.filedialog import askopenfilename
from utilities.file_io import *
from utilities.constants import CellStatus, CellSize, Algorithm, ScrollConst
from utilities.util_funcs import create_markers, calc_next_indices, get_cells, set_cells, count_cells_marked, validate
from utilities.combination_algos import generate_combination
import pysat_algo
import backtracking_algo
import brute_force_algo
import threading


def GUI():
    root = tk.Tk()
    root.title("Coloring Puzzle - AI HCMUS")

    # General Frame
    control = tk.Frame(root)
    control.pack(padx=10, side=RIGHT)
    top = tk.LabelFrame(control, text="Command")
    top.pack(padx=10, pady=10)
    creditFrame = tk.LabelFrame(control, text="Credit")
    creditFrame.pack(padx=10, pady=10, fill=X)
    bot = tk.LabelFrame(root, text="Puzzle")
    bot.pack(fill=BOTH, expand=True, padx=5, pady=10, side=LEFT)
    foot = tk.Frame(bot)
    foot.pack(fill=X, side=BOTTOM)
    right = tk.Frame(bot)
    right.pack(fill=Y, side=RIGHT)

    # variables for using
    algoMode = ["PySat", "A Star", "Brute Force", "Backtracking", "None"]
    curMode = -1
    matrix = []
    stopFlag = False
    rtFlag = False

    # Function in GUI
    def handleGetFile():  # Get file's path
        path = askopenfilename()
        if len(path) != 0:
            filePath.delete(0, END)
            filePath.insert(0, path)
        return

    def handleDisplayArray():  # Load puzzle array
        nonlocal matrix
        path = filePath.get()
        if len(path) == 0:
            warning.config(text="Please choose file or enter file path first!!!!", fg="red")
            return

        warning.config(text="Loading puzzle .....", fg="blue")
        okButton["state"] = DISABLED
        for widget in array.winfo_children():
            widget.destroy()

        try:
            matrix = read_file(path)
            size = (len(matrix), len(matrix[0]))
        except FileNotFoundError:
            warning.config(text="File does not exist!!!!", fg="red")
            okButton["state"] = NORMAL
            return
        except ValueError:
            warning.config(text="Incorrect file format!!!!", fg="red")
            okButton["state"] = NORMAL
            return

        for i in range(size[0]):
            for j in range(size[1]):
                cell = " "
                if matrix[i][j] != -1:
                    cell = str(matrix[i][j])
                box = tk.Label(
                    array,
                    text=cell,
                    width=CellSize.WIDTH,
                    height=CellSize.HEIGHT,
                    borderwidth=2,
                    relief="solid",
                    font=("Arial", CellSize.FONTSIZE),
                )
                box.grid(row=i, column=j)

        warning.config(text="Load successfully", fg="green")
        okButton["state"] = NORMAL
        return

    def handleSelectAlgo():  # Select algorithm for running
        popup = tk.Tk()
        nonlocal curMode
        mode = tk.StringVar(popup, value=str(curMode))
        popup.title("Select Algorithm")
        titleText = tk.Label(
            popup, text="Please choose one of algorithms below", font=("Arial", 10)
        )
        titleText.pack(padx=10, pady=10)
        optionWrapper = tk.LabelFrame(popup)
        optionWrapper.pack()
        values = (
            ("None", "-1"),
            ("PySat", "0"),
            ("A Star", "1"),
            ("Brute Force", "2"),
            ("Backtracking", "3")
        )

        def onClick():
            return

        def handleConfirm():
            nonlocal curMode
            curMode = int(mode.get())
            algoSelected.config(text="{}".format(algoMode[curMode]))
            popup.destroy()

        for i, item in zip(range(len(values)), values):
            tk.Radiobutton(optionWrapper, text=item[0], variable=mode, value=item[1], command=onClick,).grid(row=0, column=i)
        confirmButton = tk.Button(popup, text="Confirm", command=handleConfirm)
        confirmButton.pack(side=RIGHT, padx=10)
        popup.geometry("450x150+%d+%d" % (root.winfo_screenwidth() / 2 - 225, root.winfo_screenheight() / 2 - 75))
        return

    def renew():
        for widget in array.winfo_children():
            widget.config(bg='white', fg="black")
        return

    def redraw(markers):
        for widget, i in zip(array.winfo_children(), range(len(array.winfo_children()))):
            row = int(i / len(markers[0]))
            col = i - row * len(markers[0])
            color = "green" if markers[row][col] == CellStatus.MARKED else "red"
            widget.config(bg=color, fg="white")
        return

    def changeAllButtonState(state):
        chooseFile["state"] = state
        okButton["state"] = state
        runButton["state"] = state
        clearButton["state"] = state
        algoButton["state"] = state
        return



    def handleRunAlgo():  # Run algorithm to solve the puzzle
        nonlocal stopFlag
        stopFlag = False
        renew()
        if curMode == -1:
            warning.config(text="Please select an algorithm!!!", fg="red")
        else:
            if len(matrix) == 0:
                warning.config(text="Please load the puzzle first!!!", fg="red")
                return
            changeAllButtonState(DISABLED)
            warning.config(text="Running {} .....".format(algoMode[curMode]), fg="blue")

            model = None

            if curMode == Algorithm.PYSAT:
                model = pysat_algo.solve(matrix)
                changeAllButtonState(NORMAL)
            elif curMode == Algorithm.A_STAR:
                warning.config(text="{} has not been implemented yet".format(algoMode[curMode]), fg="red")
                changeAllButtonState(NORMAL)
                return
            elif curMode == Algorithm.BRUTE_FORCE:
                    model = brute_force_algo.solve(matrix)
                    changeAllButtonState(NORMAL)
            elif curMode == Algorithm.BACKTRACKING:
                    model = backtracking_algo.solve(matrix)
                    changeAllButtonState(NORMAL)

            
            if model == None:
                warning.config(text="No solution with {}".format(algoMode[curMode]), fg="green")
            else:
                try:
                    algo_names = ['pysat', 'a_star', 'brute_force', 'backtracking']
                    path = filePath.get().split('/')
                    path[-1] = algo_names[curMode] + '_output.txt'
                    msg = 'Output file: ' + path[-1]
                    write_file('/'.join(path), model, len(matrix), len(matrix[0]))
                except ValueError:
                    msg = 'Cannot write data to file!!!'

                for widget, num in zip(array.winfo_children(), model):
                    color = "green" if num > 0 else "red"
                    widget.config(bg=color, fg="white")
                warning.config(text="Run {} successfully\n{}".format(algoMode[curMode], msg), fg="green")

        return

    def handleClear():  # Clear puzzle
        warning.config(text="Clearing puzzle .....", fg="blue")
        nonlocal matrix
        nonlocal stopFlag
        stopFlag = True
        for widget in array.winfo_children():
            widget.destroy()
        matrix.clear()
        warning.config(text="Clear puzzle successfully", fg="green")
        return

    def handleStop():
        nonlocal stopFlag
        stopFlag = True
        return

    
    # Command frame
    topLeft = tk.Frame(top, width=200, height=100)
    topLeft.pack(side=LEFT, padx=10)
    topRight = tk.Frame(top, width=200, height=100)
    topRight.pack(side=RIGHT, padx=10)

    # Command button (TOP RIGHT)
    chooseFile = tk.Button(topRight, text="Choose File", fg="black", command=handleGetFile, width=13)
    chooseFile.pack(pady=5)

    okButton = tk.Button(topRight, text="Load Puzzle", fg="black", command=handleDisplayArray, width=13)
    okButton.pack(pady=5)

    runButton = tk.Button(topRight, text="Run", command=handleRunAlgo, width=13)
    runButton.pack(pady=5)

    clearButton = tk.Button(topRight, text="Clear Puzzle", fg="black", command=handleClear, width=13)
    clearButton.pack(pady=5)

    stopButton = tk.Button(topRight, text="Stop", fg="black", command=handleStop, width=13)
    stopButton.pack(pady=5)



    # Area for display data
    canvas = tk.Canvas(bot)
    canvas.pack(fill=BOTH, expand=True, side=LEFT)
    scrollY = tk.Scrollbar(right, command=canvas.yview)
    scrollY.pack(fill=Y, expand=True)
    scrollX = tk.Scrollbar(foot, orient="horizontal", command=canvas.xview)
    scrollX.pack(fill=X, expand=True)
    array = tk.Frame(canvas)

    # Bind event for scroll
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    array.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def scrollWithMouse(event):
        canvas.yview_scroll(int(-1 * (event.delta / ScrollConst.MODIFIER)), "units")

    canvas.bind_all("<MouseWheel>", scrollWithMouse)

    # Config scroll
    canvas.configure(yscrollcommand=scrollY.set, xscrollcommand=scrollX.set)

    # Create window frame
    canvas.create_window((0, 0), window=array, anchor="nw")

    # Command Infomation (TOP LEFT)
    pathTitle = tk.Label(topLeft, text="Path:")
    filePath = tk.Entry(topLeft, width=50)
    pathTitle.pack(anchor=W)
    filePath.pack()
    algoBlock = tk.Frame(topLeft)
    algoBlock.pack(fill=X)
    algoTitle = tk.Label(algoBlock, text="Selected Algorithm:")
    algoTitle.pack(side=LEFT)
    algoSelected = tk.Label(algoBlock, text="{}".format(algoMode[curMode]), fg="blue")
    algoSelected.pack(side=LEFT)
    algoButton = tk.Button(algoBlock, text="Select Algorithm", fg="black", command=handleSelectAlgo, width=13)
    algoButton.pack(side=RIGHT, pady=10)

    # Notification while running
    mid = tk.LabelFrame(topLeft, text="Status")
    mid.pack(side=BOTTOM, fill=X)
    warning = tk.Label(mid, text="None", fg="black")
    warning.pack(padx=5, pady=5)

    # Credit
    creditText = tk.Label(creditFrame, text='Project 2: Coloring Puzzle', font=('Arial', 15))
    creditText.pack(padx=10, pady=10)
    creditTextBody1 = tk.Label(creditFrame, text='Programmed by:', font=('Arial', 10))
    creditTextBody1.pack()
    creditTextBody2 = tk.Label(creditFrame, text='Bui Tran Huan - 20127507\nNguyen Van Viet - 20127110\nNguyen Huu Nam - 20127000')
    creditTextBody2.pack(padx=10, pady=5)
    creditTextFooter = tk.Label(creditFrame, text='University Of Science - HCM City', font=('Arial', 10))
    creditTextFooter.pack(padx=10, pady=10)

    # main window size
    width = 1500 if root.winfo_screenwidth() > 1500 else root.winfo_screenwidth()
    height = 900 if root.winfo_screenheight() > 900 else root.winfo_screenheight()
    root.geometry("%dx%d+%d+%d" % (width, height, root.winfo_screenwidth() / 2 - width / 2, root.winfo_screenheight() / 2 - height / 2))
    root.update()
    root.mainloop()
