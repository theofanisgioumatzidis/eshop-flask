# My E-Shop
#### Video Demo:  <URL HERE>
#### Description:

This project is a web application using flask that depicts an eshop called "My E-Shop" that is styled to be used by both desktop and mobile devices. The eshop contains smartphones and laptops that the user after login can add to cart, then checkout the cart and lastly see the order along with any previous orders that the user has placed in the past.

Technologies used:
- Flask
- Sqlite 3
- Bootstrap
- jquery


# How the webpage works

### <ins>Before log in</ins>

If the user tries to access "/orders", "/cart" or “/checkout” while not logged in, he/she will be redirected to the login page.

- Layout

The basic visual structure of the site consists of the top and bottom bars and every page adds in between. In the bottom bar the "copyright" is displayed. In the top bar the name of the site is displayed along with four buttons. Menu where it opens up a section in the top bar with the buttons for redirection to each category. The cart button that when pressed redirects the user to the login page. And lastly the login and register buttons that redirects to the corresponding page.

- Homepage

In the homepage, the user is presented with two sections: Smartphones and Laptops where three of each are displayed. Each section has a button with the name of the category that redirects to the corresponding page. When title of each product is pressed, the user is redirected to the corresponding product page.

- Products

In the product page there is a bigger image of the product with the title, the price and an add to cart button. Underneath a description of the product is found along with some specifications. The products are also displayed in the Smartphones and Laptops pages where all the currently active coresponding products are displayed and the user can click on the title to be redirected to the product page.

- Cart

When the "Add to cart" button is pressed in the product page and when the cart button in the top bar is clicked, the user is redirected to the Login page.

- Login/Register

In the Register page there are three forms: Username and Password and confirm. The user can fill the forms and by pressing the Register button, a new account is created and the user is redirected to the login page. If any of the forms are not filled or if the confirm doesn’t match with the password the user is redirected to the Register page along with a bar underneath of the top bar with the problem of the submission. When incorrect confirm is been typed, a message is being displayed dynamically underneath the confirm form stating the problem.

In the Login page there are two forms: Username and Password. The user can fill the forms and by pressing the Login button and will be directed to the homepage along with a flash message stating: “Login successful”. If any of the forms where not filled or if the input was not one of the already registered users, the user will be redirected to the login page with a flash message stating the problem.

### <ins>After log in</ins>

When the user is logged in, the users a flask session is being created and loaded with user info and the cart.

- Layout

The two buttons: Login and Register, now are being replaced with “Welcome, username”, where username is the username of the user, an order button that redirects to the orders page and a logout button that deletes the session and redirects the user to the homepage along with a flash message stating: “Logout successful”.

- Products

 Now the “Add to cart” button adds the product to the cart and a message appears dynamically underneath the cart button stating: “Product added to cart successfully.”

- Cart

When hovered upon the cart button, now the contents of the user’s cart are displayed dynamically by making space underneath the top bar. When the cart button is being clicked, the user is redirected to the cart page. In the Cart page, a list of the products of the user’s cart is displayed along with shipping and the total price. Lastly there is the checkout button that when pressed the cart is being saved as an order and being cleared of the user’s cart and the user is directed to the homepage.

- Orders

When the user clicks on the orders button, he/she is redirected to the orders page. In the Orders page the user is presented with a list of all the orders placed by him/herself with the date price and shipping. When the “Contents” button is being clicked, dynamically appear the contents of the order with each name, price and quantity.

# How it was developed

All the data are stored in a sqlite3 database and then extracted when needed. A helper function was created for easy quering.

Every template uses the layout.html where is imported bootstrap, jquery, the script.js and styles.css along and all the all the meta tags. The top and bottom bar is being configured and in the “main” tag a block is created to allow other templates to add to content to the page. Each page has a template that adds to the layout. Ajacks was used for all the dynamic feature of the site.  
The Passwords are being hashed and stored as so to the database.
The session contains the user id, username and the cart which are drawn from the database.



