# Inventory-Management
An inventory management system built with Flask and MySQL that allows users to track, manage, and report on product movements, quantities, and locations efficiently.

## Features
- Keep track of products and their quantities.
- Manage stock movements (incoming and outgoing).
- Generate Excel reports on product movements.

## How to Set Up the Project

### Clone the Repository

First, you need to get a copy of the project on your computer. Open a terminal or command prompt and run:
`git clone https://github.com/kavearhasi/Inventory-Management.git`

### Set Up the MySQL Database

You need to have MySQL installed to store the data. 

Create a new MySQL database:
    
`CREATE DATABASE inventory;`

create all the database tables provided in the database_structure folder



### Install Python and Dependencies

Navigate to the project directory and install the dependencies which are provided in the requirement.txt

### Run the Application

Start the Flask application by running:
`flask run`

## How to Use the Application
- Register to the system.
- Log in to the system using your credentials.
- Manage Products: Add new products to the inventory.
- Manage Warehouses: Add new warehouses.
- Track Movements: Record product movements (incoming, outgoing, or transfers).
- Generate Reports: Export inventory data as Excel reports.

## Technologies Used

- Flask: A web framework for Python.
- MySQL: The database used to store product and movement data.
- Pandas: A Python library used to generate Excel reports.
