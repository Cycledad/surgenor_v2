--SET FOREIGN KEYS OFF INORDER TO DROP & CREATE TABLES
PRAGMA foreign_keys = OFF;
PRAGMA foreign_keys;


DROP TABLE IF EXISTS OrderTbl;
CREATE TABLE OrderTbl (
	id INTEGER NOT NULL,
	OrderNbr INTEGER NOT NULL,
	OrderSupplierId INTEGER NOT NULL,
	deptName TEXT NOT NULL,
	--OrderPartNbr TEXT NOT NULL,
	OrderPartDesc TEXT NOT NULL,
	OrderQuantity INTEGER NOT NULL,
	--OrderUnitId INTEGER NOT NULL,
	OrderPartPrice REAL DEFAULT(0.0) NOT NULL,
	--OrderTotalCost REAL NOT NULL,
	OrderReceivedDate TEXT,
	OrderReceivedBy TEXT,
	OrderReturnDate TEXT,
	OrderReturnQuantity INTEGER,
	PO TEXT,
	OrderUsername TEXT NOT NULL,
	OrderActive BOOLEAN DEFAULT(TRUE) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY(OrderSupplierId) REFERENCES Supplier (id),
	FOREIGN KEY(OrderNbr) REFERENCES purchaseOrder (purchaseOrderNbr)
	--FOREIGN KEY(OrderPartId) REFERENCES Part (id)
);
/*
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(1, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(2, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(3, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(4, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(5, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(6, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(7, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(8, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(9, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
INSERT INTO OrderTbl(OrderNbr, OrderSupplierId, OrderPartId, OrderQuantity, OrderUnitId, OrderPartPrice, OrderTotalCost, orderReceivedDate)
values(10, 1, 1, 1, 1, 20.50, 20.50, DATE('now'));
*/

--- PART TABLE NO LONGER USED
/*
DROP TABLE IF EXISTS Part;
CREATE TABLE Part (
	id INTEGER NOT NULL,
	partNbr TEXT NOT NULL,
	partDesc TEXT NOT NULL,
	partSupplierId INTEGER,
	partQuantity INTEGER NOT NULL,
	partInStock BOOLEAN NOT NULL,
	partDateCreated TEXT DEFAULT DATE() NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE ("partNbr"),
	FOREIGN KEY(partSupplierId) REFERENCES Supplier (id)
);
*/



/*
INSERT into Part(partNbr,PartDesc,partSupplierId,partQuantity,partInStock,partDateCreated) VALUES('A1000', 'BOLT', 1, 20, True, "20220101");
INSERT into Part(partNbr,PartDesc,partSupplierId,partQuantity,partInStock,partDateCreated) VALUES('A2000', 'CHAIN', 2, 20, False, "25122022");
INSERT into Part(partNbr,PartDesc,partSupplierId,partQuantity,partInStock,partDateCreated) VALUES('BBBBB', 'Bottom Bracket Clamp', 2, 20, True, "25122022");
*/

DROP TABLE IF EXISTS PurchaseOrder;
CREATE TABLE PurchaseOrder(
id INTEGER NOT NULL,
purchaseOrderDate TEXT DEFAULT(DATE()) NOT NULL,
purchaseOrderReceivedDate TEXT,
purchaseOrderActive BOOLEAN DEFAULT(TRUE) NOT NULL,
purchaseOrderDateDeleted TEXT,
purchaseOrderNbr INTEGER NOT NULL,
purchaseOrderPurchaserId INTEGER NOT NULL,
purchaseOrderPurchaserDeptId INTEGER NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT)
);

/*
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('02112022', '15122023', False, 1,1,1);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 2,2,1);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 3,2,2);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 4,2,2);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 5,2,2);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 6,2,1);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 7,2,1);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 8,2,1);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 9,2,1);
INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderPurchaserId,purchaseOrderPurchaserDeptId)
values('01121999', '15121999', False, 10,2,1);

*/

