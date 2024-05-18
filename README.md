# Description

Repo contains project assignment from [Meta-backend Developer Specialization](https://www.coursera.org/professional-certificates/meta-back-end-developer)

There are 2 main projects in my view. Both project related to LittleLemon restaurant API.
1. [Capstone project.](https://www.coursera.org/learn/back-end-developer-capstone?specialization=meta-back-end-developer) This project consist of exercises with step-by-step guide that describes how to build booking and menu APIs for a restaurant. This APIs build using generics and model viewsets so there is no much code but it shows general understanding of main django concepts and how they work altogether. This project was final for specialization.
2. [LittleLemon API.](https://www.coursera.org/learn/apis?specialization=meta-back-end-developer). Even though this project was in the middle of specialization course it was the most challenging because it's stated that the programmer should use only function and class-based views (I understood it as do not use viewsets and generics). So most of the functionality has to be written by the programmer.

## LittleLemon API project description.
### Project description
It's needed to build back-end API that allows customers to browse food items, add items to cart and place orders. Managers would be in charge of user roles and assigning orders to delivery crew. Delivery crew should be able to check orders assigned to them and change their status.

People with different roles will be able to:
- browse, add and edit menu items
- place orders, browse orders
- assign delivery crew to orders
- deliver the orders.

### Project Structure
One single app `LittleLemonAPI` and all endpoints in it. Use `pipenv` for virtual environment.

Only function and class-based views are allowed.

There are 2 main user groups:
1. Managers
2. Delivery crew

Customers are users with no group assigned.

### Status codes
- 200 - successful **get, put, patch, delete** class
- 201 - successful **post** calls
- 401 - unauthorized - if authentication fails
- 403 - Forbidden - if authorization fails for the current user token
- 400 - Bad request - validation for **post, put, patch, delete** fails
- 404 - Not Found - non-existing resource

**Issue with task decription:** In the task decription codes for unauthorized and forbidden statuses are confused. To be clear
- 401 - lacks valid authentication credentials
- 403 - not enough permissions

### API endpoints
#### User authentication
Djoser is allowed!
- `/api/users`
    - POST
        - creates new user with `name`, `email` and `password` 201
        - 400 - Bad request if some field not valid. *Email is not required?* **TODO**
- `/api/users/me`
    - GET
        - displays current user **if token is valid** 200
        - 401 unauthorized **otherwise**
- `/token/login`
    - POST 
        - generates token for valid username and password in payload. 201
        - 400 badRequest **otherwise**

#### Menu-items endpoints
- `/api/menu-items`
    - GET
        - Invalid token - 401
        - **Any Role:** list all menu items - 200
    - POST
        - Invalid token - 401
        - **Customer, Delivery crew** - 403
        - **Manager**
            - invalid payload - 400
            - create new menu item - 201
    - PUT, PATCH, DELETE
        - not implemented 405(**Issue: Description said 403 for not manageres**)
- `/api/menu-items/{menuItemId}`
    - GET
        - Invalid token - 401
        - Not Found - 404
        - **AnyRole:** List single menu items - 200
    - POST
        - not implemented 405 (**Issue: Description said 403 for not manageres**)
    - PUT
        - Invalid token - 401
        - **Customer, Delivery Crew** - 403
        - **Managers**
            - Not Found - 404
            - Invalid payload - 400
            - Updates single menu item - 200
    - PATCH
        - Invalid token - 401
        - **Customer, Delivery Crew** - 403
        - **Managers**
            - Not Found 404
            - Invalid payload - 400 ??? **(TODO READ - extra fields to the payload)**
            - Updates single menu item - 200
    - DELETE
        - Invalid token - 401
        - **Customer, Delivery Crew** - 403
        - **Managers**
            - Not Found 404
            - Deletes item - 200

#### User group management endpoints
Delivery crew and customers not stated in endpoint description for the project => 403 unauthorized considered.
- `/api/groups/manager/users`
    - Invalid Token - 401
    - **Customer, Delivery crew** - 403
    - **Manager**
        - GET - all managers 200
        - POST
            - Invalid payload 400
            - User Not Found 404
            - Assign the user in the payload to the manager group - 201
    - Other methods - not implemented 501
- `/api/groups/manager/users/{userId}`
    - Invalid Token - 401
    - **Customer, Delivery crew** - 403
    - **Manager**
        - DELETE
            - Not Found - 404
            - Removes user from managers - 200
- `/api/groups/delivery-crew/users`
    - Invalid Token - 401
    - **Customer, Delivery crew** - 403
    - **Manager**
        - GET - all delivery crew 200
        - POST
            - Invalid payload 400
            - User Not Found 404
            - Assign the user in the payload to the delivery crew group - 201
- `/api/groups/delivery-crew/users/{userId}`
    - Invalid Token - 401
    - **Customer, Delivery crew** - 403
    - **Manager**
        - DELETE 
            - user not found - 404
            - removes user from delivery group - 200
            
#### Cart management endpoints
Managers and delivery crew not stated - 403 considered by me (**Restrict staff to make orders and add items to cart!**)
- `/api/cart/menu-items`
    - Invalid Token - 401
    - **Manager, Delivery crew** - 403
    - **Customer**
        - GET
            - all items for current user - 200
        - POST
            - invalid payload - 400
            - No menu item found - 400
            - Add new item to the cart - 201
        - DELETE
            - deletes all items - 200

#### Order Management endpoints
- `/api/orders`
    - GET
        - Invalid Token - 401
        - **Customer**
            - all customer **orders with order items** 200
        - **Manager**
            - **all orders with order items** to all users 200
        - **Delivery crew**
            - **all orders with order items** assigned to this delivery - 200
    - POST
        - Invalid Token - 401
        - **Customer**
            - if cart is empty - 400
            - **creates new order for current user with items from cart, deletes cart for user!** - 201
        - **Managers, Delivery Crew not stated in description** - Forbidden 403
- `/api/orders/{orderId}`
    - GET
        - Invalid Token - 401
        - **Customer**
            - Order not found 404
            - Order belongs to another user 403
            - Returns all items for order id 200
        - **Managers, Delivery crew** always show an order items 200 or 404
    - PUT
        - Invalid Token - 401
        - **Customer, Delivery Crew not stated** - 403
        - **Managers**
            - Order not found 404
            - Invalid payload 400
            - Updates the order 200 (set delivery crew or change status)
    - PATCH
        - Invalid Token - 401
        - **Customer not stated** - 403
        - **Delivery Crew**
            - Order not found 404
            - Order not assigned to del crew - 403
            - update only status (0, 1) 200
        - **Managers**
            - Order not found 404
            - Updates the order 200 (set delivery crew or change status)
    - DELETE
        - Invalid token - 401
        - **Customer, Delivery Crew** - 403
        - **Managers**
            - Order not found 404
            - Delete order

### Additional functionality
Proper filtering, pagination, sorting capabilities for menu-items and orders endpoints

Filtering:
- Orders by status
- menu-items by categories and price ranges
Searching
- Orders by customer
- Menu-items by title, category__title
Throttling
- 5 calls per min

### Examples of payloads
#### Creating a new user `/api/users`
```json
{
    "username": "UserName",
    "password": "Password123!",
    "email": "email@email.com"
}
```

#### Getting token `/token/login/`
```json
{
    "username": "UserName",
    "password": "Password123!",
}
```

#### Creating menu item `/api/menu-items`
```json
{
    "title": "NewItem",
    "price": "10.99",
    "category_id": 1
}
```

#### Updating menu item `/api/menu-items/{menuItemId}`
PUT:
```json
{
    "title": "NewItemPUT",
    "price": "10.99",
    "category_id": 1
}
```

PATCH:
```json
{
    "title": "NewItemPatched",
}
```

#### Assigng users to manager `/api/groups/manager/users` or delivery crew `/api/groups/delivery-crew/users`
```json
{
    "id": 3 //user id
}
```

#### Cart item creation or update `/api/cart/menu-items`
```json
{
    "menu_item_id": 1,
    "quantity": 10,
}
```

#### Order status and delivery crew update `/api/orders/{orderId}`
PUT:
```json
{
    "status": true,
    "delivery_crew_id": 4
}
```

PATCH:
```json
{
    "status": true
}
```
