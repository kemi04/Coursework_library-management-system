from tkinter import *
from bookcheckout import *
from bookreturn import *
from booksearch import *
from bookweed import *
from pathlib import Path

# Global declarations of the GUI elements
menu = Tk()
title = Label(menu)
checkOutButton = Button(menu)
returnButton = Button(menu)
removeButton = Button(menu)
searchButton = Button(menu)

def getScreenWidth():
    """Returns the width of a screen."""
    global menu
    return menu.winfo_screenwidth()

def getScreenHeight():
    """Returns the height of a screen."""
    global menu
    return menu.winfo_screenheight()
    
def createWindow():
    """Creates the menu window and its GUI elements."""
    menu.title("Library Management System")
    size = str(getScreenWidth())+ "x" + str(getScreenHeight())
    menu.geometry(size)
    menu.configure(background = 'grey75')
    title.config(text = "Library Management System", font=("Courier", 22, 
                                               'bold', 'italic'), bg = 'grey75')
    title.grid(columnspan = 4, padx = (getScreenWidth() - title.winfo_reqwidth()) / 2, 
        pady = (getScreenHeight() * 0.3, getScreenHeight() * 0.15), row = '0', 
                                                                    column = '0')
    checkOutButton.grid(column = '0', row = '1')
    returnButton.grid(column = '1', row = '1')
    removeButton.grid(column = '2', row = '1')
    searchButton.grid(column = '3', row = '1')
    checkOutButton.config(text = "Check out a book", width = 20, command = 
                          lambda: checkOutBook())
    returnButton.config(text = "Return a book", width = 20, command = 
                        lambda: returnBookUpdate())
    removeButton.config(text = "Remove a book", width = 20, command = 
                        lambda: removeBook())
    searchButton.config(text = "Search for a book", width = 20, command = 
                        lambda: createGUI())


def checkFile():
    """Checks if the database and log files exist. If not, they are created blank."""
    file = Path("database.txt")
    if not(file.is_file()):
        w = open("database.txt", "w")
        w.close()
    file = Path("logfile.txt")
    if not(file.is_file()):
        w = open("logfile.txt", "w")
        w.close()
    

checkFile()
createWindow()
menu.mainloop()