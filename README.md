# Member API using Flask
This repository contains implementation of Member and Membership API using Flask and SQL Database

In this Repository we are going to create a Member API using Flask (Python module) and SQLite 3 Database.

# Architecture

![member-api-architecture drawio](https://github.com/user-attachments/assets/9aadf81d-ed76-4c65-b99a-b0676509a8d7)

# Admin, Member and Membership

So the Basic idea of this API is we have Admins and Members, each member will have a active membership (Basic, Mobile, Standard and Premium)

## Admin

Admin will have following details
ID | Name | Username | Email ID | Password | Active Status | Creation Date | Update Date
---| --- | --- | --- | --- | --- | --- | ---
1 | Shreenath Powar | admin | admin@email.com | ***** | 1 | 2025 Jan 20, 21:25:06 | 2025 Jan 20, 21:25:06

Admin can:
  1. login/logout with username/emailid and password
  2. modify/create memberships
  3. activate/deactivate member (cannot create/delete)
  4. change membership of a member.
  5. update their(admin) details
  6. view other admin details (id, name, active status, creation date)
  7. view member details (id, name, active status, membership, creation date)
  8. deactivate/delete (admin can delete and update only their active status)
  9. change active status of other admins
  10. delete account

## Member

Member will have following details
ID | Name | Username | Email ID | Password | Active Status | Creation Date | Update Date
---| --- | --- | --- | --- | --- | --- | ---
1 | Shreenath Powar | sheenathpowar | shreenathpowar@email.com | ***** | 1 | 2025 Jan 20, 21:25:06 | 2025 Jan 20, 21:25:06

Member can:
  1. login/logout with username/emailid and password
  2. create member (with no membership assigned)
  3. deactivate/delete account
  4. update their details

## Membership

So basically we will have these four memberships Basic, Mobile, Standard and Premium.
Admins can modify them and create new memberships and delete current.

membership will have following details

ID | Name | Adds Level | Max Resolution | Active Status | Creation Date | Update Date
---| --- | --- | --- | --- | --- | --- 
1 | Basic | 2 | 720p | 1 | 2025 Jan 20, 21:25:06 | 2025 Jan 20, 21:25:06
