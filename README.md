# LittleLemon
LittleLemon capstone project from meta back-end developer specialization on coursera.

## Endpoints to test and their functionality of API project
### DB configuration
***I added db credentials in db.cnf file at the base dir of project. Please enter your local db credentials for everything to work and then perform migrations.***

### Web Page
- Static content
    - `/restaurant/menu/` **web page!** (check in browser)
        - Note: index.html in exercises is different from index.html from assets. I included the template from assets and configured for static content to show.

### API endpoints
- Authentication - djoser + drf token authentication
    - `/auth/users/` - POST to create new user with username and password. GET to get yourself or all users if you are admin.
        - **Note: Bad url - trailing slash - djoser by default**
    - `/auth/token/login` - to get token via djoser
    - `/auth/token/logout` to delete token
    - `/restaurant/menu/api-auth-token` to get authentication token
        - **Note: Bad endpoint because followed description of exercises.**
- Menu api - generics
    - `/restaurant/menu/items` - GET to retrieve all items, POST to create a new one with all models fields in payload.
    - `restaurant/menu/items/{menuItemId}` - GET to retrieve a particular item, PUT to change it and DELETE to delete it.
    - payload example
        ```json
        {
            "title": "Cheeseburger",
            "price": "10.99",
            "inventory": 10
        }
        ```
- Booking api - viewset (***Bearer token needed!***)
    - `/restaurant/booking/tables` - GET, POST to create and list booking
    - `/restaurant/booking/tables/{bookingId}` - to get, delete and change booking.
    - payload example
        ```json
        {
            "name": "Name",
            "no_of_guests": 3,
            "booking_date": "2024-05-15T22:10:00Z"
        }
        ```

### Testing
- Unit Tests
    - test_models - test menu item creation
    - test_views - menu items list method test