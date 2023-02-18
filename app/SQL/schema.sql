--SET FOREIGN KEYS OFF INORDER TO DROP & CREATE TABLES
PRAGMA foreign_keys = OFF;
PRAGMA foreign_keys;


DROP TABLE IF EXISTS OrderTbl;
CREATE TABLE OrderTbl (
	id INTEGER NOT NULL,
	OrderNbr INTEGER NOT NULL,
	OrderSupplierId INTEGER,
	deptName TEXT,
	OrderPartNbr TEXT,
	OrderPartDesc TEXT,
	OrderQuantity INTEGER NOT NULL,
	--OrderUnitId INTEGER NOT NULL,
	OrderPartPrice REAL NOT NULL,
	--OrderTotalCost REAL NOT NULL,
	OrderReceivedDate TEXT,
	OrderReceivedBy TEXT,
	OrderReturnDate TEXT,
	OrderReturnQuantity INTEGER,
	PO TEXT,
	OrderUsername TEXT,
	OrderActive BOOLEAN,
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

/*
DROP TABLE IF EXISTS Part;
CREATE TABLE Part (
	id INTEGER NOT NULL,
	partNbr TEXT NOT NULL,
	partDesc TEXT NOT NULL,
	partSupplierId INTEGER,
	partQuantity INTEGER NOT NULL,
	partInStock BOOLEAN NOT NULL,
	partDateCreated TEXT NOT NULL,
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
purchaseOrderDate TEXT NOT NULL,
purchaseOrderReceivedDate TEXT,
purchaseOrderActive BOOLEAN NOT NULL,
purchaseOrderDateDeleted TEXT,
purchaseOrderNbr INTEGER,
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
	purchaserName TEXT NOT NULL,
	purchaserDeptId INTEGER NOT NULL,
	purchaserActive BOOLEAN NOT NULL,    /* boolean */
	purchaserDateInActive TEXT,
	purchaserDateCreated TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE (purchaserName)
);

INSERT INTO Purchaser(purchaserName, PurchaserDeptId, purchaserActive, purchaserDateCreated)
VALUES('Daniel Savoie', 3, true, DATE('now'));

INSERT INTO Purchaser(purchaserName, PurchaserDeptId, purchaserActive, purchaserDateCreated)
VALUES('Jessy G-B', 1, true, DATE('now'));

INSERT INTO Purchaser(purchaserName, PurchaserDeptId, purchaserActive, purchaserDateCreated)
VALUES('Kevin Davis', 1, true, DATE('now'));

INSERT INTO Purchaser(purchaserName, PurchaserDeptId, purchaserActive, purchaserDateCreated)
VALUES('Ron Bergeron', 5, true, DATE('now'));

INSERT INTO Purchaser(purchaserName, PurchaserDeptId, purchaserActive, purchaserDateCreated)
VALUES('Simon Landreville', 2, true, DATE('now'));

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
	supplierDateCreated TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
	--UNIQUE (supplierAddr),
	--UNIQUE (supplierTel),
	--UNIQUE (supplierEmail),
	--UNIQUE (supplierContact)
);

INSERT INTO Supplier(supplierName, supplierProv, supplierActive, supplierDateCreated)
values('Benson', 'QC', true, DATE('now'));
/*
INSERT INTO Supplier(supplierName, supplierAddr, supplierTel, supplierEmail, supplierContact, supplierActive, supplierDateCreated)
values('Canadian Tire', '2 Dump Road', '613-123-4568', 'supplierx@email.com', 'Mr. Wrong', true, '28012022');
INSERT INTO Supplier(supplierName, supplierAddr, supplierTel, supplierEmail, supplierContact, supplierActive, supplierDateCreated)
values('Window Max', '2 Glass Road', '613-123-4568', 'supplierx@email.com', 'Mr. Wright', true, '28012022');
*/

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
	dateCreated	INTEGER NOT NULL,
	active BOOLEAN NOT NULL,    /* boolean */
	dateInActive TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO Department(deptName, dateCreated, active) values('Finance', DATE('now'), true);
INSERT INTO Department(deptName, dateCreated, active) values('Parts', DATE('now'), true);
INSERT INTO Department(deptName, dateCreated, active) values('Sales', DATE('now'), true);
INSERT INTO Department(deptName, dateCreated, active) values('Service', DATE('now'), true);
INSERT INTO Department(deptName, dateCreated, active) values('BodyShop', DATE('now'), true);


drop table if exists User;
CREATE TABLE User (
	id	INTEGER,
	username	TEXT NOT NULL UNIQUE,
	password	TEXT NOT NULL UNIQUE,
	createDate	TEXT,
	active	BOOLEAN,
	dateInActive TEXT,
	securityLevel INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT));


insert into user (username, password, createDate, active, securityLevel) values('admin', '$2b$12$QFMmOK4vmBjhXUcPYjUATe7bxuiFCmBUG2xvc8mpLqM8T8wr9piFm', DATE('now'), True, 5);
insert into user (username, password, createDate, active, securityLevel) values('kevin', '$2b$12$QvBCaPauAgQsJEEhBv8lSusozWKYlDRr.SBjHLLqaWNUMZ7sH2c.W', DATE('now'), True, 5);

drop table if exists ProvincialTaxRates;
CREATE TABLE ProvincialTaxRates (
	id	INTEGER,
	provincialCode TEXT NOT NULL UNIQUE,
	taxRate	float NOT NULL,
	label TEXT NOT NULL,
	active BOOLEAN NOT NULL,    /* boolean */
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