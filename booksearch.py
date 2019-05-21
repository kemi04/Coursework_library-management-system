from bookweed import cleanup
from bookcheckout import checkOutParticular, readList, booksNumber, writeToDatabase
from tkinter import *
from tkinter import messagebox
from datetime import *
import bookreturn

#Global declarations of the GUI elements
#They are set to be integers in the beginning and their type is changed after 
#the return form is opened because otherwise
#the return form would be created when the program is launched instead of after 
#a button click in the menu window.
form = 0
frameBackground = 0
background = 0
scrl = 0
frameElements = 0
searchLabel = 0
searchBox = 0
searchButton = 0
noResults = 0
emptField = 0
bgColor = 0
titles = []
authors = []
IDs = []
loanStatuses = []
remove = []
checkOut = []
lines = []

def emptySetLabel():
    """Displays the searching form when the searchBox is empty."""
    global emptField
    global noResults
    if (not type(emptField) == Label):
        emptField = Label(frameElements)
        emptField.config(text = "Please enter text to look for. You can input \
IDs of both books and students, titles \
or authors. You can input separate words and look for an author and a title \
simultaneously.\nSearching is case insensitive. \
\nThe most similar results appear at the top of the list.")
        emptField.config(font=("New Times Roman", 13), bg = 'grey75')
        emptField.grid(row = 4, column = 0, columnspan = 10)
    if (type(noResults) == Label):
        noResults.grid_forget()
        noResults = 0

def deleteResults():
    """Clears all results and elements from the form."""
    global titles, authors, loanStatuses, IDs, remove, checkOut, lines, noResults
    while len(titles) > 0:
        titles[0].grid_forget()
        del titles[0]
        authors[0].grid_forget()
        del authors[0]
        loanStatuses[0].grid_forget()
        del loanStatuses[0]
        IDs[0].grid_forget()
        del IDs[0]
        remove[0].grid_forget()
        del remove[0]
        checkOut[0].grid_forget()
        del checkOut[0]
        lines[0].grid_forget()
        del lines[0]
    if (type(noResults) == Label):
        noResults.grid_forget()
        noResults = 0

def searchBoxEmpty():
    """Displays the searching form when the searchbox is empty."""
    emptySetLabel()
    deleteResults()
    return True

def clearEmptyLabel():
    """Removes the label displaying a message that the searchbox is empty."""
    global emptField
    global noResults
    if (type(emptField) == Label):
            emptField.grid_forget()
            emptField = 0
    if (type(noResults) == Label):
        noResults.grid_forget()

def getSearchResult(title, author, ID, loanStatus, numberOfBooks):
    """Gets user's input and compares it with the details of the books' in the 
    database.txt file. Returns lists sorted according similarity:
    
    title - list of titles
    author - list of authors
    ID - list of ID's
    loanStatus - list of loan statuses
    numberOfBooks - a number of books in the database.txt file."""
    global searchBox
    searchValue = search(searchBox.get(), title, author, ID, loanStatus)
    searchValueNew, titleNew, authorNew, loanStatusNew, IDNew = \
    quickSort(0, numberOfBooks, searchValue, title, author, loanStatus, ID)
    return searchValueNew, titleNew, authorNew, IDNew, loanStatusNew
        
def addLabels():
    """Adds label elements to the table."""
    global titles, authors, loanStatuses, IDs
    j = len(titles)
    titles.append(Label(frameElements, width = 44))
    titles[j].config(font=("New Times Roman", 12))
    titles[j].grid(column = 0, row = j + 4, padx = '10', pady = '5', sticky="n")    
    authors.append(Label(frameElements, width = 44))
    authors[j].config(font=("New Times Roman", 12))
    authors[j].grid(column = 1, row = j + 4, padx = '10', pady = '5', sticky="n")
    loanStatuses.append(Label(frameElements, width = 17))
    loanStatuses[j].config(font=("New Times Roman", 12))
    loanStatuses[j].grid(column = 2, row = j + 4, padx = '10', pady = '5', sticky="n")
    IDs.append(Label(frameElements, width = 17)) 
    IDs[j].config(font=("New Times Roman", 12))
    IDs[j].grid(column = 3, row = j + 4, padx = '10', pady = '5', sticky="n")