DROP TABLE IF EXISTS Purchaser;
CREATE TABLE Purchaser (
	id INTEGER NOT NULL,
	username text not null unique,
	--givenName   TEXT NOT NULL,
	--surname     TEXT NOT NULL,
---	purchaserName TEXT NOT NULL,
	purchaserDeptId INTEGER NOT NULL,
	purchaserActive BOOLEAN NOT NULL,    /* boolean */
	purchaserDateInActive TEXT,
	purchaserDateCreated TEXT DEFAULT(DATE()) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)

);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('kevin', 1, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('admin', 1, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('AlainC', 6, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('ClaudiaD', 1, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('RonBergeron', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('DavidB', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('BenjaminB', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('EricD', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('GabrielI', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('ChristineK', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('LiseL', 6, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('MartinL', 3, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('StephaneR', 4, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('JuniorV', 4, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('NicholasC', 4, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('DanielS', 2, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('FrancisC', 2, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('SimonL', 5, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('BeryM', 5, true);
INSERT INTO Purchaser(username, PurchaserDeptId, purchaserActive) VALUES('JesseyGB', 1, true);




--INSERT INTO Purchaser(givenName, surname, PurchaserDeptId, purchaserActive)
--VALUES('Daniel', 'Savoie', 3, true);

--INSERT INTO Purchaser(givenName, surname, PurchaserDeptId, purchaserActive)
--VALUES('Jessy', 'G-B', 1, true);

--INSERT INTO Purchaser(givenName, surname, PurchaserDeptId, purchaserActive)
--VALUES('Kevin', 'Davis', 1, true);

--INSERT INTO Purchaser(givenName, surname, PurchaserDeptId, purchaserActive)
--VALUES('Ron', 'Bergeron', 5, true);

--INSERT INTO Purchaser(givenName, surname, PurchaserDeptId, purchaserActive)
--VALUES('Simon', 'Landreville', 2, true);

DROP TABLE IF EXISTS Supplier;
CREATE TABLE Supplier (
	id INTEGER NOT NULL,
	supplierName TEXT NOT NULL,
	--supplierAddr TEXT NOT NULL,
	supplierProv TEXT NOT NULL,
	--supplierTel TEXT NOT NULL,
	--supplierEmail TEXT NOT NULL,
	--supplierContact TEXT NOT NULL,
	supplierActive BOOLEAN NOT NULL,    /* boolean */
	--supplierDateInActive TEXT,
	supplierDateCreated TEXT DEFAULT(DATE()) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
	--UNIQUE (supplierAddr),
	--UNIQUE (supplierTel),
	--UNIQUE (supplierEmail),
	--UNIQUE (supplierContact)
);

INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('Benson', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('Fournitures De Bureau Denis', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('Gama', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('Pieces D''Auto Le Bon Choix', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('LKQ', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('AUTO VALUE', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('NAPA', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('LAR', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('TIRE LINK', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('STOX', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('FRISBY TIRE', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('DAI DIRECT AUTO IMPORT', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('TRANSBEC', 'QC', true);
INSERT INTO Supplier(supplierName, supplierProv, supplierActive) values('CANTEEN', 'QC', true);

/*
INSERT INTO Supplier(supplierName, supplierAddr, supplierTel, supplierEmail, supplierContact, supplierActive, supplierDateCreated)
values('Canadian Tire', '2 Dump Road', '613-123-4568', 'supplierx@email.com', 'Mr. Wrong', true, '28012022');
INSERT INTO Supplier(supplierName, supplierAddr, supplierTel, supplierEmail, supplierContact, supplierActive, supplierDateCreated)
values('Window Max', '2 Glass Road', '613-123-4568', 'supplierx@email.com', 'Mr. Wright', true, '28012022');
*/


--- unit no longer used
/*
DROP TABLE IF EXISTS Unit;
CREATE TABLE Unit (
	id INTEGER NOT NULL,
	unitDesc TEXT NOT NULL,
	PRIMARY KEY ("id" AUTOINCREMENT)
);

INSERT INTO Unit(unitDesc) values('KG');
INSERT INTO Unit(unitDesc) values('POUNDS');
INSERT INTO Unit(unitDesc) values('PIECES');
*/


DROP TABLE IF EXISTS OrderNbrTbl;
CREATE TABLE OrderNbrTbl (
	orderNbr INTEGER NOT NULL unique

);

--insert into OrderNbrTbl values(0);

drop table if exists Department;
CREATE TABLE Department (
	id	INTEGER,
	deptName TEXT NOT NULL UNIQUE,
	dateCreated	INTEGER DEFAULT(DATE()) NOT NULL,
	active BOOLEAN NOT NULL,    /* boolean */
	dateInActive TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO Department(deptName, active) values('Finance', true);
INSERT INTO Department(deptName, active) values('Parts', true);
INSERT INTO Department(deptName, active) values('Sales', true);
INSERT INTO Department(deptName, active) values('Service', true);
INSERT INTO Department(deptName, active) values('BodyShop', true);
INSERT INTO Department(deptName, active) values('Admin', true);

--note, givenName & surname in table User should match givenName & surname in Purchaser table ... im not using foreign keys
drop table if exists User;
CREATE TABLE User (
	id	INTEGER,
	givenName   TEXT NOT NULL,
	surname     TEXT NOT NULL,
	username	TEXT NOT NULL UNIQUE,
	password	TEXT NOT NULL UNIQUE,
	createDate	TEXT DEFAULT(DATE()) NOT NULL,
	active	BOOLEAN DEFAULT(TRUE) NOT NULL, /* boolean */
	dateInActive TEXT,
	securityLevel INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT));


insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('admin', '$2b$12$QFMmOK4vmBjhXUcPYjUATe7bxuiFCmBUG2xvc8mpLqM8T8wr9piFm', 'admin', 'admin', DATE('now'), True, 5);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('kevin', '$2b$12$QvBCaPauAgQsJEEhBv8lSusozWKYlDRr.SBjHLLqaWNUMZ7sH2c.W', 'Kevin', 'Davis', DATE('now'), True, 5);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('JesseyGB', '$2b$12$HOD9pOgXvghsww3n4q07..fvbpTjwCD2xW66BG.SMczbq6SOlZZgu', 'Jessey', 'Gromoll-Branchaud', DATE('now'), True, 5);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('AlainC', '$2b$12$yHpt2OwHMl9BQumcxa0jz.7kJ6ojSkMHT3snTr4weWgvRpUxkMJMK', 'ALAIN', 'CHARETTE', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('ClaudiaD', '$2b$12$PZp3wbXsiOjHfMTL9FAdZ.MX1n4vqYSxdmn//fvwp9ll5q7dpC32G', 'CLAUDIA', 'DUSHIME', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('RonBergeron', '$2b$12$X/UJEmoblfmu/BudPl7kJ.vkdKsBGPChrG1pClCvU..Qe2NUS7vOi', 'RON', 'BERGERON', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('DavidB', '$2b$12$1sYOJLhZoQk7Voh9C6a4BOyEyIxFFF3rOdgpxpxzFtHCX9iVuuXBa', 'DAVID', 'BOISSELY', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('EricD', '$2b$12$46ckdTUHTio2FlUw8hfJbeVDfYEOZgs2ymptNB/x5ZxR7I55r44Cy', 'ERIC', 'DAGENAIS', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('GabrielI', '$2b$12$tgWNSbMqX/w2FolAdvZKcuFtZMbmiakb0nqT9ZPPtkJdYsPGlx7BG', 'GABRIEL', 'IONETE', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('ChristineK', '$2b$12$IE0Jf1gudM2WVZQii4zw9OJNSljIc9RldaA3sgHXhxQ/nFzX2pDLe', 'CHRISTINE', 'KNIGHT', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('LiseL', '$2b$12$rTXuZZJ.jf5DiEyKm8o51ed0VbyNYJObnfGPlL6iYrKlUF6I3MFDq', 'LISE', 'LEDUC', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('StephaneR', '$2b$12$KQiPeEF06tdvrBL6ybhGJe7tDoxFrzyLxQMtSxi5X6HFI6lfd3UzW', 'STEPHANE', 'ROBITAILLE', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('JuniorV', '$2b$12$aY6mhe5Xz7fNng.Uc0aHFuKvq2zDvfmjGTXrVEoTl547xERBJma1C', 'JEAN-MARC (JUNIOR)', 'VALLIERES', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('NicholasC', '$2b$12$lSBJK861h2ZwZ.zGpJK4Uurt8p3zcSJI/929r9RZZeuQABHmUdKNe', 'NICHOLAS', 'CHARTRAND', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('DanielS', '$2b$12$t7KLgUs3kLyrHpykzn58ZODtAwJqYtYqKkZZBDRzgyfHsm3DDxQS6', 'DANIEL', 'SAVOIE', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('FrancisC', '$2b$12$GsgpFJxgcWyQxP.YNzCKG.L1QPTBKwaLIUy4lodM6zkymE6v18eo.', 'FRANCIS', 'CHARBONNEAU', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('SimonL', '$2b$12$xpnG74u5kahNrHu6449wu.q3uBDz15VGbik0hoBed4zRCtzouOYj2', 'SIMON', 'LANDREVILLE', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('BeryM', '$2b$12$zas2tthe5FQ8sY1EMnr4BOHwvthVpIK6B/t1A4e.8kj66gx2mT5WK', 'BERY', 'MEDIKA', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('MartinL', '$2b$12$zbaagiBSdDyjAJ3CSacg1e0LzcL6SJBonli5W7l94.SagV1wNq6By', 'MARTIN', 'LEGARE', DATE('now'), True, 0);
insert into user (username, password, givenName, surname, createDate, active, securityLevel) values('BenjaminB', '$2b$12$HX9oxlh6Qdvprm/PQffl.eLSrrDI.0qTam0.sEfWuB9O5oyqB6Sz2', 'BENJAMIN', 'BONIN', DATE('now'), True, 0);




drop table if exists ProvincialTaxRates;
CREATE TABLE ProvincialTaxRates (
	id	INTEGER,
	provincialCode TEXT NOT NULL UNIQUE,
	taxRate	float NOT NULL,
	label TEXT NOT NULL,
	active BOOLEAN DEFAULT(TRUE) NOT NULL,    /* boolean */
	PRIMARY KEY("id" AUTOINCREMENT)
);

insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('QC', 14.975, 'Sales tax rate (PST+QST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('ON', 13, 'Sales tax rate (HST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('AB', 5, 'Sales tax rate (GST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('BC', 12, 'Sales tax rate (PST+GST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('MB', 12, 'Sales tax rate (PST+GST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('NB', 15, 'Sales tax rate (HST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('NL', 15, 'Sales tax rate (HST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('NT', 5, 'Sales tax rate (GST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('NS', 15, 'Sales tax rate (HST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('NU', 5, 'Sales tax rate (GST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('PE', 15, 'Sales tax rate (HST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('SK', 11, 'Sales tax rate (PST+GST) %', 1);
insert into ProvincialTaxRates(provincialCode, taxRate, label, active) values('YK', 5, 'Sales tax rate (GST) %', 1);

PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;