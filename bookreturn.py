from tkinter import *
from datetime import *
from bookcheckout import booksNumber, readList, writeToDatabase

#Global declarations of the GUI elements
#They are set to be integers in the beginning and their type is changed after the 
#return form is opened because otherwise
#the return form would be created when the program is launched instead of after a 
#button click in the menu window.
returnForm = 0
error = 0
bookEntry = 0

def createWindow():
    """Creates the return window and its all GUI elements."""
    setFormProperties()
    setLabelProperties()
    setEntryProperties()
    setButtonProperties()

def setButtonProperties():
    """Creates the buttons of the return form and sets their properties."""
    global returnForm
    global btn
    global cncl
    btn = Button(returnForm, command = lambda: returnBook())
    btn.grid(row = '1', column = '1', sticky = "e", padx = (0, 3))
    btn.config(text = "Return", width = 10)
    cncl = Button(returnForm)
    cncl.config(text = "Cancel", command = lambda: closeRet(), width = 10)
    cncl.grid(row = '2', column = '1', sticky = "e", padx = (0, 3), pady = 5)

def setFormProperties():
    """Creates the form and sets its properties."""
    global returnForm
    returnForm = Tk()
    returnForm.title("Return a book")
    returnForm.geometry('500x150')
    returnForm.configure(background = 'grey75')

def setLabelProperties():
    """Creates the label and sets its properties."""
    global returnForm
    global error
    global bookLabel
    error = Label(returnForm)
    bookLabel = Label(returnForm)
    bookLabel.config(text = "Book's ID", width = 21, bg = "grey75")
    bookLabel.grid(row = '0', column = '0', padx = (25, 5), pady = (50, 5), 
                   sticky = "e")

def setEntryProperties():
    """Creates the entry (textbox) and sets its properties."""
    global bookEntry
    global returnForm
    bookEntry = Entry(returnForm)
    bookEntry.grid(row = '0', column = '1', padx = (30, 5), pady = (50, 5))
    bookEntry.config(width = 45)

def closeRet():
    """Closes the return form."""
    global returnForm
    returnForm.destroy()

def returnBookUpdate():
    """Opens the return form."""
    createWindow()
    returnForm.mainloop()

def invalidInput():
    """Checks if user's input ID is valid."""
    global error
    try:
        id = int(bookEntry.get())
        return False, id
    except ValueError:
        error = Label(returnForm)
        error.grid(row = '1', column = '0', columnspan = '2')
        error.config(text = "Invalid book ID", bg = "red", font = 13)
        return True, 0

def writeToLogfileRet(id):
    """Writes data to the logfile.txt file:
    
    id - ID of the returned book (str)."""
    a = open("logfile.txt", 'a')
    a.write(str(id) + " " + str(datetime.now().year) + " " + 
    str(datetime.now().month) + " " + str(datetime.now().day) + " ret\n")
    a.close()

def notTaken():
    """Modifies the label so it shows that a book is not checked out."""
    global error
    error = Label(returnForm)
    error.grid(row = '1', column = '0', columnspan = '2')
    error.config(text = "The book is not taken", bg = "red", font = 13)

def returned(title, author, loanStatus, ID, numberOfBooks, ind):
    """Modifies the label so it shows that a book was returned and additionally 
    calls functions printing data to the text files:    
    
    title - a list of titles (str)
    author - a list of authors (str)
    loanStatus - a list of loan statuses of books (str)
    ID - a list of book IDs (str)
    numberOfBooks - a total number of books in the database.txt file (int)
    ind - the index of the returned book (int)."""
    global error
    global bookEntry
    error = Label(returnForm)
    error.grid(row = '1', column = '0', columnspan = '2')
    error.config(text = "Book returned", bg = "grey75", font = 13)
    loanStatus[ind] = 0
    writeToDatabase(title, author, loanStatus, ID, numberOfBooks)
    writeToLogfileRet(ID[ind])
    bookEntry.delete(0,END)

def isTaken(numberOfBooks, id, title, author, ID, loanStatus):
    """Checks if a book is checked out and checks it as returned if it is 
    checked out.
    
    numberOfBooks - a total number of books in the database.txt file (int)
    title - a list of titles (str)
    author - a list of authors (str)
    loanStatus - a list of loan statuses of books (str)
    ID - a list of book IDs (str)."""
    global error
    global bookEntry
    found = False
    excpt = False
    for i in range (numberOfBooks):
        if (int(ID[i]) == id):
            found = True
            if (int(loanStatus[i]) == 0):
                excpt = True
                notTaken()                    
            else:
                returned(title, author, loanStatus, ID, numberOfBooks, i)
            break
    return found, excpt

def notFound():
    """Modifies the label so it shows that a book with the given ID was not found."""
    global error
    error = Label(returnForm)
    error.grid(row = '1', column = '0', columnspan = '2', rowspan = '2')
    error.config(text = "No such book found", bg = "red", font = 13)


def returnBook():
    """Checks if data is valid and, if it is, marks a book as returned."""
    global bookEntry
    global error
    numberOfBooks = booksNumber()
    title, author, loanStatus, ID = readList()
    found = False
    if (type(error) == Label):
        error.grid_remove()
    excpt, id = invalidInput()
    if (not excpt):
            found, excpt = isTaken(numberOfBooks, id, title, author, ID, loanStatus)
            if (not found and not excpt):
                notFound()