#Created by Jere Lyytinen, VAMK, 2016
#All rights reserved

import re
from tkinter import *
from tkinter.ttk import *
import pymysql.cursors

class DBTest:
    #Initiates things we'll use
    def __init__(self, root):
        self._create_tabs()
        self._layout()
        #Create tabs
    def _create_tabs(self):
        self.frame = Frame(root) # Main Frame
        self.update_button = Button(self.frame, text="\"Update\"", command=lambda: self.rebuild_window())  # Rebuild window thing
        self.info = Label(self.frame, text="By: J. Lyytinen")
        self.nb = Notebook(self.frame) # The 'tab-thing'

        # Create main tabs
        customer = Frame(self.nb)
        order = Frame(self.nb)
        product = Frame(self.nb)
        # Create customer NB
        self.customer = Notebook(customer)
        # Create Customer-tabs
        customer.insert = Frame(self.customer)
        customer.select = Frame(self.customer)
        customer.selAll = Frame(self.customer)
        customer.delete = Frame(self.customer)
        customer.modify = Frame(self.customer)
        self._customer_insert_frame(customer.insert)
        self._customer_select_frame(customer.select)
        self._customer_selAll_frame(customer.selAll)
        self._customer_delete_frame(customer.delete)
        self._customer_modify_frame(customer.modify)

        # Create product NB
        self.product = Notebook(product)
        # Create product-tabs
        product.insert = Frame(self.product)
        product.select = Frame(self.product)
        product.selAll = Frame(self.product)
        product.delete = Frame(self.product)
        product.modify = Frame(self.product)
        self._product_insert_frame(product.insert)
        self._product_select_frame(product.select)
        self._product_selAll_frame(product.selAll)
        self._product_delete_frame(product.delete)
        self._product_modify_frame(product.modify)

        # Create order NB
        self.order = Notebook(order)
        # Create order-tabs
        order.insert = Frame(self.order)
        order.select = Frame(self.order)
        order.selAll = Frame(self.order)
        order.delete = Frame(self.order)
        self._order_insert_frame(order.insert)
        self._order_select_frame(order.select)
        self._order_selAll_frame(order.selAll)
        self._order_delete_frame(order.delete)

        # Adds the tabs to the notebook
        self.nb.add(customer, text="Customer")
        self.nb.add(order, text="Order")
        self.nb.add(product, text="Product")
        self.customer.add(customer.insert, text="Insert")
        self.customer.add(customer.select, text="Select")
        self.customer.add(customer.selAll, text="Select ALL")
        self.customer.add(customer.delete, text="Delete Cust.")
        self.customer.add(customer.modify, text="Modify Cust.")
        self.product.add(product.insert, text="Insert")
        self.product.add(product.select, text="Select")
        self.product.add(product.selAll, text="Select ALL")
        self.product.add(product.delete, text="Delete Prod.")
        self.product.add(product.modify, text="Modify Prod.")
        self.order.add(order.insert, text="Insert")
        self.order.add(order.select, text="Select")
        self.order.add(order.selAll, text="Select ALL")
        self.order.add(order.delete, text="Delete Order")

    def _layout(self):
        # Layout creation
        self.frame.grid(row=0, column=0, sticky=(N,S,W,E))
        self.update_button.grid(row=1, column=0)
        self.info.grid(row=1, column=0, sticky=E)
        self.nb.grid(row=0, column=0, sticky=(N,S,W,E))
        self.customer.grid(row=0, column=0, columnspan=2, sticky=(N,S,W,E), pady=5)
        self.product.grid(row=0, column=0, columnspan=2, sticky=(N, S, W, E), pady=5)
        self.order.grid(row=0, column=0, columnspan=2, sticky=(N,S,W,E), pady=5)
        # Resize rules
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=2)
        self.frame.rowconfigure(0, weight=2)

    #CUSTOMER section
    def _customer_insert_frame(self, insert):
        # Creates the Entry boxes to get data
        insert.name = Entry(insert)
        insert.address = Entry(insert)
        insert.phone = Entry(insert)
        # Makes a label and puts things out on the screen.
        Label(insert, text="Name: ").grid(row=0, column=0, sticky=E)
        insert.name.grid(row=0, column=1, sticky=W)
        Label(insert, text="Address: ").grid(row=1, column=0, sticky=E)
        insert.address.grid(row=1, column=1, sticky=W)
        Label(insert, text="Phone: ").grid(row=2, column=0, sticky=E)
        insert.phone.grid(row=2, column=1, sticky=W)
        # Using 'lambda: ' to prevent prepare_insert from running before we want it to.
        insert.submit_button = Button(insert, text="Submit", command=lambda: self.customer_prepare_insert(insert))
        insert.submit_button.grid(row=4, column=0, columnspan=2)
        insert.text = Text(insert, width=34, height=4, wrap=WORD)
        insert.text.grid(row=5,column=0,columnspan=2)

    def customer_prepare_insert(self, insert):
        """ Reg ex for the phone number.
        Explanation:
        [+]? = First char can be a +, not needed tho
        [\d -]* = allow unlimited digits (0-9), spaces and -
        {3,} = Specifies at least 3 numbers."""
        pattern = re.compile(r"^[+]?[\d -]{3,}")
        # Gets values from the Entry boxes above.
        name = insert.name.get()
        address = insert.address.get()
        phone = insert.phone.get()

        # Checks if every field has something in them. (Does not check if only a space)
        if not all((name, address, phone)):
            errorText = "Need to enter something in all boxes."
            error = True
        # Checks if the phone-pattern matches our regEx
        elif not pattern.match(phone):
            error = True
            errorText = "Phone number can only contain 0-9, spaces and dashes (-).\nFirst symbol can be + for country codes."
        else:
            error = False
        # If we have an error, throw the error text
        if error:
            text = errorText
        # Else does the insert into DB.
        else:
            text = self.add_to_DB('CUSTOMER',name, address, phone)

        insert.text.config(state=NORMAL)
        insert.text.delete(0.0, END)
        insert.text.insert(0.0, text)
        insert.text.config(state=DISABLED)

    def _customer_select_frame(self, select):
        # Create the Entry boxes
        select.sID = Entry(select)
        select.name = Entry(select)
        select.address = Entry(select)
        select.phone = Entry(select)

        # Puts them out on the frame
        Label(select, text="Search for Databasedata\nenter at least 1 searchfield").grid(row=0, column=0, columnspan=2)
        Label(select, text="Search ID:").grid(row=1, column=0, sticky=E)
        select.sID.grid(row=1, column=1, sticky=W)
        Label(select, text="Search Name:").grid(row=2, column=0, sticky=E)
        select.name.grid(row=2, column=1, sticky=W)
        Label(select, text="Search Address").grid(row=3, column=0, sticky=E)
        select.address.grid(row=3, column=1, sticky=W)
        #Label(select, text="Search phone").grid(row=4, column=0, sticky=E)
        #select.phone.grid(row=4, column=1, sticky=W)
        # Using lambda again on the button to not make it do the
        # prepare before we actually click the button
        select.submit_button = Button(select, text="Submit", command=lambda: self.customer_prepare_select(select))
        select.submit_button.grid(row=5, column=0, columnspan=2)
        select.text = Text(select, width=30, height=10, wrap=WORD)
        select.text.grid(row=6,column=0,columnspan=2)

    def customer_prepare_select(self, select):
        # Get value from the search fields
        sID = select.sID.get()
        name = select.name.get()
        address = select.address.get()
        phone = select.phone.get()
        args = {}
        stmt = ""
        # Checks at least one have data. (Does not check if only a space)
        if sID != "" or name != "" or address != "" or phone != "":
            # If at least one have data we check which
            # one and adds the string for the query
            if sID != "":
                args['ID'] = "id='"+sID+"' AND "
            if name != "":
                args['name'] = "name='"+name+"' AND "
            if address != "":
                args['address'] = "address='"+address+"' AND "
            #This is for checking by the phone number but search by that felt a bit stupid so leaving it out:
            # if phone != "":
            #     args['phone'] = "phone='"+phone+"' AND"
            for key, value in args.items():
                stmt += value
            # Removes the last ' AND '
            stmt = stmt[:-5]
            sql = "SELECT * FROM CUSTOMER WHERE {val}".format(val=stmt)
            db_result = self.get_from_DB(sql)
            textBox = ""
            # If we get rows back
            if db_result:
                # Iterates for all rows gotten
                for key in db_result:
                    textBox += "ID: {id} Name: {name}\nAddress: {address}\nPhone: {phone}\n\n".format(id=key['id'], name=key['name'], address=key['address'], phone=int(key['phone']))
            # If we searched for an entry that didnt exist
            else:
                textBox = "Could not find what you searched for."
        # If we enter no value in any box.
        else:
            textBox = "Must insert at least one value."

        # Updates the textfield
        select.text.config(state=NORMAL)
        select.text.delete(0.0, END)
        select.text.insert(0.0, textBox)
        select.text.config(state=DISABLED)

    def _customer_selAll_frame(self, selAll):
        #Create the button to show everything
        Label(selAll, text="Fetch all entries?").grid(row=0, column=0, sticky=E)
        selAll.submit_button = Button(selAll, text="Fetch!", command=lambda: self.customer_select_all_DB(selAll))
        selAll.submit_button.grid(row=0, column=1, sticky=W)
        selAll.text = Text(selAll, width=30, height=15, wrap=WORD)
        selAll.text.grid(row=1, column=0, columnspan=2)

    def customer_select_all_DB(self, selAll):
        sql = "SELECT * from CUSTOMER"
        # Gets all entries from the DB
        db_result = self.get_from_DB(sql)
        textBox = ""
        # If we get result returned
        if db_result:
            # Iterates for every Row
            for key in db_result:
                textBox += "ID: {id} Name: {name}\nAddress: {address}\nPhone: {phone}\n\n".format(id=key['id'], name=key['name'], address=key['address'], phone=key['phone'])
        # If no entries was found in the DB
        else:
            textBox = "There's nothing in the Database or some error n shit."
        # Updates the textfield
        selAll.text.config(state=NORMAL)
        selAll.text.delete(0.0, END)
        selAll.text.insert(0.0, textBox)
        selAll.text.config(state=DISABLED)

    def _customer_delete_frame(self, delete):
        Label(delete, text="Delete a user with the dropdown menu").grid(row=0, column=0, columnspan=2, sticky=E)
        # Creates the menu
        # The variable we need to "get"-value from
        delete.var = StringVar()
        delete.var.set("None")
        # Gets the list with usernames:
        delete.users = self.get_customer_list()
        delete.menu = OptionMenu(delete, delete.var, *delete.users[0])
        delete.menu.grid(row=1, column=0)
        delete.submit_button = Button(delete, text="DELETE!", command=lambda: self.customer_delete_from_DB(delete))
        delete.submit_button.grid(row=2)
        delete.text = Text(delete, width=34, height=15, wrap=WORD)
        delete.text.grid(row=3, column=0, columnspan=2)

    def customer_delete_from_DB(self, delete):
        # Gets the name we want to delete
        # and sets from which tab(table) and column
        custName = delete.var.get()
        custID = delete.users[1].get(custName)
        table = "customer"
        x = self.delete_from_DB(table, custID, custName)
        delete.text.config(state=NORMAL)
        delete.text.delete(0.0, END)
        delete.text.insert(0.0, x)
        delete.text.config(state=DISABLED)

    def _customer_modify_frame(self, modify):
        # Makes the LabelFrames
        self.modify_cust = LabelFrame(modify, text="Who do you want to change?", labelanchor=N)
        self.modify_cust.grid(row=0, column=0, sticky=(N, S, W, E))
        self.modify_values = LabelFrame(modify, text="Update with...", labelanchor=N)
        self.modify_values.grid(row=1, column=0, sticky=(N, S, W, E))
        self.modify_submit = LabelFrame(modify, text="Submit changes", labelanchor=N)
        self.modify_submit.grid(row=2, column=0, sticky=(N, S, W, E))
        # Creates text fields
        modify.newAddress = Entry(self.modify_values)
        modify.newPhone = Entry(self.modify_values)
        ## Customer Frame
        # default Vars
        modify.customerVar = StringVar()
        modify.customerVar.set("None")
        # Get the list of customers
        modify.customers = self.get_customer_list()
        modify.customerMenu = OptionMenu(self.modify_cust, modify.customerVar, *modify.customers[0])
        modify.customerMenu.grid(row=0, column=0, sticky=(W, E))
        ## New values field
        Label(self.modify_values, text="New Phone: ").grid(row=0, column=0, sticky=W)
        modify.newPhone.grid(row=0, column=1, sticky=W)
        Label(self.modify_values, text="New Address: ").grid(row=1, column=0, sticky=W)
        modify.newAddress.grid(row=1, column=1, sticky=W)
        ## Submit button field
        modify.submit_button = Button(self.modify_submit, text="Submit",
                                      command=lambda: self.customer_prepare_modify(modify))
        modify.submit_button.grid(row=0, column=1, sticky=W)
        modify.text = Text(modify, width=34, heigh=10, wrap=WORD)
        modify.text.grid(row=3, column=0, columnspan=2, sticky=(N, S, W, E))

    def customer_prepare_modify(self, modify):
        """ Reg ex for the phone number.
        Explanation:
        [+]? = First char can be a +, not needed tho
        [\d -]* = allow unlimited digits (0-9), spaces and -
        {3,} = Specifies at least 3 numbers."""
        pattern = re.compile(r"^[+]?[\d -]{3,}")
        # Sets up the vars
        error = False
        customer = modify.customerVar.get()
        phone = modify.newPhone.get()
        address = modify.newAddress.get()
        fields = []
        text = ""
        # Checks if anything is filled
        if customer == "None":
            text += "Got to choose a customer.\n\n"
            error = True
        if phone == "" and address == "":
            text += "At least one field must be changed (Contain a value).\n\n"
            error = True
            #Checking the phone number
        if not pattern.match(phone) and not phone == "" and not error:
            text = "Phone number can only contain 0-9, spaces and dashes (-).\nFirst symbol can be + for country codes."
            error = True
            #Checks the done changes
        if not error:
            if phone:
                fields.append('phone')
                fields.append(phone)
            if address:
                fields.append('address')
                fields.append(address)
            text = self.update_DB('modCustomer', customer, fields)
        modify.text.config(state=NORMAL)
        modify.text.delete(0.0, END)
        modify.text.insert(0.0, text)
        modify.text.config(state=DISABLED)

    #PRODUCT section
    def _product_insert_frame(self, insert):
        # Creates the Entry boxes to get data
        insert.name = Entry(insert)
        insert.price = Entry(insert)
        insert.unit = Entry(insert)
        # Makes a label and puts things out on the screen.
        Label(insert, text="Name: ").grid(row=0, column=0, sticky=E)
        insert.name.grid(row=0, column=1, sticky=W)
        Label(insert, text="Price: ").grid(row=1, column=0, sticky=E)
        insert.price.grid(row=1, column=1, sticky=W)
        Label(insert, text="Unit: ").grid(row=2, column=0, sticky=E)
        insert.unit.grid(row=2, column=1, sticky=W)
        # Using 'lambda: ' to prevent prepare_insert from running before we want it to.
        insert.submit_button = Button(insert, text="Submit", command=lambda: self.product_prepare_insert(insert))
        insert.submit_button.grid(row=4, column=0, columnspan=2)
        insert.text = Text(insert, width=34, height=4, wrap=WORD)
        insert.text.grid(row=5, column=0, columnspan=2)

    def product_prepare_insert(self, insert):
        # Gets values from the Entry boxes above.
        name = insert.name.get()
        price = insert.price.get()
        unit = insert.unit.get()
        pattern = re.compile(r"^[0-9]*$")

        # Checks if every field has something in them. (Does not check if only a space)
        # If we have an error, throw the error text
        if not all((name, price, unit)):
            errorText = "Need to enter something in all boxes."
            error = True
        #Checks that the pattern matches the regular expression, which only accepts numbers. 0 alone is not accepted.
        elif not pattern.match(price):
            error = True
            errorText = "Price needs to be a number (0-9) and above 0."
        elif not pattern.match(unit):
            error = True
            errorText = "Price needs to be a number (0-9) and above 0."
        # Else does the insert into DB since there's no error.
        else:
            error = False

        if error:
            text = errorText
        else:
            text = self.add_to_DB('PRODUCT', name, price, unit)

        insert.text.config(state=NORMAL)
        insert.text.delete(0.0, END)
        insert.text.insert(0.0, text)
        insert.text.config(state=DISABLED)

    def _product_select_frame(self, select):
        # Create the Entry boxes
        select.sID = Entry(select)
        select.name = Entry(select)
        select.price = Entry(select)
        select.unit = Entry(select)

        # Puts them out on the frame
        Label(select, text="Search for Databasedata\nenter at least 1 searchfield").grid(row=0, column=0, columnspan=2)
        Label(select, text="Search ID:").grid(row=1, column=0, sticky=E)
        select.sID.grid(row=1, column=1, sticky=W)
        Label(select, text="Search Name:").grid(row=2, column=0, sticky=E)
        select.name.grid(row=2, column=1, sticky=W)
        Label(select, text="Search price").grid(row=3, column=0, sticky=E)
        select.price.grid(row=3, column=1, sticky=W)
        Label(select, text="Search unit").grid(row=4, column=0, sticky=E)
        select.unit.grid(row=4, column=1, sticky=W)
        # Using lambda again on the button to not make it do the
        # prepare before we actually click the button
        select.submit_button = Button(select, text="Submit", command=lambda: self.product_prepare_select(select))
        select.submit_button.grid(row=5, column=0, columnspan=2)
        select.text = Text(select, width=34, height=10, wrap=WORD)
        select.text.grid(row=6, column=0, columnspan=2)

    def product_prepare_select(self, select):
        # Get value from the search fields.
        sID = select.sID.get()
        name = select.name.get()
        price = select.price.get()
        unit = select.unit.get()
        args = {}
        stmt = ""
        # Checks at least one have data. (Does not check if only a space)
        if sID != "" or name != "" or price != "" or unit != "":
            # If at least one have data we check which
            # one and adds the string for the query
            if sID != "":
                args['ID'] = "id='" + sID + "' AND "
            if name != "":
                args['name'] = "name='" + name + "' AND "
            if price != "":
                args['price'] = "price='" + price + "' AND "
            if unit != "":
                args['unit'] = "unit='" + unit + "' AND "
            for key, value in args.items():
                stmt += value
            # Removes the last ' AND '
            stmt = stmt[:-5]
            sql = "SELECT * FROM PRODUCT WHERE {val}".format(val=stmt)
            db_result = self.get_from_DB(sql)
            textBox = ""
            # If we get rows back
            if db_result:
                # Iterates for all rows gotten
                for key in db_result:
                    textBox += "ID: {id} Name: {name}\nPrice: {price}\nUnit: {unit}\n\n".format(id=key['id'],
                                                                                                      name=key['name'],
                                                                                                      price=key[
                                                                                                          'price'],
                                                                                                      unit=key[
                                                                                                          'unit'])
            # If we searched for an entry that didnt exist
            else:
                textBox = "Could not find what you searched for."
        # If we enter no value in any box.
        else:
            textBox = "Must insert at least one value."

        # Updates the textfield
        select.text.config(state=NORMAL)
        select.text.delete(0.0, END)
        select.text.insert(0.0, textBox)
        select.text.config(state=DISABLED)

    def _product_selAll_frame(self, selAll):
        # Create the button to show everything
        Label(selAll, text="Fetch all entries?").grid(row=0, column=0, sticky=E)
        selAll.submit_button = Button(selAll, text="Fetch!", command=lambda: self.product_select_all_DB(selAll))
        selAll.submit_button.grid(row=0, column=1, sticky=W)
        selAll.text = Text(selAll, width=34, height=15, wrap=WORD)
        selAll.text.grid(row=1, column=0, columnspan=2)

    def product_select_all_DB(self, selAll):
        sql = "SELECT * from PRODUCT"
        # Gets all entries from the DB
        db_result = self.get_from_DB(sql)
        textBox = ""
        # If we get result returned
        if db_result:
            # Iterates for every Row
            for key in db_result:
                textBox += "ID: {id} Name: {name}\nPrice: {price}\nUnit: {unit}\n\n".format(id=key['id'],
                                                                                                  name=key['name'],
                                                                                                  price=key[
                                                                                                      'price'],
                                                                                                  unit=key['unit'])
        # If no entries was found in the DB
        else:
            textBox = "There's nothing in the Database or some error n shit."
        # Updates the textfield
        selAll.text.config(state=NORMAL)
        selAll.text.delete(0.0, END)
        selAll.text.insert(0.0, textBox)
        selAll.text.config(state=DISABLED)

    def _product_delete_frame(self, delete):
        Label(delete, text="Delete a product with the dropdown menu").grid(row=0, column=0, columnspan=2, sticky=E)
        # Creates the menu
        # The variable we need to "get"-value from
        delete.var = StringVar()
        delete.var.set("None")
        # Gets the list with products:
        delete.products = self.get_product_list()
        delete.menu = OptionMenu(delete, delete.var, *delete.products[0])
        delete.menu.grid(row=1, column=0)
        delete.submit_button = Button(delete, text="DELETE!", command=lambda: self.product_delete_from_DB(delete))
        delete.submit_button.grid(row=2)
        delete.text = Text(delete, width=34, height=15, wrap=WORD)
        delete.text.grid(row=3, column=0, columnspan=2)

    def product_delete_from_DB(self, delete):
        # Gets the product we want to delete
        # and sets from which tab(table) and column
        prodName = delete.var.get()
        prodID = delete.products[1].get(prodName)
        table = "product"
        x = self.delete_from_DB(table, prodID, prodName)
        delete.text.config(state=NORMAL)
        delete.text.delete(0.0, END)
        delete.text.insert(0.0, x)
        delete.text.config(state=DISABLED)

    def _product_modify_frame(self, modify):
        # Makes the LabelFrames
        self.modify_prod = LabelFrame(modify, text="What do you want to change?", labelanchor=N)
        self.modify_prod.grid(row=0, column=0, sticky=(N, S, W, E))
        self.modify_values = LabelFrame(modify, text="Update with...", labelanchor=N)
        self.modify_values.grid(row=1, column=0, sticky=(N, S, W, E))
        self.modify_submit = LabelFrame(modify, text="Submit changes", labelanchor=N)
        self.modify_submit.grid(row=2, column=0, sticky=(N, S, W, E))
      # Creates text fields
        modify.newUnit = Entry(self.modify_values)
        modify.newPrice = Entry(self.modify_values)
      ## Product Frame
      # default Vars
        modify.productVar = StringVar()
        modify.productVar.set("None")
      # Get the list of products
        modify.products = self.get_product_list()
        modify.productMenu = OptionMenu(self.modify_prod, modify.productVar, *modify.products[0])
        modify.productMenu.grid(row=0, column=0, sticky=(W, E))
      ## New values field
        Label(self.modify_values, text="New amount: ").grid(row=0, column=0, sticky=W)
        modify.newUnit.grid(row=0, column=1, sticky=W)
        Label(self.modify_values, text="New price: ").grid(row=1, column=0, sticky=W)
        modify.newPrice.grid(row=1, column=1, sticky=W)
     ## Submit button field
        modify.submit_button = Button(self.modify_submit, text="Submit",
        command=lambda: self.product_prepare_modify(modify))
        modify.submit_button.grid(row=0, column=1, sticky=W)
        modify.text = Text(modify, width=34, heigh=10, wrap=WORD)
        modify.text.grid(row=3, column=0, columnspan=2, sticky=(N, S, W, E))

    def product_prepare_modify(self, modify):
        pattern = re.compile(r"^[0-9]*$")
      # Sets up the vars
        error = False
        product = modify.productVar.get()
        unit = modify.newUnit.get()
        price = modify.newPrice.get()
        fields = []
        text = ""
      # Checks if anything is filled
        if product == "None":
                text += "Got to choose a product.\n\n"
                error = True
        if unit == "" and price == "":
                text += "At least one field must be changed (Contain a value).\n\n"
                error = True
        if not pattern.match(unit) and not unit == "" and not error:
                text = "The amount needs to be a number (0-9) and above 0."
                error = True
        if not pattern.match(price) and not price == "" and not error:
            text = "The price needs to be a number (0-9) and above 0."
            error = True
    #Checks the unit has no errors
        if not error:
            if unit:
                fields.append('unit')
                fields.append(unit)
    #Checks the price has no errors
            if price:
                fields.append('price')
                fields.append(price)
            text = self.update_DB('modProduct', product, fields)
        modify.text.config(state=NORMAL)
        modify.text.delete(0.0, END)
        modify.text.insert(0.0, text)
        modify.text.config(state=DISABLED)

    #ORDERS section
    def _order_insert_frame(self, insert):
        # Makes the Customer and Product Frames
        self.order_customer = LabelFrame(insert, text="Buyer: ", labelanchor=N)
        self.order_customer.grid(row=0, column=0, sticky=(N,S,W,E))
        self.order_product = LabelFrame(insert, text="Product: ",labelanchor=N)
        self.order_product.grid(row=1, column=0, sticky=(N,S,W,E))
        self.order_amount = LabelFrame(insert, text="Amount: ", labelanchor=N)
        self.order_amount.grid(row=2, column=0, sticky=(N,S,W,E))
        self.order_confirm = LabelFrame(insert, text="Confirm: ",labelanchor=N)
        self.order_confirm.grid(row=3, column=0, sticky=(N,S,W,E))
        # Some default Vars
        insert.productVar = StringVar()
        insert.productVar.set("None")
        insert.totalUnits = IntVar()
        insert.customerVar = StringVar()
        insert.customerVar.set("None")
        # Gets the list of customers
        insert.customers = self.get_customer_list()
        insert.customerMenu = OptionMenu(self.order_customer, insert.customerVar, *insert.customers[0])
        insert.customerMenu.grid(row=0, column=1, sticky=EW)
        # Gets the list of products and current stocks
        insert.products = self.get_product_list()
        insert.unitLabel = Label(self.order_product, text="In stock: ~")
        insert.unitLabel.grid(row=0, column=1, sticky=W)
        insert.productMenu = OptionMenu(self.order_product, insert.productVar, *insert.products[0], command=lambda _: self.order_update_price(insert))
        insert.productMenu.config(width=15)
        insert.productMenu.grid(row=0, column=0, sticky="EW")
        # Enter how many you want to buy
        insert.amount = Entry(self.order_amount)
        insert.amount.grid()
        insert.insert_button = Button(self.order_confirm, text="Submit", command=lambda: self.order_prepare_insert(insert))
        insert.insert_button.grid(row=0, column=0)
        # Shows result.
        insert.text = Text(self.order_confirm, width=34, height=10, wrap=WORD)
        insert.text.grid(row=1, column=0,columnspan=2, sticky=(N,S,W,E))
        insert.text.config(state=DISABLED)

    def order_prepare_insert(self, x):
        # Only allow numbers
        pattern = re.compile(r"^[^0][\d]{0,}")
        # Sets up the things we need to use
        error = False
        errorT = ""
        totUnit = x.totalUnits.get()
        amount = x.amount.get()
        cust = x.customerVar.get()
        custID = x.customers[1].get(cust, "CustError")
        prod = x.productVar.get()
        prodID = x.products[1].get(prod, "prodError")

        # Try and see if amount is a number
        try:
            amount = int(amount)
        except Exception:
            error = True
        # Checks so everything is entered:
        if cust == "None" or prod == "None":
            error = True
            errorT = "Must choose a customer and/or product.\n"
        # If amount doesn't match pattern
        if not pattern.match(str(amount)):
            error = True
            errorT += "Amount must contain numbers (0-9), can't be 0\n"

        # Checks if we don't have an error
        if not error:
            if int(totUnit) - amount < 0:
                answer = "Can't order more units than what exist in stock."
            else:
                stock = int(totUnit) - int(amount)
                #answer = "Customer: {cust} with ID: {custid}\nOrdered: {amount} units\nProduct: {prod} with ID: {prodID}\nUnits left: {stock}".format(cust=cust, custid=custID, prod=prod, prodID=prodID, amount=amount, stock=stock)
                answer = self.add_to_DB('ORDERS', custID, prodID, amount)
                answer += "\n\n" + self.update_DB('productUnit', stock, prodID)
        else:
            answer = errorT

        x.text.config(state=NORMAL)
        x.text.delete(0.0, END)
        x.text.insert(0.0, answer)
        x.text.config(state=DISABLED)

    def order_update_price(self, insert):
        productName = insert.productVar
        unitsList = insert.products[2]
        errorT = False
        if productName.get() != "None":
            units = unitsList[productName.get()]
        else:
            units = 0
        try:
            insert.totalUnits.set(int(units))
        except Exception as e:
            errorT = True
            error = self.errorCodeHandler(e)
        if errorT:
            text = error
        else:
            text = "In stock: "+str(units)
        insert.unitLabel.config(text=text)

    def _order_select_frame(self, select):
        # Create entry boxes
        select.orderID = Entry(select)
        select.custID = Entry(select)
        select.productID = Entry(select)
        # Puts them out on the frame
        Label(select, text="Search for Order-data\nenter at least 1 searchfield").grid(row=0, column=0, columnspan=2)
        Label(select, text="Order ID").grid(row=1, column=0, sticky=E)
        select.orderID.grid(row=1, column=1, sticky=W)
        Label(select, text="Customer").grid(row=2, column=0, sticky=E)
        select.custID.grid(row=2, column=1, sticky=W)
        Label(select, text="Product ID").grid(row=3, column=0, sticky=E)
        select.productID.grid(row=3, column=1, sticky=W)

        # Using lambda to not do function until button is pressed
        select.submit_button = Button(select, text="Submit", command=lambda: self.order_prepare_select(select))
        select.submit_button.grid(row=5, column=0, columnspan=2)
        select.text = Text(select, width=34, height=10, wrap=WORD)
        select.text.grid(row=6, column=0, columnspan=2)

    def order_prepare_select(self, select):
        # Get value from the search fields.
        custID = select.custID.get()
        orderID = select.orderID.get()
        productID = select.productID.get()
        args = {}
        stmt = ""
        # Checks at least one have data. (Does not check if only a space)
        if custID != "" or orderID != "" or productID != "":
            # If at least one have data we check which
            # one and adds the string for the query
            if custID != "":
                args['custID'] = "customer_id='" + custID + "' AND "
            if orderID != "":
                args['orderID'] = "id='" + orderID + "' AND "
            if productID != "":
                args['productID'] = "product_id='" + productID + "' AND "
            for key, value in args.items():
                stmt += value
            # Removes the last ' AND '
            stmt = stmt[:-5]
            sql = "SELECT * FROM ORDERS WHERE {val}".format(val=stmt)
            db_result = self.get_from_DB(sql)
            textBox = ""
            # If we get rows back
            if db_result:
                # Iterates for all rows gotten
                for key in db_result:
                    textBox += "OrderID: {order} CustomerID: {cust}\nProductID: {prod}\nAmount: {x}\nOrderdate: {y}\n\n".format(
                        order=str(key['id']), cust=str(key['customer_id']), prod=str(key['product_id']),
                        x=str(key['amount']), y=str(key['date']))
            # If we searched for an entry that didnt exist
            else:
                textBox = "Could not find what you searched for."
        # If we enter no value in any box.
        else:
            textBox = "Must insert at least one value."

        # Updates the textfield
        select.text.config(state=NORMAL)
        select.text.delete(0.0, END)
        select.text.insert(0.0, textBox)
        select.text.config(state=DISABLED)

    def _order_selAll_frame(self, selAll):
        Label(selAll, text="Fetch all orders?").grid(row=0, column=0, sticky=E)
        selAll.submit_button = Button(selAll, text="Fetch!", command=lambda: self.order_select_all_DB(selAll))
        selAll.submit_button.grid(row=0, column=1, sticky=W)
        selAll.text = Text(selAll, width=34, height=15, wrap=WORD)
        selAll.text.grid(row=1, column=0, columnspan=2)

    def order_select_all_DB(self, selAll):
        sql = "SELECT * from ORDERS"
        # Gets all entries from the DB
        db_result = self.get_from_DB(sql)
        textBox = ""
        # If we get result returned
        if db_result:
            # Iterates for every Row
            for key in db_result:
                textBox += "OrderID: {order} CustomerID: {cust}\nProductID: {prod}\nAmount: {x}\nOrderdate: {y}\n\n".format(
                    order=str(key['id']), cust=str(key['customer_id']), prod=str(key['product_id']),
                    x=str(key['amount']), y=str(key['date']))
        # If no entries was found in the DB
        else:
            textBox = "There's nothing in the Database or some error n shit."
        # Updates the textfield
        selAll.text.config(state=NORMAL)
        selAll.text.delete(0.0, END)
        selAll.text.insert(0.0, textBox)
        selAll.text.config(state=DISABLED)

    def _order_delete_frame(self, delete):
        Label(delete, text="Delete an order with the dropdown menu").grid(row=0, column=0, columnspan=2, sticky=E)
        # Creates the menu
        # The variable we need to "get"-value from
        delete.var = StringVar()
        delete.var.set("None")
        # Gets the list with usernames:
        delete.orderID = self.get_order_list()
        delete.menu = OptionMenu(delete, delete.var, *delete.orderID)
        delete.menu.grid(row=1, column=0)
        delete.submit_button = Button(delete, text="DELETE!", command=lambda: self.order_delete_from_DB(delete))
        delete.submit_button.grid(row=2)
        delete.text = Text(delete, width=34, height=15, wrap=WORD)
        delete.text.grid(row=3, column=0, columnspan=2)

    def order_delete_from_DB(self, delete):
        # Gets the name we want to delete
        # and sets from which tab(table) and column
        orderID = delete.var.get()
        if orderID != "None":
            table = "orders"
            x = self.delete_from_DB(table, orderID)
        else:
            x = "Choose an order to remove."
        delete.text.config(state=NORMAL)
        delete.text.delete(0.0, END)
        delete.text.insert(0.0, x)
        delete.text.config(state=DISABLED)

    def delete_from_DB(self, table, value, *args):
        # Making the query
        # Takes the tab (order, customer, products), plus the ID of the thing to delete
        # This is to re-use this delete code for other tabs.
        sql = "DELETE FROM {tab} WHERE id='{value}'".format(tab=table.upper(), value=value)
        # Connection config
        connection = self.db_settings()
        # Try to do the thing
        try:
            with connection.cursor() as cursor:
                # Executes the delete-query
                cursor.execute(sql)
                #Commit the changes
                connection.commit()
                # Checks how many rows that was affected
                result = cursor.rowcount
                # If 1 (row deleted) then show message.
                if result == 1:
                    if args:
                        result = "{name} from {tab}-tab has been deleted from the Database.\n".format(name=args[0], tab=table)
                    else:
                        result = "The order with the ID: {id} was succesfully deleted.".format(id=value)
                # If 0, no rows affected, thus nothing deleted.
                elif result == 0:
                    result = "Nothing got deleted."
                else:
                    result = "Something weird happened. More than 1 row changed."

        except Exception as e:
            result = self.errorCodeHandler(e)
        finally:
            connection.close()

        # Return value
        return result

    def add_to_DB(self, *args):
        """
        Accepts multiple args depending on what for.
        If args[0] is equal to, it wants these values:
        CUSTOMER: name, address, phone
        ORDER: customer_id, product_id, amount
        PRODUCT: name, unit (in stock), price (per unit)
        """
        # Connection config
        connection = self.db_settings()
        #Inserting the data
        try:
            # Adds it to DB
            with connection.cursor() as cursor:
                if args[0] == 'CUSTOMER':
                    # Makes query for CUSTOMER
                    # Args needed are args[1-3], name, address, phone.
                    sql = "INSERT INTO CUSTOMER (name, address, phone) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (args[1], args[2], args[3]))
                    result = "Data added\nName: {name}\nAddress: {address}\nPhone: {phone}".format(name=args[1],address=args[2],phone=args[3])
                elif args[0] == 'ORDERS':
                    # Makes query for orders
                    # Args needed are args[1-3], customer_id, product_id, amount
                    sql = "INSERT INTO ORDERS (customer_id, product_id, amount) VALUES (%s, %s, %s)"
                    cursor.execute(sql, [args[1], args[2], args[3]])
                    result = "Data added\nCustomer ID: {custID}\nProduct ID: {prodID}\nAmount: {amount} ex.".format(custID=args[1], prodID=args[2], amount=args[3])
                elif args[0] == 'PRODUCT':
                    # Makes query for PRODUCT
                    # Args needed are args[1-3], name, unit, price
                    sql = "INSERT INTO PRODUCT (name, unit, price) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (args[1], args[2], args[3]))
                    result = "Data added\nProduct: {name}\nUnits: {unit} ex.\nPrice: {price}€ each".format(name=args[1], unit=args[2], price=args[3])
                # Comit the query
                connection.commit()

        except Exception as e:
            result = self.errorCodeHandler(e)
        finally:
            connection.close()
        # Returns whatever result we got
        return result

    def update_DB(self, *args):
        result = ""
        # Connection config
        connection = self.db_settings()
        # Modify data
        try:
            with connection.cursor() as cursor:
                # Updates the total units of a product
                # Used by self.order_prepare_insert
                if args[0] == 'productUnit':
                    sql = "UPDATE PRODUCT SET PRODUCT.unit = '%s' WHERE PRODUCT.id = %s"
                    cursor.execute(sql, (args[1], args[2]))
                    result = "Updated product stock."
                # Updates a customer's data
                # Used by self.customer_prepare_modify
                elif args[0] == 'modCustomer':
                    ## If the customerList is 2 (as in only one field to change)
                    if len(args[2]) == 2:
                        ## If that value is phone, change the phone field
                        if args[2][0] == "phone":
                            sql = "UPDATE CUSTOMER SET phone = %s WHERE CUSTOMER.name = %s"
                            cursor.execute(sql, (args[2][1], args[1]))
                            result = "Updated customer: " + args[1]
                        ## If that value is address, change the address field
                        elif args[2][0] == "address":
                            sql = "UPDATE CUSTOMER SET address = %s WHERE CUSTOMER.name = %s"
                            cursor.execute(sql, (args[2][1], args[1]))
                            result = "Updated customer: " + args[1]
                        ## If anything else is put, do wonky msg (shouldn't happen tho)
                        else:
                            result = "Error, not updating neither phone nor address"
                    elif len(args[2]) == 4:
                        sql = "UPDATE CUSTOMER SET phone = %s, address = %s WHERE CUSTOMER.name = %s"
                        cursor.execute(sql, (args[2][1], args[2][3], args[1]))
                        result = "Updated customer: " + args[1]
                elif args[0] == 'modProduct':
                    ## If the productList is 2 (as in only one field to change)
                    if len(args[2]) == 2:
                        ## If that value is unit, change the unit field
                        if args[2][0] == "unit":
                            sql = "UPDATE PRODUCT SET unit = %s WHERE PRODUCT.name = %s"
                            cursor.execute(sql, (args[2][1], args[1]))
                            result = "Updated product: " + args[1]
                        ## If that value is price, change the price field
                        elif args[2][0] == "price":
                            sql = "UPDATE PRODUCT SET price = %s WHERE PRODUCT.name = %s"
                            cursor.execute(sql, (args[2][1], args[1]))
                            result = "Updated product: " + args[1]
                        ## If anything else is put, do wonky msg (shouldn't happen tho)
                        else:
                            result = "Error, not updating neither unit nor price"
                    elif len(args[2]) == 4:
                        sql = "UPDATE PRODUCT SET unit = %s, price = %s WHERE PRODUCT.name = %s"
                        cursor.execute(sql, (args[2][1], args[2][3], args[1]))
                        result = "Updated product: " + args[1]
                # Comit query
                connection.commit()
        except Exception as e:
            result = self.errorCodeHandler(e)
        finally:
            connection.close()
        return result


    def get_from_DB(self, sql):
        # Connection config
        connection = self.db_settings()
        # Try to get data
        try:
            with connection.cursor() as cursor:
                # The query from prepare_select()
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception as e:
            result = self.errorCodeHandler(e)
        finally:
            connection.close()
        return result

    """Returns:
    # [0] = list with only names
    # [1] = dictionary name : id
    """
    def get_customer_list(self, *args):
        sql = "SELECT name, id FROM CUSTOMER"
        # Gets all customers and put them in a list
        users = self.get_from_DB(sql)
        user = []
        userID = {}
        # Iterates the Dict we got, and turns them into list with just names.
        if users:
            for key in users:
                user.append(key['name'])
                userID[key['name']] = key['id']
        # Alphabetical sorting, cuz why not
        user.sort()
        # Adds "None" to start of list, cuz else OptionMenu gets wonky
        user.insert(0, "None")
        return user, userID

    """Returns:
        # List with order ID's only
        """

    def get_order_list(self, *args):
        sql = "SELECT * FROM ORDERS"
        # Gets all orderID's and puts them in a list
        orders = self.get_from_DB(sql)
        result = []
        # Iterates the dict we get from DB and turns into a list with names.
        if orders:
            for key in orders:
                x = str(key['id'])
                result.append(x)
        # Adds "None" to the start of list, cuz else OptionMenu gets wonky
        result.insert(0, "None")
        return result

    """Returns
    # [0] = list with only names
    # [1] = dictionary, name : id
    # [2] = dictionary, name : units
    """

    def get_product_list(self, *args):
        sql = "SELECT name, id, unit, price FROM PRODUCT"
        # Gets all products and their ID and puts them in a list
        db_products = self.get_from_DB(sql)
        db_product = []
        db_productID = {}
        db_productUnit = {}
        db_productPrice = {}
        # Iterates through the dictionary we get back from DB
        if db_products:
            for key in db_products:
                db_product.append(key['name'])
                db_productID[key['name']] = key['id']
                db_productUnit[key['name']] = key['unit']
                db_productPrice[key['name']] = key['price']
        # Alphabetical sorting, cuz why not
        db_product.sort()
        # Adds "None" to start of list, avoiding wonkyness
        db_product.insert(0, "None")
        return db_product, db_productID, db_productUnit

    # Destroys all windows, and rebuilds.
    # Got tired of trying other ways.
    def rebuild_window(self):
        self.frame.destroy()
        self._create_tabs()
        self._layout()

    def errorCodeHandler(self, error):
        # Simple "One place for all error codes"-thingy.
        return {
        1062 : "Dublicate entry was found!",
        1451 : "Entry is tied to a foreign key (orders)\nCan't be deleted until the order tied to this entry is deleted."
        # Panic message! Contact me if this pops up.
        }.get(error.args[0], "Something weird happened, forward this errorcode to me and explain how did you cause it: "+str(error.args[0]))

    ##########
    #The settings for the database, change this:
    ##########
    def db_settings(self):
        connection = pymysql.connect(host='mysql.cc.puv.fi',
                                     user='<username>',
                                     password='<password>',
                                     db='<database>',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection


root = Tk()
# Makes window not resizeable.
root.resizable(0,0)
# Window size
root.geometry("290x390")
# Title on the window
root.title("Python Project")
# "activates"(words pls) the mainClass
app = DBTest(root)
# Main loop for the tkinder
root.mainloop()