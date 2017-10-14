# python_project
#Project work for 2016 Python Course

Python Project User Manual

1) Connection to VAMk's MySQL:

	-Connect into VAMK's network (From VAMK or via OpenVPN)
	-Enter to the following website: https://mysql.cc.puv.fi/
		*If the website is not loading, you are not connected into VAMK's network
	-Create an account or enter the username and password
2) MySQL settings:
	
	- Python project has the following tables and columns that should be created if making a new database:
		CUSTOMER
			id
			name
			address
			phone
		ORDERS
			amount
			customer_id
			date
			id
			product_id
		PRODUCTS
			id
			name
			price
			unit

	- To get the date in ORDERS to work correctly, the following settings should be used:	
			name: date, type: TIMESTAMP, default: CURRENT_TIMESTAMP, attributes: on update CURRENT_TIMESTAMP

	- To tie the ID in ORDERS with Customer_id, we need to use foreign keys with the following steps:
			* Go to the Python database
			* Select SQL
			* Run the following code:
				ALTER TABLE `orders`
  				ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON UPDATE CASCADE,
 				ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON UPDATE CASCADE;

3) Using the App

	- The application is separated into 3 sections:
			* CUSTOMER
			* ORDER
			* PRODUCT
	-In addition the app has an update button to refresh the changes made in the database. Ex. For Deleting a Customer

4) CUSTOMER
	 
	Insert 
		- Insert is used for inserting a new customer into SQL database
	
		- The app asks you to fill in the name, address and phone.
			*If any of the information columns is left blank, the data saving will not happen!
			*If the phone number is not properly formatted, the data saving will not happen!
	
		- When the customer is created, it also obtains an unique ID

	Select
		- Select is used for selecting an existing customer
		
		- The customer can be selected by an ID, name or address
		
		- If a customer is found with the inserted values, it is printed below when pressing the Submit button

	Select ALL

		- Select all returns all customers and their informations. Making it easy to find their IDs if needed.

	
	Delete Cust.
		
		- Delete Customer has a droplist for selecting existing customers. Pressing DELETE! will erase all customer data about that person from the SQL
		
		- After it, press "Update" to refresh the view so the deleted customer will be gone. (Brutally)
	
	Modify Cust:

		- Modify Customer can be used by selecting an existing customer from the droplist. 
		  After that you type the values you want to change to either/both New Phone and New address. The submit button will modofy the given values to the customer.
			# If a box is left empty, the value will not be changed meaning you can choose to modify just phone or address if you want. Modifying both at once works too.
			# The phone number needs to be given in valid form. Otherwise the modifying will not happen!

5) ORDER

	Insert
		- Insert is used to create a new order into SQL database
		
		- The app will ask you to select a Buyer from the droplist (existing customer created in Customer section)
		 
		- And a product from Product droplist (existing product created in Product section)
			* The amount of the product in stock will be displayed next to the product
		
		- Amount is used to select how many units you want to buy.
			# The amount given must be a number and above 0. In addition it cannot exceed the amount of product left in the stock.
	
		 To confirm the order, click Submit and your product will be saved into the database.
	
	Select
		- Select is used for selecting an existing order
		
		- The selection can be made by filling in either Order ID, Customer (name) or product ID
	
		- If an order is found with the inserted values, it is printed below when pressing the Submit button

	Select ALL

		- Select all returns all orders and their informations. Making it easy to find their IDs if needed.

	Delete Order

		- Delete Order has a droplist for selecting existing orders. Pressing DELETE! will erase the order data about that order from the SQL
		
		- After it, press "Update" to refresh the view so the deleted order will be gone.


	# ORDER window does not have a modify section, because modifying an on-going order would be illogical.

	
6) PRODUCT	
		
	Insert 
		- Insert is used for inserting a new product into SQL database
	
		- The app asks you to fill in the name, unit and price of the product (unit = amount of product).
			*If any of the information columns is left blank, the data saving will not happen!
			* The unit and price must be numbers and above 0!
	
		- When the product is created, it also obtains an unique ID

	Select
		- Select is used for selecting an existing product
		
		- The product can be selected by an ID, name, price or unit
		
		- If a product is found with the inserted values, it is printed below when pressing the Submit button

	Select ALL

		- Select all returns all products and their informations. Making it easy to find their IDs if needed.

	
	Delete Prod.
		
		- Delete Customer has a droplist for selecting existing customers. Pressing DELETE! will erase all product data about that product from the SQL
		
		- After it, press "Update" to refresh the view so the deleted product will be gone. (Or recycled to save the nature)
	
	Modify Prod:

		- Modify Product can be used by selecting an existing Product from the droplist. 
		  After that you type the values you want to change to either/both New unit amount and New price. The submit button will modify the given values to the product.
			# If a box is left empty, the value will not be changed meaning you can choose to modify just unit or product if you want. Modifying both at once works too.
			# The given values must be numbers and above 0.

7) ENJOY!
	



By: Jere Lyytinen, VAMK, 2016 Python Course
		
