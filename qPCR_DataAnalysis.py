import eel, json, os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from ReformatCapturesID import Captureto96WellFormat, df2excelpd, dfExcel
from openpyxl import load_workbook
# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web')



@eel.expose
def pythonGoButtonClicked():
    root = tk.Tk()
    root.attributes('-topmost', 2)
    root.withdraw()
    filePath = filedialog.askopenfilename()
    root.destroy()
    return filePath

@eel.expose
def df2Newexcel(outputDf, mapAcc = None, accuracy = False, input384 = False):
    root = tk.Tk()
    root.attributes('-topmost', 1)
    root.withdraw()
    filePath = filedialog.asksaveasfile(mode='a', defaultextension = '.xlsx')
    root.destroy()

    dfExcel()

    return filePath, "Complete!!!"



eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)