def addButtons(loanStatus, ind):
    """Adds buttons to the table:
    
    loanStatus - a list of loan statuses of books
    ind - the index of a row."""
    j = len(remove)
    remove.append(Button(frameElements))
    remove[j].grid(column = 4, row = j + 4, padx = '10', pady = '5', sticky="n")
    remove[j].config(text = "Remove", width = '8', command = lambda c = ind: 
                     delBook(c))
    checkOut.append(Button(frameElements))
    checkOut[j].grid(column = 5, columnspan = 2, row = j + 4, padx = '10', 
                     pady = '5', sticky="n")
    if (loanStatus[j] == "0"):
        checkOut[j].config(text = "Check out", width = '13', command = lambda 
                           a = ind: chngBookStatus(a))
    else:
        checkOut[j].config(text = "Return", width = '13', command = lambda 
                           b = ind: chngBookStatus(b))
    lines.append(Frame(frameElements, height=1, width=1400, bg="black"))
    lines[j].grid(columnspan = 8, row = j + 4, column = 0, padx = 10, sticky = 'n')

def addLineSearchForm(loanStatus, ind):
    """Adds a line to the table of the form and fills it with data of a book:
    
    loanStatus - the list of loan statuses of books
    ind - the index of the line."""
    addLabels()
    addButtons(loanStatus, ind)

def setText(title, author, loanStatus, ID, i):
    """Sets text of label and button objects in the table:
    
    title - the list of titles
    author - the list of authors
    loanStatus - the list of loan statuses
    ID - the list of ID's
    i - the index of a line."""
    titles[i].config(text = title[i])
    authors[i].config(text = author[i])
    IDs[i].config(text = ID[i])
    loanStatuses[i].config(text = loanStatus[i])
    if (loanStatus[i] == "0"):
        checkOut[i].config(text = "Check out")
    else:
        checkOut[i].config(text = "Return")

def deleteExcessiveLines(i, ind):
    """If there are more lines in the table, than there are books in the list, 
    it removes the excessive lines:
    
    i - the index of a line
    ind - the number of how many lines were already removed."""
    global titles, authors, loanStatuses, IDs, remove, checkOut, lines
    if (len(titles) > i - ind):
        titles[i - ind].destroy()
        del(titles[i - ind])
        authors[i - ind].destroy()
        del(authors[i - ind])
        IDs[i - ind].destroy()
        del(IDs[i - ind])
        loanStatuses[i - ind].destroy()
        del(loanStatuses[i - ind])
        remove[i - ind].destroy()
        del(remove[i - ind])
        checkOut[i - ind].destroy()
        del(checkOut[i - ind])
        lines[i - ind].destroy()
        del(lines[i - ind])
        ind = ind + 1
    return ind

def displayResults(title, author, loanStatus, ID, numberOfBooks, searchValueNew):
    """Displays searching results in a table, where the most similar results are 
    at the top:
    
    title - the list of titles
    author - the list of authors
    loanStatus - the list of loan statuses
    ID - the list of ID's
    numberOfBooks - number of books in the database.txt file
    searchValueNew - the list of values, showing each book's similarity to user's 
    input."""
    global titles, authors, loanStatuses, IDs, remove, checkOut, lines, emptField
    booksFound = False
    ind = 0
    for i in range (0, numberOfBooks):
            if not(searchValueNew[i] == 0):
                booksFound = True
                if (len(titles) - 1  <= i):
                    j = len(titles) - 1
                    while(len(titles) <= i):
                        addLineSearchForm(loanStatus, i)
                setText(title, author, loanStatus, ID, i)
            else:
                ind = deleteExcessiveLines(i, ind)
    return booksFound

