#Little Lemon Restaurant API Project
Welcome to the Little Lemon Restaurant API project! This project provides a fully functioning API that allows client application developers to build web and mobile applications for the restaurant. The API is built using Django Rest Framework (DRF) for handling API endpoints and Djoser for user authentication and token generation.

#Overall Capabilities
The Little Lemon Restaurant API offers a wide range of capabilities to support various user roles and functionalities:

User Registration and Authentication: Users can register with the API by providing their name, email, and password. The API handles user authentication and token generation through Djoser, allowing users to obtain access tokens for further API calls.

Menu Items Management: Customers and delivery crew can browse the list of menu items available. Managers have additional privileges to create, update, and delete menu items. Customers can add menu items to their cart.

User Role Management: Managers can create and manage two user groups - "Manager" and "Delivery crew." Users can be assigned to these groups or removed from them.

Cart Management: Customers can view the current items in their cart and add new items. They can also clear the cart by deleting all items.

Order Placement: Customers can place orders, which include items from their cart. Upon order placement, the items are moved from the cart to the order items table.

Order Management: Customers can view their own orders, while managers can view all orders placed by users. Managers can also update orders by assigning delivery crew and changing order status.

Delivery Status Management: Delivery crew can view orders assigned to them and update the delivery status (0 - out for delivery, 1 - delivered) for the orders they are handling.

#Technologies Used
The Little Lemon Restaurant API is built using the following technologies:

Django: A powerful and popular web framework for building web applications in Python.

Django Rest Framework (DRF): An extension of Django that simplifies building RESTful APIs, providing serializers, views, and other utilities.

Djoser: A Django app that provides user authentication endpoints, including user registration and token generation.

Pipenv: A virtual environment manager for Python projects, used for managing dependencies.


#API Endpoints
User Registration and Token Generation
POST /api/users

Role: No role required
Purpose: Creates a new user with name, email, and password.
GET /api/users/users/me/

Role: Anyone with a valid user token
Purpose: Displays only the current user.
POST /token/login/

Role: Anyone with a valid username and password
Purpose: Generates access tokens that can be used in other API calls in this project.
Menu Items Endpoints
GET /api/menu-items

Role: Customer, delivery crew
Purpose: Lists all menu items.
POST, PUT, PATCH, DELETE /api/menu-items

Role: Customer, delivery crew
Purpose: Denies access and returns 403 - Unauthorized HTTP status code.
GET /api/menu-items/{menuItem}

Role: Customer, delivery crew
Purpose: Lists a single menu item.
POST, PUT, PATCH, DELETE /api/menu-items/{menuItem}

Role: Customer, delivery crew
Purpose: Returns 403 - Unauthorized.
GET /api/menu-items

Role: Manager
Purpose: Lists all menu items.
POST /api/menu-items

Role: Manager
Purpose: Creates a new menu item and returns 201 - Created.
GET /api/menu-items/{menuItem}

Role: Manager
Purpose: Lists a single menu item.
PUT, PATCH /api/menu-items/{menuItem}

Role: Manager
Purpose: Updates a single menu item.
DELETE /api/menu-items/{menuItem}

Role: Manager
Purpose: Deletes a menu item.
User Group Management Endpoints
GET /api/groups/manager/users

Role: Manager
Purpose: Returns all managers.
POST /api/groups/manager/users

Role: Manager
Purpose: Assigns the user in the payload to the manager group and returns 201 - Created.
DELETE /api/groups/manager/users/{userId}

Role: Manager
Purpose: Removes this particular user from the manager group and returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found.
GET /api/groups/delivery-crew/users

Role: Manager
Purpose: Returns all delivery crew.
POST /api/groups/delivery-crew/users

Role: Manager
Purpose: Assigns the user in the payload to the delivery crew group and returns 201 - Created HTTP.
DELETE /api/groups/delivery-crew/users/{userId}

Role: Manager
Purpose: Removes this user from the manager group and returns 200 - Success if everything is okay. If the user is not found, returns 404 - Not found.
Cart Management Endpoints
GET /api/cart/menu-items

Role: Customer
Purpose: Returns current items in the cart for the current user token.
POST /api/cart/menu-items

Role: Customer
Purpose: Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items.
DELETE /api/cart/menu-items

Role: Customer
Purpose: Deletes all menu items created by the current user token.
Order Management Endpoints
GET /api/orders

Role: Customer
Purpose: Returns all orders with order items created by this user.
POST /api/orders

Role: Customer
Purpose: Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user.
GET /api/orders/{orderId}

Role: Customer
Purpose: Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.
GET /api/orders

Role: Manager
Purpose: Returns all orders with order items by all users.
PUT, PATCH /api/orders/{orderId}

Role: Manager
Purpose: Updates the order. A manager can use this endpoint to set a delivery crew to this order and also update the order status to 0 or 1.
If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.
If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.
DELETE /api/orders/{orderId}

Role: Manager
Purpose: Deletes this order.
GET /api/orders

Role: Delivery crew
Purpose: Returns all orders with order items assigned to the delivery crew.
PATCH /api/orders/{orderId}

Role: Delivery crew
Purpose: A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.
Filtering, Pagination, and Sorting
Proper filtering, pagination, and sorting capabilities have been implemented for the following endpoints:

/api/menu-items
/api/orders

For these endpoints, you can filter, paginate, and sort the results as needed by using appropriate query parameters.



