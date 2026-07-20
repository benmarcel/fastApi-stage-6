Implement the following routes for your e-commerce project:

 

For Users:

POST /register

POST /login

POST /forget-password

POST /reset-password

 

POST /admin/register

POST /admin/login

Update your route to add, edit and delete routes to check if a user is logged in and has the admin role before they can take those actions. (This works with "Depends").

 

Every product should have an adminId which is the I.D. of the admin that added the product. One admin should be able to have many products.