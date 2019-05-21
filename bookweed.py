from bookcheckout import booksNumber, readList, writeToDatabase
from tkinter import *
from datetime import *
import booksearch

#Global declarations of the GUI elements
#They are set to be integers in the beginning and their type is changed after
# the return form is opened because otherwise
#the return form would be created when the program is launched instead of
# after a button click in the menu window.
removeForm = 0
error = 0

def createEntries():
    """Creates the entry element of the form."""
    global bookEntry
    bookEntry = Entry(removeForm)
    bookEntry.grid(row = '1', column = '1', columnspan = 2, padx = (15, 5),
                  pady = (10, 0))
    bookEntry.config(width = 45)

def createLabels():
    """Creates label elements of the form."""
    global error
    bookLabel = Label(removeForm)
    bookLabel.config(text = "Book's ID", width = 21, bg = 'grey75')
    bookLabel.grid(row = '1', column = '0', padx = (15, 5), pady = (10, 5), 
                   sticky = "e")
    error = Label(removeForm)
    listLabel = Label(removeForm)
    listLabel.config(text = "See the full list of books suggested to be removed", 
                     width = 40, bg = 'grey75')
    listLabel.grid(row = '0', column = '0', columnspan = 2, padx = (5, 0), 
                   pady = (25, 25), sticky = "e")

def createButtons():
    """Creates the button elements of the form."""
    btn = Button(removeForm)
    btn.grid(row = '2', column = '2', sticky = "e", padx = (0, 3), pady = 5)
    btn.config(text = "Remove", command = lambda: delete(), width = 10)
    cncl = Button(removeForm)
    cncl.config(text = "Cancel", command = lambda: closeRemove(), width = 10)
    cncl.grid(row = '3', column = '2', sticky = "e", padx = (0, 3))
    toRemove = Button(removeForm)
    toRemove.config(text = "See the List", command = lambda: 
                    booksearch.booksToRemove(), width = 15)
    toRemove.grid(row = '0', column = '2', sticky = "e", padx = (0, 3))

def createForm():
    """Creates the form window."""
    global removeForm
    removeForm = Tk()
    removeForm.title("Remove a book")
    removeForm.geometry('500x200')
    removeForm.configure(background = 'grey75')

def createWindow():
    """Creates the Remove form with its elements."""
    createForm()
    createLabels()
    createButtons()
    createEntries()


def closeRemove():
    """Closes the Remove form."""
    global removeForm
    removeForm.destroy()


def removeBook():
    """Opens the Remove form."""
    createWindow()
    removeForm.wait_window(removeForm)

def invalidID():
    """Displays the message that the input data is invalid."""
    global error
    error = Label(removeForm)
    error.grid(row = '2', column = '0', columnspan = '2')
    error.config(text = "Invalid book ID", bg = "red", font = 13)
    return True

def deleteBook(numberOfBooks, ind, title, author, loanStatus, ID):
    """Shows the message that a book has been deleted and deletes it from 
    the lists:
    
    numberOfBooks - number of books in the database.txt file
    ind - the index of the book which is to be removed
    title - the list of all titles in the database.txt file
    author - the list of all authors in the database.txt file
    loanStatus - the list of all loanStatuses in the database.txt file
    ID - the list of all IDs in the database.txt file."""
    global error
    error = Label(removeForm)
    error.grid(row = '2', column = '0', columnspan = '2')
    error.config(text = "Book deleted", bg = "grey75", font = 13)
    del(title[ind])
    del(author[ind])
    del(loanStatus[ind])
    del(ID[ind])
    return True

def notFound():
    """Shows the message that a book was not found."""
    global error
    error = Label(removeForm)
    error.grid(row = '2', column = '0', columnspan = '2')
    error.config(text = "No such book found", bg = "red", font = 13)

def findBook(numberOfBooks, title, author, loanStatus, ID, id):
    """Returns a Boolean if a book was found in the database.txt file:
    
    numberOfBooks - number of books in the database.txt file
    ind - the index of the book which is to be removed
    title - the list of all titles in the database.txt file
    author - the list of all authors in the database.txt file
    loanStatus - the list of all loanStatuses in the database.txt file
    ID - the list of all IDs in the database.txt file
    id - user's input ID of a book."""
    global bookEntry
    found = False
    for i in range (numberOfBooks):
        if (int(ID[i]) == id):
            found = deleteBook(numberOfBooks, i, title, author, loanStatus, ID)
            writeToDatabase(title, author, loanStatus, ID,  numberOfBooks - 1)
            bookEntry.delete(0,END)
            break
    return found

def delete():
    """Deletes the book having the user's input ID, otherwise, displays an error 
    message."""
    global error
    numberOfBooks = booksNumber()
    title, author, loanStatus, ID = readList()
    found = False
    error.grid_forget()
    excpt = False
    try:
        id = int(bookEntry.get())
    except ValueError:
        excpt = invalidID()
    if (not excpt):
        found = findBook(numberOfBooks, title, author, loanStatus, ID, id)
    if (not found and not excpt):
        notFound()

def splitLine(line):
    """Takes a line from the logfile.txt and returns its separate elements."""
    id = int(line.split(" ")[0])
    year = int(line.split(" ")[1])
    month = int(line.split(" ")[2])
    day = int(line.split(" ")[3])
    status = line.split(" ")[4]
    return id, year, month, day, status

def isRecommended(year, month, day, status, sugg, id):
    """Returns a list of indices of the books suggested to be removed:
    
    year - year when a book was checked out or returned
    month - month when a book was checked out or returned
    day - day when a book was checked out or returned
    status - a string (either "ret" or "chck" showing if a book was checked 
        out or returned)
    id - ID of the book checked out or returned."""
    first = False
    second = False
    now = datetime.now()
    if (now.year - year > 0 and (now.month - month > 0 or (now.month - month == 0 
                                                         and now.day - day >= 0))):
        first = True
    else:
        first = False
    if (status.strip() == 'chck' and (now.month - month > 3 or (now.month - month 
                                                    == 3 and now.day - day >= 0))):
        second = True
    elif (status.strip() == 'ret'):
        second = False
    if (first or second):
        sugg[id] = True
    else:
        sugg[id] = False
    return sugg

def getList(numberOfBooks, sugg, ID):
    """Returns the list of indices of the books which are suggested to be removed:
    
    numberOfBooks - the number of books in the database.txt file
    sugg - a dictionary of indices of books (keywords) and boolean values of 
    books being not to be removed
    ID - the list of the indices of books."""
    toBeRemoved = []
    for i in range (numberOfBooks):
        try:
            if(sugg[int(ID[i])]):
                toBeRemoved.append(i)
        except KeyError:
            toBeRemoved.append(i)
    return toBeRemoved

def cleanup(IDs):
    """Creates and returns the list of indices of the books which are suggested 
    to be removed:
    
    IDs - IDs of books."""
    title, author, loanStatus, ID = readList()
    ID = IDs
    numberOfBooks = booksNumber()
    sugg = {}
    r = open("logfile.txt", 'r')
    for line in r:
        id, year, month, day, status = splitLine(line)
        sugg = isRecommended(year, month, day, status, sugg, id)
    return getList(numberOfBooks, sugg, ID)