def booksNotFound(booksFound):
    """If no books were found, it displays that no books were found:
    
    booksFound - a Boolean showing if at least one book was found."""
    global noResults
    if not (booksFound):
        noResults = Label(frameElements)
        noResults.config(text = "No results found", bg = 'grey75', font = 
                         ("New Times Roman", 12))
        noResults.grid(row = 5, column = 0, columnspan = 8)

def changeRemoveColour(i, searchValueNew, toBeRemoved):
    """Changes colours of all remove buttons, not associated with a book suggested 
    to be removed, to the default colour:
    
    i - index of a line
    searchValueNew - the list of values, showing each book's similarity to user's 
    input
    toBeRemoved - the list of indices of books, suggested to be removed."""
    global remove
    if (i == 0):
        for z in range(0, toBeRemoved[0]):
            if (searchValueNew[z] > 0):
                remove[z].config(bg = bgColour)
    if (i > 0 and i < len(toBeRemoved) - 1):
        for z in range(toBeRemoved[i - 1] + 1, toBeRemoved[i]):
            if (searchValueNew[z] > 0):
                remove[z].config(bg = bgColour)
    if (i == len(toBeRemoved) - 1):
        for z in range(toBeRemoved[i] + 1, booksNumber()):
            if (searchValueNew[z] > 0):
                remove[z].config(bg = bgColour)

def showSuggested(ID, searchValueNew):
    """Changes colours of all remove buttons, associated with a book suggested 
    to be removed, to red:
    
    ID - the list of ID's
    searchValueNew - the list of values, showing each book's similarity to user's 
    input."""
    global remove
    booksSuggested = False
    toBeRemoved = cleanup(ID)
    i = 0
    if (len(toBeRemoved) > 0):
        for ind in toBeRemoved:
            if (searchValueNew[ind] > 0):
                remove[ind].config(bg = 'red')
                booksSuggested = True
            changeRemoveColour(i, searchValueNew, toBeRemoved)
            i = i + 1

def updateList():
    """Updates the table in the form."""
    global searchBox
    title, author, loanStatus, ID = readList()
    numberOfBooks = booksNumber()
    booksFound = False
    if (searchBox.get() == ""):
        booksFound = searchBoxEmpty()
    else:
        clearEmptyLabel()
        searchValueNew, titleNew, authorNew, loanStatusNew, IDNew = \
        getSearchResult(title, author, loanStatus, ID, numberOfBooks)
        booksFound = \
        displayResults(title, author, loanStatus, ID, numberOfBooks, searchValueNew)
        showSuggested(ID, searchValueNew)
    booksNotFound(booksFound)
    frameBackground.update_idletasks()
    background.config(scrollregion=background.bbox("all"))

def createDeletionForm():
    """Creates the form, where all books, suggested to be removed, are displayed 
    in a table."""
    global form, searchLabel, searchBox, searchButton, emptField
    createGUI()
    form.title("List of suggested to be removed books")
    searchLabel.grid_forget()
    searchBox.grid_forget()
    searchButton.grid_forget()
    emptField.grid_forget()

def addLineRemoveForm():
    """Adds a line to the remove form."""
    global titles, authors, loanStatuses, IDs, remove, lines
    titles.append(Label(frameElements, width = 44))
    authors.append(Label(frameElements, width = 44))
    loanStatuses.append(Label(frameElements, width = 17))
    IDs.append(Label(frameElements, width = 17))
    remove.append(Button(frameElements))
    lines.append(Frame(frameElements, height=1, width=1400, bg="black"))

def setElementPositions(j):
    """Sets elements' positions in the table in a form:
    
    j - the index of a row."""
    global titles, authors, loanStatuses, IDs, remove, lines
    titles[j].grid(column = 0, row = j + 4, padx = '10', pady = '5', sticky="n")
    authors[j].grid(column = 1, row = j + 4, padx = '10', pady = '5', sticky="n")
    loanStatuses[j].grid(column = 2, row = j + 4, padx = '10', pady = '5', sticky="n")
    IDs[j].grid(column = 3, row = j + 4, padx = '10', pady = '5', sticky="n")
    remove[j].grid(column = 4, row = j + 4, padx = '10', pady = '5', sticky="n")
    lines[j].grid(columnspan = 8, row = j + 4, column = 0, padx = 10, sticky = 'n')

