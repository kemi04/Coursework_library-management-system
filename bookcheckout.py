from tkinter import *
from datetime import *

#Global declarations of the GUI elements
#They are set to be integers in the beginning and their type is changed after the
# return form is opened because otherwise
#the return form would be created when the program is launched instead of after 
#a button click in the menu window.
checkoutForm = 0
userEntry = 0
bookEntry = 0
error = 0
btn = 0
success = 0

def booksNumber():
    """Returns the number of books in the database.txt file."""
    i = 0
    r = open("database.txt", "r")
    for lines in r:
        i = i + 0.25
    r.close()
    return int(i)

def createWindow():
    """Creates the checkout window."""
    global checkoutForm
    checkoutForm = Tk()
    checkoutForm.title("Check out a book")
    checkoutForm.geometry('500x200')
    checkoutForm.configure(background = 'grey75')

def createLabels():
    """Creates the labels of the checkout form."""
    global checkoutForm
    global error
    global success
    userLabel = Label(checkoutForm)
    userLabel.config(text = "User ID", width = 21, bg = "grey75")
    userLabel.grid(row = '0', column = '0', padx = (25, 5), pady = (50, 5), 
                   sticky = "e")
    bookLabel = Label(checkoutForm)
    bookLabel.config(text = "Book's ID", width = 20, bg = "grey75")
    bookLabel.grid(row = '1', column = '0', padx = (25, 5), pady = (15, 0), 
                   sticky = "e")
    error = Label(checkoutForm)
    success = Label(checkoutForm)

def createEntries():
    """Creates the entries of the checkout form."""
    global userEntry
    global bookEntry
    userEntry = Entry(checkoutForm)
    userEntry.grid(row = '0', column = '1', padx = (30, 5), pady = (50, 5))
    userEntry.config(width = 45)
    bookEntry = Entry(checkoutForm)
    bookEntry.config(width = 45)
    bookEntry.grid(row = '1', column = '1', padx = (30, 5), pady = (15, 0))

def createButtons():
    """Creates the buttons of the checkout form."""
    btn = Button(checkoutForm, command = lambda: borrowBook())
    btn.grid(row = '2', column = '1', sticky = "e", padx = (0, 3), pady = 5)
    btn.config(text = "Check out", width = 10)
    cncl = Button(checkoutForm)
    cncl.config(text = "Cancel", command = lambda: closeCheckOut(), width = 10)
    cncl.grid(row = '3', column = '1', sticky = "e", padx = (0, 3))

def createForm():
    """Creates the GUI elements of the checkout window."""
    createWindow()
    createLabels()
    createEntries()
    createButtons()


def closeCheckOut():
    """Closes the checkout form."""
    global checkOutForm
    checkoutForm.destroy()

def clearWindow():
    """Removes all additional (error and success) labels from the form."""
    global error
    global success
    error.destroy()
    success.destroy()

def getUserID():
    """Gets user ID and checks if it is an integer."""
    global userEntry
    global error
    user = userEntry.get()
    excpt = False
    try:
        user = int(user)
    except ValueError:
        excpt = True
        error = Label(checkoutForm)
        error.grid(row = '2', column = '0', columnspan = '2')
        error.config(text = "Invalid user ID", bg = "red", font = 13)
    return user, excpt

def clearEntries():
    """Deletes text from the entries."""
    global userEntry
    global bookEntry
    bookEntry.delete(0,END)
    userEntry.delete(0,END)

def getBookID():
    """Gets book's ID and checks if it is an integer."""
    global bookEntry
    global error
    excpt = False
    book = bookEntry.get()
    try:
        book = int(book)
    except ValueError:
        excpt = True
        error = Label(checkoutForm)
        error.grid(row = '2', column = '0', columnspan = '2')
        error.config(text = "Invalid book ID", bg = "red", font = 13)
    return book, excpt

def findBook(bookID, loanStatus, ID, excpt, user):
    """Searches for a book with a corresponding ID in the list:

    bookID - ID of the book to look for (int)
    loanStatus - a list of loan statuses of books (str)
    ID - a list of IDs of books (str)
    excpt - a variable showing if there were any exceptions (bool)
    user - ID of a user who borrows a book (str)."""""
    global error
    found = False
    numberOfBooks = booksNumber()
    for i in range(numberOfBooks):
        if (int(ID[i]) == int(bookID)):
            found = True
            if (int(loanStatus[i]) != 0 and not excpt):
                excpt = True
                error = Label(checkoutForm)
                error.grid(row = '2', column = '0', columnspan = '2')
                error.config(text = "The book is already borrowed", bg = "red", 
                             font = 13)
                break
            else:
                loanStatus[i] = user
                break
    return found, loanStatus, excpt

