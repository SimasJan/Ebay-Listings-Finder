from tkinter import *
import backend
import webbrowser

###########################################################################
# AREA FOR BUTTON ACTION FUNCTIONS

def get_seller_and_items_command():
    """ Takes the user input of the seller and performs the backend get_seller function, returns
    the found results, if results == 0; returns No results. """
    value = str(user_entry.get())
    backend.get_seller(value)
    for item in backend.soup.find_all('span', {'class':'rcnt'}):
        if str(item.get_text()) == str(0):
            found_results.set('No results found. Maybe check your input?')
        elif str(item.get_text()) > str(0):
            for title in backend.soup.select('title'):
                found_results.set('Seller Found: {} || Results: {}'.format(title.get_text(), item.get_text()))
        else:
            found_results.set('Something gone wrong...')


def show_seller_items_command():
    """ Performs the backend function to get listed item details from sellers page, and
    inserts them into the listbox (databox). """
    databox.delete(0,END)
    backend.seller_listed_items()
    for key, value in backend.listing_dict.items():
        databox.insert(END, [value[0],key])

def internet(event):
    """ Identifies the selected item in the listbox (databox), if item title matches key value in the 
    backend listed item dictionary, opens the matched title url link in the browser. """
    item = databox.get('active') # gets clicked item
    print(item)
    for key, value in backend.listing_dict.items():
        if key == item[1]:
            webbrowser.open_new(value[1])

def export_items():
    """ Exports to csv file all the items in the listbox (databox) with the name of the seller.
    Method 1: Select all the items in the listbox. Identifies (?) them by some measurement, goes to backend and finds 
    identified item details from a dictionary of full item details. Finally, exports them to csv file in the existing directory.
    csv file format: title (key) = first column | values = following columns.
    """
    pass

def show_listing_details():
    """ Goes to backend and performs function to scrape individual listing.
    inserts into the listbox (databox)
    """
    databox.delete(0,END)
    backend.megaList()
    for value in backend.allProductList:
        databox.insert(END, value)
        
def show_detailed_items():
    for value in backend.allProductList:
        databox.insert(END,value)


###########################################################################
# GUI WINDOW CODE AREA BELOW 
root = Tk()
# Styling the main window
root.geometry('750x650+30+30')
root.title('Ebay Scraper (v.1.0) [by SJ]')
root.configure(background='lightgrey')

##########################################################################################
# TOP-BAR FOR USER INTERACTION

topbar= Frame(root, height=20, padx=2,pady=2)
topbar.pack(expand=NO, fill=X,side=TOP)
# Defining a label.
l1=Label(topbar, text='Seller/Shop Name:').grid(row=0,column=0,sticky='w')

# user entry fields
user_entry = StringVar()
e1=Entry(topbar, textvariable=user_entry)
e1.grid(row=0,column=2,columnspan=2)
# creating a cursor focus on the entry field
e1.focus()

# TOP-BAR BUTTONS FOR USER TO INTERACT
b1=Button(topbar, text='START', width=10, command=get_seller_and_items_command).grid(row=0,column=4,padx=4)

commandBar = Frame(root, height=10, padx=2,pady=2, relief='solid',bd=2)
commandBar.pack(expand=NO, fill=X, side=TOP)

b2=Button(commandBar,text='Show Listings', command=show_seller_items_command).grid(row=1,column=1,sticky='w')
b3=Button(commandBar,text='Get Product Details', command=show_listing_details).grid(row=1,column=2,sticky='w')
b4=Button(commandBar,text='Show Detailed Items', width=15,command=show_detailed_items).grid(row=1,column=3,sticky='w')

##########################################################################
# INFO-BAR FOR INFORMATION, USER NOTIFICATION ABOUT RESULTS

# info-bar frame
info_bar = Frame(root,height=12, padx=2)
info_bar.pack(expand=NO,fill=X, side=TOP)

# Notification/Information field label.
found_results = StringVar()
info_label = Label(info_bar, textvariable=found_results, bg='grey').grid(row=1,column=0,columnspan=10,sticky='w',pady=2)

##########################################################################
# BOTTOM-BAR TO DISPLAY THE RESULTS 

# Creating a listbox window 
databox = Listbox(root,width=630,height=520, bg='lightblue',relief='solid',bd=2)
databox.pack(expand=YES, fill=BOTH,side=TOP)

# Making an item in the databox clickable and opening it in a browser.
databox.bind('<Double-Button-1>', internet)

root.mainloop()