def setElementText(title, author, loanStatus, ID, j, ind, toBeRemoved):
    """Sets text of the table elements:
    
    title - the list of titles
    author - the list of authors
    loanStauts - the list of loan statuses
    ID - the list of ID's
    j - the index of a row
    ind - the index of title, author, loanStatus and ID lists
    toBeRemoved - the list of indices of the books suggested to be removed."""
    titles[j].config(text = title[ind], font=("New Times Roman", 12))
    authors[j].config(text = author[ind], font=("New Times Roman", 12))
    loanStatuses[j].config(text = loanStatus[ind], font=("New Times Roman", 12))
    IDs[j].config(text = ID[ind], font=("New Times Roman", 12))
    remove[j].config(text = "Remove", width = '8', command = lambda c = 
                     toBeRemoved[j]: delBook2(c))
    remove[j].config(bg = 'red')


def fillTable(toBeRemoved, title, author, loanStatus, ID):
    """Fills the table in a form with data of the books in the database.txt file:
    
    title - the list of titles
    author - the list of authors
    loanStauts - the list of loan statuses
    ID - the list of ID's."""
    j = 0
    if (len(toBeRemoved) > 0):
        for ind in toBeRemoved:
            addLineRemoveForm()
            setElementPositions(j)
            setElementText(title, author, loanStatus, ID, j, ind, toBeRemoved)
            j = j + 1
    else:
        noResult = Label(frameElements, width = 44)
        noResult.config(text = "No books are suggested to be removed.", 
                        font=("New Times Roman", 12))
        noResult.grid(column = 0, columnspan = 6, row = j + 4)

def booksToRemove():
    """Creates the form, where all books, suggested to be removed, are displayed 
    in a table."""
    global titles, authors, IDs, loanStatuses, remove, checkOut, lines, searchLabel
    global searchBox, searchButton, form, emptField
    titles = []
    authors = []
    loanStatuses = []
    IDs = []
    remove = []
    checkOut = []
    lines = []
    createDeletionForm()
    createHeader()
    title, author, loanStatus, ID = readList()
    toBeRemoved = cleanup(ID)
    fillTable(toBeRemoved, title, author, loanStatus, ID)
    frameBackground.update_idletasks()
    background.config(scrollregion=background.bbox("all"))

def delBook2(ind):
    """Deletes a book when a remove button is clicked in the form, where the 
    books, suggested to be removed are displayed:
    
    ind - the index of a book."""
    global form
    title, author, loanStatus, ID = readList()
    if (messagebox.askokcancel("Confirm Box","Are you sure you want to remove the \
following book?\n"
 + title[ind] + " by " + author[ind] + " having ID-" + ID[ind], parent=form)):
        del title[ind]
        del author[ind]
        del loanStatus[ind]
        del ID[ind]
        numberOfBooks = booksNumber() - 1
        title, author, loanStatus, ID = quickSortID(0, numberOfBooks, title, 
                                                    author, loanStatus, ID)
        writeToDatabase(title, author, loanStatus, ID, numberOfBooks)
        form.destroy()
        booksToRemove()


