-- Create Tables
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100),
    City VARCHAR(50),
    SignupDate DATE
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10,2)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    ProductID INT FOREIGN KEY REFERENCES Products(ProductID),
    Quantity INT,
    OrderDate DATE,
    TotalAmount DECIMAL(10,2)
);

-- Insert Customers
INSERT INTO Customers VALUES
(1,'Aarav','Sharma','aarav.sharma@email.com','Mumbai','2024-01-15'),
(2,'Priya','Nair','priya.nair@email.com','Bengaluru','2024-02-20'),
(3,'Rohan','Mehta','rohan.mehta@email.com','Delhi','2024-03-05'),
(4,'Ananya','Iyer','ananya.iyer@email.com','Chennai','2024-03-22'),
(5,'Vikram','Singh','vikram.singh@email.com','Pune','2024-04-10'),
(6,'Sneha','Reddy','sneha.reddy@email.com','Hyderabad','2024-05-01'),
(7,'Karan','Joshi','karan.joshi@email.com','Ahmedabad','2024-05-18'),
(8,'Diya','Kapoor','diya.kapoor@email.com','Kolkata','2024-06-02'),
(9,'Arjun','Pillai','arjun.pillai@email.com','Mumbai','2024-06-25'),
(10,'Meera','Rao','meera.rao@email.com','Bengaluru','2024-07-08');

-- Insert Products
INSERT INTO Products VALUES
(1,'Wireless Mouse','Electronics',599.00),
(2,'Mechanical Keyboard','Electronics',2499.00),
(3,'USB-C Hub','Electronics',1299.00),
(4,'Running Shoes','Footwear',3299.00),
(5,'Yoga Mat','Fitness',899.00),
(6,'Protein Shaker','Fitness',349.00),
(7,'Backpack','Accessories',1899.00),
(8,'Water Bottle','Accessories',499.00),
(9,'Desk Lamp','Home',1099.00),
(10,'Bluetooth Speaker','Electronics',1799.00);

-- Insert Orders
INSERT INTO Orders VALUES
(1,1,2,1,'2024-07-01',2499.00),
(2,2,4,1,'2024-07-02',3299.00),
(3,3,1,2,'2024-07-03',1198.00),
(4,4,5,1,'2024-07-04',899.00),
(5,5,7,1,'2024-07-05',1899.00),
(6,6,9,1,'2024-07-06',1099.00),
(7,7,3,1,'2024-07-07',1299.00),
(8,8,10,1,'2024-07-08',1799.00),
(9,9,6,3,'2024-07-09',1047.00),
(10,10,8,2,'2024-07-10',998.00),
(11,1,8,1,'2024-07-12',499.00),
(12,3,10,1,'2024-07-14',1799.00),
(13,5,2,1,'2024-07-15',2499.00),
(14,2,6,2,'2024-07-16',698.00),
(15,9,4,1,'2024-07-18',3299.00);
