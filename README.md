# Charitably
## What is Charitably?
Charitably was inspired by my family's tradition of collective giving. Every year, during the holidays my family puts together a list of notable charitable organizations that they would like to give to at the end of the year. Each member of the family is asked to provide a small handful of organizations that they think are worthy of support and present them to the family during the Thanksgiving holiday. Afterwards a each family member is allowed to allocate a portion of a collective funding pool to any of the organizations that where presented. However, as the younger generation has grown and moved off to college, and during times when it isn't possible for the family to gather, this process has become harder to manage. Charitably was built to allow us to carry out this tradition online wherever life might find us at the moment. Charitably allows groups to collectively allocate charitable giving. Users are able to propose organizations that they would like to give to and then allocate donations from a collective giving fund.

Charitably was created as my final project for CSE-183 (Web Development) in Spring of 2021 while attending The University of California Santa Cruz. It is built using py4web, Vue.js, and Bulma css. It's a work in progress and you probably shouldn't try to deploy it.

---
## Usage
Unauthenticated users are presented with the following landing page. They can access the account creation option from the hamburger menu in the top right.

![Screenshot1](./Images/Screenshots/Screenshot1.png)

From here users can choose to sign in if they have an existing account or create a new account.

![Screenshot2](./Images/Screenshots/Screenshot2.png)

The Account Creation Page

![Screenshot4](./Images/Screenshots/Screenshot4.png)

After creating an account users can log in to the system using their email and password.

![Screenshot5](./Images/Screenshots/Screenshot5.png)

A new users will not be a part of any giving groups and must either create a new group or be added to another group by that groups admin. Click manage groups to create a new group.

![Screenshot6](./Images/Screenshots/Screenshot6.png)

The group management screen. From here, users can create new giving groups and add other users to groups that they manage.

![Screenshot7](./Images/Screenshots/Screenshot7.png)

When creating a group users can give the group a name, description, and default funding.

![Screenshot8](./Images/Screenshots/Screenshot8.png)

Once the user is a member of one or more groups they will be shown on the users home page. Clicking on a giving groups card will allow them to view suggest organizations the group might want to give to, view other proposed organizations, or allocate their portion of the funding pool.

![Screenshot9](./Images/Screenshots/Screenshot9.png)

This group has no propoposals yet 

![Screenshot10](./Images/Screenshots/Screenshot10.png)

Users can click the plus button to propose an organization that they would like to give to.

![Screenshot11](./Images/Screenshots/Screenshot11.png)

Clicking the checkmark will add the organization to the list of orgs wich the user would like to allocate funding to and then they can choose the ammount they would like to allocate. If their total allocations go over their allowance then the sum will highlight in red.

![Screenshot12](./Images/Screenshots/Screenshot12.png)

Clicking the View Report Button will give a summary of the groups allocations including each group memebers individual allocations and then a summary wich provides the total allocations given to each organization.

![Screenshot13](./Images/Screenshots/Screenshot13.png)
---
## Future Improvements
- [ ] A proper authentication system - Charitably currently uses a very rudimentary authentication system (please don't use Charitably in it's current state...) I would like to build out a more secure authentication system so that Charitably could be safely deployed to internet facing servers. I would also like to include oauth so that users can create accounts using their existing Google Accounts.
- [ ] A proper docker image to simplify deployment
- [ ] Database improvements - Charitably currently uses a sql light datbase that runs as part of the py4web server. I would like to add the ability to connect to a separate database system so that the database can be run on it's own server / container.
- [ ] UI improvements.
- [ ] Better user management - I would like to be able to search for users, invite users (via email), remove users from groups etc.
- [ ] and so much more... (see projects page)