def chngBookStatus(ind):
    """Changes the status of a book from checked out to returned or otherwise:

    ind - the index of a book."""
    global form, searchBox
    numberOfBooks = booksNumber()
    title, author, loanStatus, ID = readList()
    searchValue = search(searchBox.get(), title, author, ID, loanStatus)
    searchValue, title, author, loanStatus, ID = quickSort(0, numberOfBooks, 
                                       searchValue, title, author, loanStatus, ID)
    if not (int(loanStatus[ind]) == 0):
        if (messagebox.askokcancel("Confirmation Box","Are you sure you want to \
mark the following book as returned?\n"
 + title[ind] + " by " + author[ind] + " having ID-" + ID[ind], parent=form)):
            loanStatus[ind] = 0
            title, author, loanStatus, ID = quickSortID(0, numberOfBooks, title, 
                                                        author, loanStatus, ID)
            writeToDatabase(title, author, loanStatus, ID, numberOfBooks)
            bookreturn.writeToLogfileRet(ID[ind])
            updateList()
    else:
        checkOutParticular(title, author,loanStatus, ID, ID[ind])
        updateList()


def delBook(ind):
    """Deletes a book from the table and from the database.txt file:

    ind - the index of a book."""
    global form
    numberOfBooks = booksNumber()
    title, author, loanStatus, ID = readList()
    searchValue = search(searchBox.get(), title, author, ID, loanStatus)
    searchValue, title, author, loanStatus, ID = quickSort(0, numberOfBooks, 
                                       searchValue, title, author, loanStatus, ID)
    if (messagebox.askokcancel("Confirm Box","Are you sure you want to remove \
the following book?\n"
 + title[ind] + " by " + author[ind] + " having ID-" + ID[ind], parent=form)):
        del title[ind]
        del author[ind]
        del loanStatus[ind]
        del ID[ind]
        numberOfBooks = booksNumber() - 1
        title, author, loanStatus, ID = quickSortID(0, numberOfBooks, title, 
                                                    author, loanStatus, ID)
        writeToDatabase(title, author, loanStatus, ID, numberOfBooks)
        updateList()

def createForm():
    """Creates the searching window."""
    global form, frameBackground, background, scrl, frameElements
    form = Tk()
    form.title("Search")
    form.config(bg = 'grey75')
    frameBackground = Frame(form)
    frameBackground.grid(row = 2, column = 0, pady = 10, padx = 15, sticky = 'news')
    frameBackground.grid_rowconfigure(0, weight=1)
    frameBackground.grid_columnconfigure(0, weight=1)
    frameBackground.grid_propagate(False)
    frameBackground.config(height = 725, width = 1470, bg = 'grey75')
    background = Canvas(frameBackground)
    background.grid(row=0, column=0, sticky="news")
    scrl = Scrollbar(frameBackground, command=background.yview, orient = VERTICAL)
    scrl.grid(row=0, column=1, sticky='ns')
    frameElements = Frame(background)
    background.create_window((0, 0), window=frameElements, anchor='nw')
    background.configure(yscrollcommand=scrl.set)
    frameElements.config(bg = 'grey75')


def createGUIElements():
    """Creates the GUI elements of the searching form."""
    global searchLabel, searchBox, searchButton, bgColour, emptField, noResults
    searchLabel = Label(frameElements)
    searchLabel.config(text = "Search", font=("Courier", 12), bg = 'grey75')
    searchLabel.grid(row = 1, column = 0, sticky = 'e', pady = (25, 10))
    searchBox = Entry(frameElements)
    searchBox.grid(row = 1, column = 1, columnspan = 2, pady = (25, 10))
    searchBox.config(width = '90')
    searchButton = Button(frameElements, command = lambda: updateList())
    searchButton.grid(row = 1, column = 3, sticky = 'w', pady = (25, 10))
    searchButton.config(text = "Search", width = '15')
    bgColour = searchButton['bg']
    emptField = 0
    noResults = 0


def createGUI():
    """Creates the searching form with its GUI elements."""
    global frameBackground, background, titles, authors, loanStatuses
    global IDs, remove, checkOut, lines
    titles = []
    authors = []
    loanStatuses = []
    IDs = []
    remove = []
    checkOut = []
    lines = []
    createForm()
    createGUIElements()
    frameBackground.update_idletasks()
    background.config(scrollregion=background.bbox("all"), bg = 'grey75')
    createHeader()
    updateList()