def invalidUserID():
    """Modifies the error label to show that the user's ID is invalid."""
    global error
    error = Label(checkoutForm)
    error.grid(row = '2', column = '0', columnspan = '2')
    error.config(text = "Invalid user ID", bg = "red", font = 13)
    return True

def bookNotFound():
    """Modifies the error label to show that the book's ID is invalid."""
    global error
    error = Label(checkoutForm)
    error.grid(row = '2', column = '0', columnspan = '2')
    error.config(text = "No such book found", bg = "red", font = 13)
    return True

def writeToDatabase(title, author, loanStatus, ID, numberOfBooks):
    """Writes data to the database.txt file:
    
    title - a list of titles (str)
    author - a list of authors (str)
    loanStatus - a list of loan statuses of books (str)
    ID - a list of book IDs (str)
    numberOfBooks - a total number of books in the database.txt file (int)."""
    w = open("database.txt", 'w')
    for i in range (int(numberOfBooks)):
        w.write(str(title[i]).strip() + '\n')
        w.write(str(author[i]).strip() + '\n')
        w.write(str(loanStatus[i]).strip() + '\n')
        w.write(str(ID[i]).strip() + '\n')
    w.close()

def writeToLogfileChck(bookID):
    """Writes data to the logfile.txt file:
    
    bookID - ID of the book which is checked out (str)."""
    a = open("logfile.txt", 'a')
    a.write(str(bookID) + " " + str(datetime.now().year) + " " + 
            str(datetime.now().month)
                 + " " + str(datetime.now().day) + " chck\n")
    a.close()

def checkedOut(title, author, loanStatus, ID, bookID):
    """Writes data to files and modifies the labels to show that a book was 
    checked out successfully:
    
    title - a list of titles (str)
    author - a list of authors (str)
    loanStatus - a list of loan statuses of books (str)
    ID - a list of book IDs (str)
    bookID - ID of the book which is checked out (str)."""
    global success
    success = Label(checkoutForm)
    success.grid(row = '2', column = '0', columnspan = '2')
    success.config(text = "Book checked out", bg = "grey75", font = 13)
    numberOfBooks = booksNumber()
    writeToDatabase(title, author, loanStatus, ID, numberOfBooks)
    writeToLogfileChck(bookID)

def borrowBook():
    """Checks if input data is valid and, if it is, modifies data and writes 
    it to the logfile.txt and database.txt files."""
    numberOfBooks = booksNumber()
    title, author, loanStatus, ID = readList()
    clearWindow()
    found = False
    user, excpt = getUserID()
    if not (excpt):
        book, excpt = getBookID()   
        if (not excpt and (user >= 1000 and user <= 9999)):
            found, loanStatus, excpt = findBook(book, loanStatus, ID, excpt, user)
        elif (not excpt):
            excpt = invalidUserID()
        if (not (found) and not (excpt)):
            excpt = bookNotFound()
    if not (excpt):
        checkedOut(title, author, loanStatus, ID, book)
        clearEntries()


def checkOutBook():
    """Opens the checkout form."""
    createForm()
    checkoutForm.mainloop()

def checkOutParticular(titles, authors, loanStatuses, IDs, particular):
    """Opens the checkout form with a locked book ID in the book ID entry:
    
    titles - a list of titles (str)
    authors - a list of authors (str)
    loanStatuses - a list of loan statuses of books (str)
    IDs - a list of book IDs (str)
    particular - ID of a book which was selected to be checked out in the search 
    window."""
    global checkoutForm
    global bookEntry
    createForm()
    bookEntry.insert(0, particular)
    bookEntry.config(state=DISABLED)
    checkoutForm.wait_window(checkoutForm)


def readList():
    """Reads the whole file and returns the lists of titles, authors, loan 
    statuses and IDs"""
    title = []
    author = []
    loanStatus = []
    ID = []
    numberOfBooks = booksNumber()
    r = open("database.txt", 'r')
    for i in range (numberOfBooks):
        title.append(r.readline().strip())
        author.append(r.readline().strip())
        loanStatus.append(r.readline().strip())
        ID.append(r.readline().strip())
    r.close()
    return title, author, loanStatus, ID