def createHeader():
    """Creates the header of the searching form."""
    titleL = Label(frameElements, text="Title", height = '1')
    authorL = Label(frameElements, text = "Author", height = '1')
    IDL = Label(frameElements, text = "Book ID", height = '1')
    loanStatusL = Label(frameElements, text = "Loan Status", height = '1')
    titleL.grid(column = 0, row = 3, padx = 10, pady = (5, 20))
    titleL.config(font=("New Times Roman", 13, 'bold'), width = '40')
    authorL.grid(column = 1, row = 3, padx = 10, pady = (5, 20))
    authorL.config(font=("New Times Roman", 13, 'bold'), width = '40')
    IDL.grid(column = 3, row = 3, padx = 10, pady = (5, 20))
    IDL.config(font=("New Times Roman", 13, 'bold'), width = '15')
    loanStatusL.grid(column = 2, row = 3, padx = 10, pady = (5, 20))
    loanStatusL.config(font=("New Times Roman", 13, 'bold'), width = '15')


def search(text, title, author, ID, loanStatus):
    """Searches for books with data similar to user's input information:
    
    title - the list of titles
    author - the list of authors
    loanStauts - the list of loan statuses
    ID - the list of ID's."""
    text = text.strip()
    numberOfBooks = booksNumber()
    searchValue = [0] * numberOfBooks
    if (len(title) < numberOfBooks):
        title = []
        author = []
        ID = []
        loanStatus = []
        title, author, ID, loanStatus = readList()
    for i in range(numberOfBooks):
        if (text.strip().lower() == title[i].strip().lower() or 
            text.strip().lower() ==
            author[i].strip().lower() or text.strip().lower() == 
            ID[i].strip().lower() or
            text.strip().lower() == loanStatus[i].strip().lower()):
            searchValue[i] = len(text) * 1.1 + len(text.strip().split(" ")) * 0.3
        else:
            searchValue[i] = compare(text, title[i], searchValue[i])
            searchValue[i] = compare(text, author[i], searchValue[i])
    return searchValue
        
def removeEmpt(list):
    """Removes empty elements from a list:
    
    list - the list, from which empty elements are removed."""
    for j in range (0, len(list)):
                if (j >= len(list)):
                    break
                if (list[j] == ""):
                    del(list[j])
                    j = j - 1
    return list

def compareWords(words1, words2):
    """Compares separate words of two lists of words.
    Returns the number of words matching and their total length::
    
    words1 - a list of user's input words or either a book's title or author
    words2 - a list of user's input words or either a book's title or author."""
    j = 0
    same = 0
    letters = 0
    while j < len(words1):
        if (j >= len(words1)):
            break
        if (words1[j].lower() == words2[j].lower()):
            same = same + 1
            letters = letters + len(words1[j])
            del (words1[j])
            del (words2[j])
            j = j - 1
        j = j + 1
    return same, letters, words1, words2

def wordsSameInd(words1, words2):
    """Compares words, having the same indices in two lists.. 
    Returns the number of words matching and their total length:
    
    words1 - a list of user's input words or either a book's title or author
    words2 - a list of user's input words or either a book's title or author."""
    if (len(words1) > len(words2)):
        same, letters, words2, words1 = compareWords(words2, words1)
    else:
        same, letters, words1, words2 = compareWords(words1, words2)
    return same, letters, words1, words2

def wordsDiffInd(words1, words2):
    """Finds matching words in two lists of strings and removes them.
    Returns value accumulated for similarity of the lists:
    
    words1 - a list of user's input words or either a book's title or author
    words2 - a list of user's input words or either a book's title or author."""
    value = 0
    j = 0
    while j < len(words1):
        k = 0
        while k < len(words2):
            if (j >= len(words1)):
                break
            if (k >= len(words2)):
                break
            if (words1[j].lower() == words2[k].lower()):
                value = value + 1.1 * len(words2[k])
                del(words1[j])
                del(words2[k])
                j = j - 1
                break
            k = k + 1
        j = j + 1
    return value

def compare(text, element, value):
    """Returns the value showing the similarity of two lists of strings:
    
    text - user's input text
    element - book's data (title or author)
    value - value for similarity already calculated for a particular book."""
    words1 = removeEmpt(text.strip().split(" "))
    words2 = element.strip().split(" ")
    same, letters, words1, words2 = wordsSameInd(words1, words2)
    value = value + wordsDiffInd(words1, words2)
    value = value + 0.3 * same + 1.1 * letters
    return value

def swap(a, b):
    """Swaps two variables:

    a - variable one
    b - variable two."""
    return b, a

def quickSort(left, right, searchValue, title, author, loanStatus, ID):
    """Sorts the title, author, loanStatus, ID and searchValue lists according 
    to searchValue values.
    
    left - left boundary of the list to be sorted
    right - right boundary of the list to be sorted
    searchValueNew - the list of values, showing each book's similarity to user's 
                                                                            input
    title - the list of titles
    author - the list of authors
    loanStauts - the list of loan statuses
    ID - the list of ID's."""
    pivIndex = left
    if (left >= right):
        return searchValue, title, author, loanStatus, ID
    wall = left
    pivot = searchValue[wall]
    for i in range (left, right):
        if (pivot < searchValue[i]):
            title[wall], title[i] = swap(title[wall], title[i])
            author[wall], author[i] = swap(author[wall], author[i])
            loanStatus[wall], loanStatus[i] = swap(loanStatus[wall], loanStatus[i])
            ID[wall], ID[i] = swap(ID[wall], ID[i])
            searchValue[wall], searchValue[i] = swap (searchValue[wall], 
                                                      searchValue[i])
            if (pivIndex == wall):
                pivIndex = i
            wall = wall + 1
    title[wall], title[pivIndex] = swap(title[wall], title[pivIndex])
    author[wall], author[pivIndex] = swap(author[wall], author[pivIndex])
    loanStatus[wall], loanStatus[pivIndex] = swap(loanStatus[wall], 
                                                  loanStatus[pivIndex])
    ID[wall], ID[pivIndex] = swap(ID[wall], ID[pivIndex])
    searchValue[wall], searchValue[pivIndex] = swap(searchValue[wall], 
                                                    searchValue[pivIndex])
    quickSort(left, wall, searchValue, title, author, loanStatus, ID)
    quickSort(wall + 1, right, searchValue, title, author, loanStatus, ID)
    return searchValue, title, author, loanStatus, ID

def quickSortID(left, right, title, author, loanStatus, ID):
    """Sorts the title, author, loanStatus and ID lists according to ID values.
    
    left - left boundary of the list to be sorted
    right - right boundary of the list to be sorted
    title - the list of titles
    author - the list of authors
    loanStauts - the list of loan statuses
    ID - the list of ID's."""
    if (left >= right):
        return title, author, loanStatus, ID
    wall = left
    pivIndex = left
    pivot = ID[wall]
    for i in range (left, right):
        if (int(pivot) > int(ID[i])):
            title[wall], title[i] = swap(title[wall], title[i])
            author[wall], author[i] = swap(author[wall], author[i])
            loanStatus[wall], loanStatus[i] = swap(loanStatus[wall], loanStatus[i])
            ID[wall], ID[i] = swap(ID[wall], ID[i])
            if (pivIndex == wall):
                pivIndex = i
            wall = wall + 1
    title[wall], title[pivIndex] = swap(title[wall], title[pivIndex])
    author[wall], author[pivIndex] = swap(author[wall], author[pivIndex])
    loanStatus[wall], loanStatus[pivIndex] = swap(loanStatus[wall], 
                                                  loanStatus[pivIndex])
    ID[wall], ID[pivIndex] = swap(ID[wall], ID[pivIndex])
    quickSortID(left, wall, title, author, loanStatus, ID)
    quickSortID(wall + 1, right, title, author, loanStatus, ID)
    return title, author, loanStatus, ID