import datetime
import os
import random
import sqlite3
import stat


import docx
import webbrowser
import requests


from urllib.parse import urljoin

#from docx2html import convert

# URL for print routine: https://www.youtube.com/watch?v=fziZXbeaegc&list=PL7QI8ORyVSCavY8MYL3dM54SviNlnEA3T&index=11
# for print routine
from pathlib import Path

from docxtpl import DocxTemplate

from app import app, constants

import traceback


def getDatabase(dataBaseName: str) -> str:
    return os.path.join(app.root_path, dataBaseName)


def getConnection(db: str) -> sqlite3.Connection:
    conn = None

    try:
        # database will be created if doesn't already exist
        conn = sqlite3.connect(db)
        # conn = sqlite3.connect(r'C:\Users\wayne\APP\app\mysite.db')

        conn.row_factory = sqlite3.Row

        return conn

    except Exception as e:
        print(f'Could not establish a connection with database {db}, error {e}')


def reloadDatabase():
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        conn.row_factory = sqlite3.Row

        schema = os.path.join(app.root_path, 'SQL\schema.sql')

        with open(schema) as f:
            conn.executescript(f.read())

        conn.close()

    except Exception as e:
        print(f'problem in reloadDatabase: {e}')

def getProvincialTaxRate(provincialCode: str) -> list:
    try:
        row: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (provincialCode ,)
        stmt = 'select * from provincialTaxRates where provincialCode = ?'
        cur.execute(stmt, parm)
        row = cur.fetchone()
        # for row in cur:
        #    print(f'row:{row}')

        cur.close()
        conn.close()

        return row

    except Exception as e:
        print(f'problem in getProvincialTaxRate: {e}')


def getUnitDesc(id: int) -> str:
    try:
        row: str = ''
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (id,)
        stmt = 'select unitDesc from unit where id = ?'
        cur.execute(stmt, parm)
        row = cur.fetchone()
        # for row in cur:
        #    print(f'row:{row}')
        #print(f'row: {row[0]}')
        cur.close()
        conn.close()

        return row[0]

    except Exception as e:
        print(f'problem in getUnitDesc: {e}')


def getUnitId(desc: str) -> int:
    try:
        row: int = None
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (desc,)
        stmt = 'select Id from unit where unitDesc = ?'
        cur.execute(stmt, parm)
        row = cur.fetchone()
        #print(f'row: {row[0]}')
        cur.close()
        conn.close()

        return row[0]

    except Exception as e:
        print(f'problem in getUnitId: {e}')


def getALLUnitDesc() -> list:
    try:
        row: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'select unitDesc from unit'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt)
        row = cur.fetchall()
        row = list(row)
        cur.close()
        conn.close()

        return row

    except Exception as e:
        print(f'problem in getALLUnitDesc: {e}')


def getPartId(Desc: str) -> int:
    try:
        row: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (Desc,)
        stmt = 'select Id from Part where partNbr = ? and partInStock is True'
        cur.execute(stmt, parm)
        row = cur.fetchone()

        cur.close()
        conn.close()

        return row[0]

    except Exception as e:
        print(f'problem in getPartId: {e}')


def updatePurchaser(id: int, username: str, purchaserDeptId: int, purchaserActive: bool,
                    purchaserDateInActive: str, purchaserDateCreated: str) -> None:
    try:
        # soft delete
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()

        if purchaserActive == '1':
            purchaserDateInActive = ''
        else:
            purchaserDateInActive = datetime.date.today()

        parms = (username, purchaserDeptId, purchaserActive, purchaserDateInActive, purchaserDateCreated, id,)
        stmt = 'update Purchaser set username = ?, purchaserDeptId = ?, purchaserActive = ?, purchaserDateInActive = ?, purchaserDateCreated = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updatePurchaser: {e}')


def updateParts(id: int, partNbr: int, partDesc: str, partSupplierId: int, partQuantity: int, partInStock: bool,
                partDateOutOfStock: str, partDateCreated: str):
    try:
        # soft delete
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parms = (partNbr, partDesc, partSupplierId, partQuantity, partInStock, partDateOutOfStock, partDateCreated, id,)
        stmt = 'update Part set partNbr = ?, partDesc = ?, partSupplierId = ?, partQuantity = ?, partInStock = ?, partDateOutOfStock = ?, partDateCreated = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateParts: {e}')


def updateProvincialTaxRates(parms) -> None:

    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'update ProvincialTaxRates set provincialCode = ?, taxRate = ?, label = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateProvincialTaxRates: {e}')


def updateSupplier(id: int, supplierName: str, supplierProv: str, supplierActive: bool, supplierDateCreated: str) -> None:
    try:
        # soft delete
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parms = (supplierName, supplierProv, supplierActive, supplierDateCreated, id,)
        stmt = 'update Supplier set supplierName = ?, supplierProv = ?, supplierActive = ?, supplierDateCreated = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateSupplier: {e}')


def updatePurchaseOrderTable(id: int, purchaseOrderDate: str, purchaseOrderReceivedDate: str, purchaseOrderActive: bool, purchaseOrderDateDeleted: str,
                             purchaseOrderNbr: int, purchaseOrderPurchaserId: int, purchaseOrderPurchaserDeptId: int) -> None:
    try:
        # soft delete
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parms = (purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderDateDeleted, purchaseOrderNbr, purchaseOrderPurchaserId, purchaseOrderPurchaserDeptId, id,)
        stmt = 'update PurchaseOrder set purchaseOrderDate = ?, purchaseOrderReceivedDate = ?, purchaseOrderActive = ?, purchaseOrderDateDeleted = ?, purchaseOrderNbr = ?, purchaseOrderPurchaserId = ?, purchaseOrderPurchaserDeptId = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updatePurchaseOrderTable: {e}')

def updateUser(id: int, givenName: str, surname: str, username: str, password: str, createDate: str, active: str,
               dateInactive: str, securityLevel: int) -> None:
    try:
        # soft delete
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()

        if active == '1':
            dateInactive = ''
        else:
            dateInactive = datetime.date.today()

        parms = (givenName, surname, username, password, createDate, active, dateInactive, securityLevel, id,)
        stmt = 'update User set givenName = ?, surname = ?, username = ?, password = ?, createDate = ?, active = ?, dateInactive = ?, securityLevel = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateUser: {e}')


def updateUserPassword(username: str, hashed_pw: str) -> bool:

    try:
        result: bool = True
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parms = (hashed_pw, username, )
        stmt = 'update User set password = ? where username = ? and active'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return result

    except Exception as e:
        print(f'problem in updateUserPassword: {e}')
        result = False

        return result


def getSupplierName(id: int) -> str:
    try:
        row: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (id,)
        stmt = 'select supplierName from supplier where id = ? and supplierActive'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt, parm)
        row = cur.fetchone()
        # for row in cur:
        #    print(f'row:{row}')
        #print(f'row: {row[0]}')
        cur.close()
        conn.close()
        return row[0]

    except Exception as e:
        print(f'problem in getSupplierName: {e}')


def insertPurchaser(parms) -> None:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        #stmt = 'INSERT INTO Purchaser (givenName, surname, purchaserDeptId, purchaserActive) values (?, ?, ?, ?)'
        stmt = 'INSERT INTO Purchaser (username, purchaserDeptId, purchaserActive) values (?, ?, ?)'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in insertPurchaser: {e}')


def getPurchaserId(username: str) -> int:
    try:
        row: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        #nameList = purchaserName.split
        #givenName = nameList[0]
        #surname = nameList[1]
        #parm = (name,)
        parm = (username,)
        #stmt = 'select Id from user where username = ? and active' #as per kevin Jan 16, 2023
        stmt = 'select Id from purchaser where username = ? and purchaserActive'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt, parm)
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0]

    except Exception as e:
        print(f'problem in getPurchaserId: {e}')


def getPurchaserDeptId(username: str) -> int:
    try:
        row: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        #nameList = purchaserName.split
        #givenName = nameList[0]
        #surname = nameList[1]
        #parm = (givenName, surname,)
        parm = (username,)
        stmt = 'select purchaserDeptId from purchaser where username = ? and purchaserActive'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt, parm)
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0]

    except Exception as e:
        print(f'problem in getPurchaserId: {e}')


def getSupplierId(Name: str) -> int:
    try:
        row: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (Name,)
        stmt = 'select Id from supplier where supplierName = ? and supplierActive'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt, parm)
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0]

    except Exception as e:
        print(f'problem in getSupplierId: {e}')


def getALLSupplierName() -> list:
    try:
        row: list = []
        myList: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        # parm=(Name,)
        stmt = 'select distinct supplierName from supplier where supplierActive is True'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt)
        row = cur.fetchall()
        for r in row:
            myList.append(r[0])
        cur.close()
        conn.close()
        return myList

    except Exception as e:
        print(f'problem in getALLSupplierName: {e}')


def insertSupplier(parms) -> None:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'INSERT INTO supplier (supplierName, supplierProv, supplierActive) values (?, ?, ?)'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in insertSupplier: {e}')


def insertDepartment(parms) -> None:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'INSERT INTO Department (deptName, active) values (?, ?)'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in insertDepartment: {e}')


def deleteDepartment(id: int) -> None:
    try:
        # soft delete
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        dt = datetime.date.today()
        parms = (dt, id,)
        stmt = 'update Department set active = False, dateInActive = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in deleteDepartment: {e}')


def updateDepartment(id: int, dept: str, dateCreated: str, active: bool, dateInActive: str) -> None:
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()

        if active == '1':
            dateInActive = ''
        else:
            dateInActive = datetime.date.today()

        parms = (dept, dateCreated, active, dateInActive, id,)
        stmt = 'update Department set deptName = ?, dateCreated = ?, active = ?, dateInActive = ? where id = ?'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateDepartment: {e}')


def getDepartmentId(deptName: str) -> int:
    try:
        id: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (deptName,)
        stmt = 'select Id from department where deptName = ? and active is True'
        cur.execute(stmt, parm)
        id = cur.fetchone()
        cur.close()
        # conn.commit()
        conn.close()

        return id[0]

    except Exception as e:
        print(f'problem in getDepartmentId: {e}')


def getALLDepartmentNames() -> list:
    try:
        row: list = []
        myList: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'select deptName from Department where active is True'
        cur.execute(stmt)
        row = cur.fetchall()
        for r in row:
            myList.append(r[0])
        cur.close()
        conn.close()

        return myList

    except Exception as e:
        print(f'problem in getALLDepartmentNames: {e}')


def getTableItemById(id: int, tableName: str, colName: str) -> str:
    try:
        row: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (id,)
        stmt = f'select {colName} from {tableName} where id = ?'
        # cur.execute('select unitDesc from unit where id = ?', parm)
        cur.execute(stmt, parm)
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row[0]

    except Exception as e:
        print(f'problem in getTableItemById: {e}')


def insertPart(parms) -> None:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        supplierName = parms[2]
        # supplierId = getSupplierId(supplierName)

        stmt = 'insert into Part(partNbr, partDesc, partSupplierId, partQuantity, partInStock, partDateCreated) values (?, ?, ?, ?, ?, ?)'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in insertPart: {e}')


def getALLPartDesc() -> list:
    try:
        row: list = []
        myList: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'select partDesc from part where partInStock is True'
        cur.execute(stmt)
        row = cur.fetchall()
        for r in row:
            myList.append(r[0])
        cur.close()
        conn.close()

        return myList

    except Exception as e:
        print(f'problem in getALLPartDesc: {e}')


def getALLPartNbr() -> list:
    try:
        row: list = []
        myList: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'select partNbr from part where partInStock is True'
        cur.execute(stmt)
        row = cur.fetchall()
        for r in row:
            myList.append(r[0])
        cur.close()
        conn.close()

        return myList

    except Exception as e:
        print(f'problem in getALLPartDesc: {e}')


def getALLPurchasers() -> list:
    try:
        row: list = []
        myList: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'select username from purchaser where purchaserActive'
        cur.execute(stmt)
        row = cur.fetchall()
        for r in row:
            myList.append(r[0])
        cur.close()
        conn.close()

        return myList

    except Exception as e:
        print(f'problem in getALLPurchaser: {e}')


def getPurchaser(username: str) -> str:
        try:
            row: list = []
            #myList: list = []
            purchaserName: str

            db = getDatabase(constants.DATABASE_NAME)
            conn = getConnection(db)
            cur = conn.cursor()
            parm = (username,)
            stmt = 'select u.givenName, u.surname from user u, purchaser p where p.purchaserActive and u.active and u.username = p.username and u.username = ?'
            cur.execute(stmt, parm)
            row = cur.fetchone()
            if row is None:
                raise Exception(f'check database activeFlag for {username} in table purchaser.')

            #for r in row:
            #myList.append(r[0] + ' ' + r[1])
            purchaserName = row[0] + ' ' + row[1]
            cur.close()
            conn.close()

            #return myList
            return purchaserName

        except Exception as e:
            print(f'problem in getPurchaser: {e}')
            myLogInfo(funcName='getPurchaser', msg='problem in getPurchaser', myData=e, user=None, tb=traceback.format_exc())


def getALLITEMS(tblName: str, colName: str) -> list:
    try:
        row: list = []
        mylist: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        # conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        stmt = f'select {colName} from {tblName}'
        cur.execute(stmt)
        row = cur.fetchall()
        for r in row:
            mylist.append(r[0])

        cur.close()
        conn.close()
        return mylist

    except Exception as e:
        print(f'problem in getALLITEMS: {e}')


def getOrderNbr() -> int:
    try:
        purchaseOrderNbr: int = 0
        stmt: str
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        # conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        stmt = f'select OrderNbr from orderNbrTbl'
        cur.execute(stmt)
        row = cur.fetchone()

        purchaseOrderNbr = row[0]
        if row[0] is None:
            purchaseOrderNbr = 1000

        cur.close()
        conn.close()

        return purchaseOrderNbr

    except Exception as e:
        print(f'problem in getMaxOrderNbr: {e}')


def updateOrderNbr(orderNbr: int) -> None:
    try:
        stmt: str
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()

        parm = (orderNbr,)
        #if int(orderNbr) > 1:
        #
        #else:
        #    stmt = f'insert into OrderNbrTbl values(?)'

        stmt = f'update OrderNbrTbl set orderNbr = ?'
        cur.execute(stmt, parm)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateOrderNbr: {e}')


def insertOrder(parms) -> None:
    #parms = (orderNbr, partNbrId, supplierId, quantity, unitId, cost, totalCost)
    #parms = (orderNbr, partNbr, partDesc, supplierName, quantity, unitPrice, username)
    try:
        #id = {id[0]:0>3} #format left padding w 0 with 3
        stmt: str

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()

        supplierName = parms[2]
        stmt = f'select id from supplier where supplierName = "{supplierName}"'
        cur.execute(stmt)
        supplierId = cur.fetchone()
        supplierId = supplierId[0]

        dt = str(datetime.datetime.today())
        dt = dt[0:10]

        # at this point in time order id has NOT yet been committed to db, therefore get current max id and add one to get next
        # this is used to create the name of the print doc which is stored on the order rec
        maxOrderId = getMaxOrderId() + 1

        #PO = supplierName + '_' + dt + '_' + str(f'{maxOrderNbr:0>3}')
        #PO = supplierName[0] + '_' + dt + '_' + str(f'{maxOrderNbr:0>3}') + '_' + str(maxOrderId)

        #orderNbr = parms[0]
        #stmt = f'select distinct(a.deptName) from department a, purchaser b, purchaseorder c where purchaseOrderNbr = {orderNbr} and c.purchaseOrderPurchaserDeptId = b.id and b.purchaseractive and a.active'
        #stmt = 'select a.deptName from department a, ordertbl b, purchaseorder c where purchaseOrderNbr = b.ordernbr and c.purchaseOrderPurchaserDeptId = a.id and a.active is True'
        orderUsername = parms[5]
        stmt = f'select d.deptName from Department d, Purchaser p where p.username = "{orderUsername}" and p.purchaseractive and d.active and p.purchaserDeptId = d.id'
        cur.execute(stmt)
        deptName = cur.fetchone()
        deptName = deptName[0]

        orderNbr = parms[0]
        PO = supplierName + '_' + dt + '_' + str(f'{orderNbr:0>3}')
        #orderPartNbr = parms[1]
        orderDesc = parms[1]
        orderSupplierId = supplierId
        orderQuantity = parms[3]
        orderPartPrice = parms[4]
        #orderTotalCost = parms[5]
        orderUsername = parms[5]

        #rebuild parms adding deptname, po and username
        #params = (orderNbr, orderSupplierId, deptName, orderPartNbr, orderDesc, orderQuantity, orderPartPrice, PO, orderUsername, 1)
        #params = (orderNbr, orderSupplierId, deptName, orderPartNbr, orderDesc, orderQuantity, orderPartPrice, PO, orderUsername,)
        params = (orderNbr, orderSupplierId, deptName, orderDesc, orderQuantity, orderPartPrice, PO, orderUsername,)

        #ACTIVE INDICATOR NOW SET AS DEFAULT IN DB
        #stmt = 'INSERT INTO OrderTbl(orderNbr, orderSupplierId, deptName, orderPartNbr, orderPartDesc, orderQuantity, orderPartPrice, PO, orderUsername, orderActive ) values (?,?,?,?,?,?,?,?,?,?)'
        stmt = 'INSERT INTO OrderTbl(orderNbr, orderSupplierId, deptName, orderPartDesc, orderQuantity, orderPartPrice, PO, orderUsername) values (?,?,?,?,?,?,?,?)'
        #stmt = 'INSERT INTO OrderTbl(orderNbr, orderSupplierId, deptName, orderPartNbr, orderPartDesc, orderQuantity, orderPartPrice, PO, orderUsername) values (?,?,?,?,?,?,?,?,?)'
        cur.execute(stmt, params)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in insertOrder: {e}')


def insertPurchaseOrder(purchaseOrderNbr: int, purchaserId: int, purchaserDept: int) -> None:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        #orderDt = datetime.date.today() - now set as default in db
        receivedDt = ''
        #Active = True - now set as default in db
        #parms = (orderDt, receivedDt, Active, purchaseOrderNbr, purchaserId, purchaserDept)
        parms = (receivedDt, purchaseOrderNbr, purchaserId, purchaserDept,)
        #stmt = 'INSERT INTO PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderNbr, purchaseOrderpurchaserId, purchaseOrderPurchaserDeptId) values (?, ?, ?, ?, ?, ?)'
        stmt = 'INSERT INTO PurchaseOrder(PurchaseOrderReceivedDate, purchaseOrderNbr, purchaseOrderpurchaserId, purchaseOrderPurchaserDeptId) values (?, ?, ?, ?)'
        cur.execute(stmt, parms)
        cur.close()
        conn.commit()
        conn.close()

        return

    except Exception as e:
        print(f'problem in insertPurchaseOrder: {e}')


def getALLPurchaseOrders(securityLevel: int) -> list:
    try:
        row: list = []

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        # conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # added July 20, 2023, seems to speed things up (I just eye-balled this)
        # remains until connection is closed
        cur.execute('PRAGMA cache_size = -1048576')

        #if GOD_LEVEL then show ALL purchase orders, active and non-active
        if securityLevel == constants.GOD_LEVEL:
            stmt = f'select p.id, o.id, purchaser.username, o.deptName, orderNbr, p.purchaseOrderDate, s.supplierName, o.orderPartDesc, o.OrderQuantity,o.OrderPartPrice, o.orderReceivedDate, o.OrderReceivedBy, o.orderReturnDate, o.orderReturnQuantity, o.PO, o.orderUsername, o.OrderActive, {securityLevel} from purchaseOrder p, OrderTbl o, supplier s, Purchaser, Department where p.purchaseOrderNbr = o.orderNbr AND o.OrderSupplierId = s.id and Purchaser.id = p.purchaseOrderPurchaserId and purchaserDeptid = department.id'
            #stmt = f'select p.id, o.id, purchaser.purchaserName, o.deptName, orderNbr, p.purchaseOrderDate, s.supplierName, o.orderPartNbr, o.orderPartDesc, o.OrderQuantity,o.OrderPartPrice, o.orderReceivedDate, o.OrderReceivedBy, o.orderReturnDate, o.orderReturnQuantity, o.PO, o.orderUsername, o.OrderActive, {securityLevel} from purchaseOrder p, OrderTbl o, supplier s, Purchaser, Department where p.purchaseOrderNbr = o.orderNbr AND o.OrderSupplierId = s.id and Purchaser.id = p.purchaseOrderPurchaserId and purchaserDeptid = department.id'
        else:
            stmt = f'select p.id, o.id, purchaser.username, o.deptName, orderNbr, p.purchaseOrderDate, s.supplierName, o.orderPartDesc, o.OrderQuantity,o.OrderPartPrice, o.orderReceivedDate, o.OrderReceivedBy, o.orderReturnDate, o.orderReturnQuantity, o.PO, o.orderUsername, o.OrderActive, {securityLevel} from purchaseOrder p, OrderTbl o, supplier s, Purchaser, Department where p.purchaseOrderNbr = o.orderNbr AND o.OrderSupplierId = s.id and Purchaser.id = p.purchaseOrderPurchaserId and purchaserDeptid = department.id  and o.OrderActive'
            #stmt = f'select p.id, o.id, purchaser.purchaserName, o.deptName, orderNbr, p.purchaseOrderDate, s.supplierName, o.orderPartNbr, o.orderPartDesc, o.OrderQuantity,o.OrderPartPrice, o.orderReceivedDate, o.OrderReceivedBy, o.orderReturnDate, o.orderReturnQuantity, o.PO, o.orderUsername, o.OrderActive, {securityLevel} from purchaseOrder p, OrderTbl o, supplier s, Purchaser, Department where p.purchaseOrderNbr = o.orderNbr AND o.OrderSupplierId = s.id and Purchaser.id = p.purchaseOrderPurchaserId and purchaserDeptid = department.id  and o.OrderActive'

        cur.execute(stmt)
        row = cur.fetchall()
        cur.close()
        conn.close()

        return row

    except Exception as e:
        print(f'problem in getALLPurchaseOrders: {e}')


def deletePurchaseOrder(orderId: int):
    # There is ONE purchaseOrder id used to track orders.
    # there can be MANY orders per purchaseOrder
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm1 = (orderId,)
        stmt1 = 'select o.OrderNbr from orderTbl o where o.id = ?'
        cur.execute(stmt1, parm1)
        orderNbr = cur.fetchone()
        orderNbr = orderNbr[0]

        parm2 = (orderNbr,)
        stmt2 = 'select count(*) from orderTbl o where o.orderNbr = ?'
        cur.execute(stmt2, parm2)
        nbrOfOrders = cur.fetchone()
        nbrOfOrders = nbrOfOrders[0]

        # if NbrOfOrders = 1 then delete from order table and purchaseOrder table
        # if NbrOfOrders > 1 then delete only specific purchase form purchaseorder, other purchases remain in order

        stmt3 = 'delete from orderTbl where orderTbl.id = ?'
        cur.execute(stmt3, parm1)
        cur.fetchone()

        if nbrOfOrders == 1:
            stmt4 = 'delete from purchaseOrder where purchaseOrder.purchaserOrderNbr = ?'
            cur.execute(stmt3, parm2)
            cur.fetchone()

        conn.commit()
        cur.close()
        conn.close()

        return

    except Exception as e:
        print(f'problem in deletePurchaseOrder: {e}')


def updateOrderReceivedDate(id: int, dt_order_received: str, dt_order_returned: str) -> None:
    # There is ONE purchaseOrder id used to track orders.
    # there can be MANY orders per purchaseOrder
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        # if NbrOfOrders = 1 then soft delete from order table and purchaseOrder table
        # if NbrOfOrders > 1 then soft delete only specific purchase form purchaseorder, other purchases remain in order
        parm1 = (id,)
        if not dt_order_received == '':    #received date is not empty
            stmt1 = f"update orderTbl set orderreceivedDate = '{dt_order_received}', orderReturndate = '{dt_order_returned}', orderActive = False where id = ?"

        else:
            # currentDate = datetime.date.today()
            stmt1 = f"update orderTbl set orderReturndate = '{dt_order_returned}' where id = ?"

        cur.execute(stmt1, parm1)
        conn.commit()

        stmt2 = 'select o.OrderNbr from orderTbl o where o.id = ?'
        cur.execute(stmt2, parm1)
        orderNbr = cur.fetchone()
        orderNbr = orderNbr[0]

        parm3 = (orderNbr,)
        stmt3 = 'select count(*) from orderTbl o where o.orderNbr = ? and orderActive'
        cur.execute(stmt3, parm3)
        nbrOfOrders = cur.fetchone()
        nbrOfOrders = nbrOfOrders[0]

        stmt4 = 'select count(*) from purchaseOrder where purchaseOrderNbr = ? and purchaseOrderActive'
        cur.execute(stmt4, parm3)
        nbrOfPurchaseOrders = cur.fetchone()
        nbrOfPurchaseOrders = nbrOfPurchaseOrders[0]

        # we could be in this function for 2 reasons, either for the received date or returned date.
        # when ALL orders are received set the purchase order active to false and the purchase order date is set to the received date.

        if nbrOfOrders == 0 and nbrOfPurchaseOrders > 0:
            stmt5 = f"update purchaseOrder set purchaseOrderReceivedDate = '{dt_order_received}', purchaseOrderActive = False, purchaseOrderDateDeleted = '{datetime.date.today()}' where purchaseOrderNbr = ?"
            cur.execute(stmt5, parm3)

        conn.commit()
        cur.close()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateOrderReceivedDate: {e}')


def updateOrderQuantity(id: int, quantity: int, colName: str) -> None:
    # There is ONE purchaseOrder id used to track orders.
    # there can be MANY orders per purchaseOrder
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (quantity, id,)
        stmt = f"update orderTbl set {colName} = ? where id = ?"
        cur.execute(stmt, parm)
        conn.commit()
        cur.close()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateOrderQuantity: {e}')


def updateOrderReceivedBy(parms) -> None:
    # There is ONE purchaseOrder id used to track orders.
    # there can be MANY orders per purchaseOrder
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = "update orderTbl set orderReceivedBy = ? where id = ?"
        cur.execute(stmt, parms)
        conn.commit()
        cur.close()
        conn.close()

        return

    except Exception as e:
        print(f'problem in updateOrderReceivedBy: {e}')


def updateActiveFlg(parms) -> None:
    # set active flag in purchaseOrder table - used to track orders.
    # there can be MANY orders per purchaseOrder
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        # update active indicator - can be 0 (inactive) or 1 (active)
        stmt = "update orderTbl set orderActive = ? where id = ?"
        cur.execute(stmt, parms)
        conn.commit()

        # retrieve order number / po nbr
        orderId = parms[1]
        parm1 = (orderId,)
        stmt1 = 'select o.OrderNbr from orderTbl o where o.id = ?'
        cur.execute(stmt1, parm1)
        orderNbr = cur.fetchone()
        orderNbr = orderNbr[0]

        # update purchaseOrder table
        parm2 = (orderNbr,)
        stmt2 = 'select count(*) from orderTbl o where o.orderNbr = ? and o.orderActive = 1'
        cur.execute(stmt2, parm2)
        nbrOfOrders = cur.fetchone()
        nbrOfOrders = nbrOfOrders[0]

        # if NbrOfOrders = 0 then set purchaseOrderActive = 0 (inactive) in purchaseOrder table
        # else set purchaseOrderActive = 1 (active) in purchaseOrder table
        if nbrOfOrders == 0:
            stmt3 = 'update purchaseOrder set purchaseOrderActive = 0 where purchaseOrderNbr = ?'
            cur.execute(stmt3, parm2)
        else:
            stmt4 = 'update purchaseOrder set purchaseOrderActive = 1 where purchaseOrderNbr = ?'
            cur.execute(stmt4, parm2)

        conn.commit()

    except Exception as e:
        print(f'problem in updateActiveFlg: {e}')

    finally:
        cur.close()
        conn.close()

        return

def isPOArchived(PONbr: int) -> bool:
    POArchived = False
    try:
        '''
        A purchase order is completely archived when the purchase order number is found in the ARCHIVE_PurchaseOrder 
        table. Alternatively, a purchase order with multiple orders may have some orders archived, in this case some 
        records may be found in the ARCHIVE_OrderTbl but the PONbr will not be found in the ARCHIVE_PurchaseOrder table.
        '''
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (PONbr, )
        stmt = 'select count(*) from ARCHIVE_OrderTbl where orderNbr = ?'
        cur.execute(stmt, parm)
        result = cur.fetchone()
        result = result[0]

        if result > 0:
            POArchived = True

    except Exception as e:
        print(f'problem in isPOArchived: {e}')

    finally:
        cur.close()
        conn.close()

        return POArchived

def restoreOrderTbl(PONbr: int) -> bool:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (PONbr, )
        rtnCode = True
        stmt = 'INSERT INTO OrderTbl (OrderNbr, OrderSupplierId, deptName, OrderPartDesc, OrderQuantity, OrderPartPrice, OrderReceivedDate, OrderReceivedBy, \
				OrderReturnDate, OrderReturnQuantity, PO, OrderUsername, OrderActive) \
				SELECT OrderNbr, OrderSupplierId, deptName, OrderPartDesc, OrderQuantity, OrderPartPrice, OrderReceivedDate, OrderReceivedBy, \
				OrderReturnDate, OrderReturnQuantity, PO, OrderUsername, 1 FROM ARCHIVE_OrderTbl WHERE OrderActive = 0 and orderNbr = ?'
        cur.execute(stmt, parm)
        conn.commit()

    except Exception as e:
        print(f'problem in utilities.restorePurchaseOrder: {e}')
        rtnCode = False

    finally:
        cur.close()
        conn.close()

    return rtnCode

def restorePurchaseOrderTbl(PONbr) -> bool:
    try:
        '''
        check to see if purchase order has been ARCHIVED, if yes then copy from ARCHIVE otherwise
        assume purchase order has not been archived and record is present in purchase order table.
        '''
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (PONbr,)
        stmt = 'select count(*) from ARCHIVE_PurchaseOrder where purchaseOrderNbr = ? and purchaseOrderActive = 0'
        cur.execute(stmt, parm)
        result = cur.fetchone()
        result = result[0]
        rtnCode = True
        if result > 0:  # ARCHIVED
            stmt = 'INSERT INTO PurchaseOrder (purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, \
                    purchaseOrderDateDeleted, purchaseOrderNbr, purchaseOrderPurchaserId, purchaseOrderPurchaserDeptId) \
                    SELECT purchaseOrderDate, purchaseOrderReceivedDate, 1, purchaseOrderDateDeleted, \
                    purchaseOrderNbr, purchaseOrderPurchaserId, purchaseOrderPurchaserDeptId \
                    FROM ARCHIVE_PurchaseOrder WHERE purchaseOrderActive = 0 and purchaseOrderNbr = ?'
            cur.execute(stmt, parm)
            conn.commit()

    except Exception as e:
        print(f'problem in utilities.restorePurchaseOrder: {e}')
        rtnCode = False

    finally:
        cur.close()
        conn.close()

    return rtnCode


def deleteARCHIVEDOrder(PONbr):
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (PONbr,)
        stmt = 'delete from ARCHIVE_OrderTbl where OrderNbr = ? and orderActive = 0'
        cur.execute(stmt, parm)
        conn.commit()

    except Exception as e:
        print(f'problem in utilities.deleteARCHIVEDOrder: {e}')

    finally:
        cur.close()
        conn.close()

    return


def deleteARCHIVEDPurchaseOrder(PONbr):
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (PONbr,)
        stmt = 'delete from ARCHIVE_PurchaseOrder where PurchaseOrderNbr = ? and purchaseOrderActive = 0'
        cur.execute(stmt, parm)
        conn.commit()

    except Exception as e:
        print(f'problem in utilities.deleteARCHIVEDPurchaseOrder: {e}')

    finally:
        cur.close()
        conn.close()

    return


def registerUser(username: str, hashed_pw: int, givenName: str, surname: str) -> None:
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        #createdate = datetime.date.today() - now set as default in db
        #active = True - now set as default in db
        securityLevel = 0
        parm = (username, hashed_pw, givenName, surname, securityLevel, )
        #parm = (username, hashed_pw, createdate, active, securityLevel)
        stmt = "insert into user (username, password, givenName, surname, securityLevel) values(?, ?, ?, ?, ?)"
        cur.execute(stmt, parm)
        conn.commit()
        cur.close()

        return

    except Exception as e:
        print(f'problem in registerUser: {e}')


def getPassword(username: str) -> str:
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (username,)
        stmt = "select password from user where username = ? and active"
        cur.execute(stmt, parm)
        pw = cur.fetchone()

        cur.close()

        return pw[0]

    except Exception as e:
        print(f'problem in getPassword: {e}')


def getUserSecurityLevel(username: str) -> int:
    try:

        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (username,)
        stmt = "select securityLevel from user where username = ? and active is True"
        cur.execute(stmt, parm)
        level = cur.fetchone()
        # conn.commit()
        cur.close()

        return level[0]

    except Exception as e:
        print(f'problem in getUserSecurityLevel: {e}')


def getUser(username: str) -> bool:
    try:
        exists: bool = False
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (username,)
        #stmt = "select username from user where username = ? and active is True"
        stmt = "select * from user where username = ? and active"
        cur.execute(stmt, parm)
        result = cur.fetchone()
        # conn.commit()
        cur.close()
        #if result is not None:
        #    exists = True

        #return exists
        return result

    except Exception as e:
        print(f'problem in getUser: {e}')


def getTable(tableName: str) -> list:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (tableName,)
        stmt = f"select * from {tableName}"
        cur.execute(stmt)
        rows = cur.fetchall()
        rows = list(rows)
        # conn.commit()
        cur.close()

        return rows

    except Exception as e:
        print(f'problem in getTable: {e}')


def createPrintDoc(orderList: list) -> None:
    # https://nagasudhir.blogspot.com/2021/10/docxtpl-python-library-for-creating.html

    try:
        myList: list = []
        previousSupplierId = orderList[0][2]
        docName = orderList[0][11]
        orderTotalCost: float = 0.0

        for order in orderList:

            supplierId = order[2]

            if previousSupplierId != supplierId:
                createOrderDoc('purchaseOrderTemplate.docx', docName, myList, order, previousSupplierId, orderTotalCost)
                myList = []
                orderTotalCost = 0.0
                myList, orderTotalCost = buildDoc(order, myList, orderTotalCost)
                previousSupplierId = supplierId
                docName = order[11]
            else:
                myList, orderTotalCost = buildDoc(order, myList, orderTotalCost)

        createOrderDoc('purchaseOrderTemplate.docx', docName, myList, order, previousSupplierId, orderTotalCost)

        return

    except Exception as e:
        print(f'problem in createPrintDoc: {e}')


def buildDoc(order, myList: list, orderTotalCost: float):
    try:
        #partDesc = getTableItemById(order[4], 'Part', 'partDesc')
        #partNbr = order[4]
        partDesc = order[4]
        orderQuantity = order[5]
        orderPartPrice = order[6] if not order[6] == '' else 0.0
        orderCost = orderQuantity * orderPartPrice
        orderTotalCost += orderCost
        myList.append({'orderQuantity': orderQuantity, 'orderPartPrice': orderPartPrice, 'partDesc': partDesc, 'orderCost': orderCost})
        #myList.append({'orderQuantity': orderQuantity, 'orderPartPrice': orderPartPrice, 'partDesc': partDesc, 'partNbr': partNbr, 'orderCost': orderCost})

        return myList, orderTotalCost

    except Exception as e:
        print(f'problem in buildDoc: {e}')


def createOrderDoc(templateName: str, docName: str, myList: list, order, supplierId: int, orderTotalCost: float) -> None:
    try:
        #docPath = Path(__file__).parent / templateName
        docPathTemplate = constants.TEMPLATE_DIRECTORY + templateName
        doc = DocxTemplate(docPathTemplate)

        # these are common to all rows in the order
        #purchaseOrderId = order[1]
        #purchaseOrderDate = getTableItemById(purchaseOrderId, 'PurchaseOrder', 'purchaseOrderDate')
        purchaseOrderDate = getPurchaseOrderDate(order[1])
        PONbr = order[1]

        supplierName = getSupplierName(supplierId)
        #supplierAddr = getTableItemById(supplierId, 'Supplier', 'supplierAddr')
        supplierProv = getTableItemById(supplierId, 'Supplier', 'supplierProv')
        #supplierTel = getTableItemById(supplierId, 'Supplier', 'supplierTel')
        #supplierEmail = getTableItemById(supplierId, 'Supplier', 'supplierEmail')
        receivedBy = order[9]

        label1, amt1, amt2, amt3 = calcSalesTax(supplierProv, orderTotalCost)


        # https://nagasudhir.blogspot.com/2021/10/docxtpl-python-library-for-creating.html

        context = {'supplierName': supplierName,
                   #'supplierAddr': supplierAddr,
                   #'supplierTel': supplierTel,
                   #'supplierEmail': supplierEmail,
                   'receivedBy': receivedBy,
                   'purchaseOrderDate': purchaseOrderDate,
                   'PONbr': PONbr,
                   'items': myList,
                   'orderTotalCost': orderTotalCost,
                   'label1': label1,
                   'amt1': amt1,
                   'amt2': amt2,
                   'amt3': amt3
                   }

        doc.render(context)

        myDir = r'c:/users/wayne/APP/app/static/purchaseOrders'

        myDoc = constants.DOC_DIRECTORY + docName + '.docx'

        #doc.save(Path(__file__).parent / myDoc)
        doc.save(myDoc)


        #write protect document, IROTH = can be read by others
        #os.chmod(myDoc, stat.S_IROTH)

        return

    except Exception as e:
        print(f'problem in createOrderDoc: {e}')


def calcSalesTax(supplierProv, orderTotalCost):
    try:
        row: list = []
        row = getProvincialTaxRate(supplierProv)
        amt1 = row[2]
        amt2 = (amt1 * .01) * orderTotalCost  # sales tax
        label1 = row[3]
        '''
        match supplierProv:
            case 'QC':
                label1 = 'Sales tax rate (PST+QST) %'
                amt1 = 14.975
                amt2 = .14975 * orderTotalCost  # sales tax
            case 'ON':
                label1 = 'Sales tax rate (HST) %'
                amt1 = 13
                amt2 = .13 * orderTotalCost  # sales tax
            case 'AB':
                label1 = 'Sales tax rate (GST) %'
                amt1 = 5
                amt2 = .05 * orderTotalCost  # sales tax
            case 'BC':
                label1 = 'Sales tax rate (PST+GST) %'
                amt1 = 12
                amt2 = .12 * orderTotalCost  # sales tax
            case 'MB':
                label1 = 'Sales tax rate (PST+GST) %'
                amt1 = 12
                amt2 = .12 * orderTotalCost  # sales tax
            case 'NB':
                label1 = 'Sales tax rate (HST) %'
                amt1 = 15
                amt2 = .15 * orderTotalCost  # sales tax
            case 'NL':
                label1 = 'Sales tax rate (HST) %'
                amt1 = 15
                amt2 = .15 * orderTotalCost  # sales tax
            case 'NT':
                label1 = 'Sales tax rate (GST) %'
                amt1 = 5
                amt2 = .05 * orderTotalCost  # sales tax
            case 'NS':
                label1 = 'Sales tax rate (HST) %'
                amt1 = 15
                amt2 = .15 * orderTotalCost  # sales tax
            case 'NU':
                label1 = 'Sales tax rate (GST) %'
                amt1 = 5
                amt2 = .05 * orderTotalCost  # sales tax
            case 'PE':
                label1 = 'Sales tax rate (HST) %'
                amt1 = 15
                amt2 = .15 * orderTotalCost  # sales tax
            case 'SK':
                label1 = 'Sales tax rate (PST+GST) %'
                amt1 = 11
                amt2 = .11 * orderTotalCost  # sales tax
            case 'YK':
                label1 = 'Sales tax rate (GST) %'
                amt1 = 5
                amt2 = .05 * orderTotalCost  # sales tax
            case 'OTHER':
                label1 = 'Sales tax rate UNKNOWN'
                amt1 = 0
                amt2 = 0
        '''

        amt2 = round(amt2, 2) #round to 2 decimals
        amt3 = amt2 + orderTotalCost

    except Exception as e:
        print(f'problem in createSalesTax: {e}')

    return label1, amt1, amt2, amt3


def downloadDocToLocalHost(docName: str) -> None:
    try:
        #import requests
        username = 'wayneraid'
        api_token = '26351fda9e41892c159e6ddfb5b4bda44e2a88f1'
        host = 'www.pythonanywhere.com'
        api_base = "https://{host}/api/v0/user/{username}/".format(
            host=host,
            username=username,
        )

        resp = requests.get(
            urljoin(api_base, "files/path/home/{username}/surgenor/app/{docName}".format(username=username, docName=docName)),
            headers={"Authorization": "Token {api_token}".format(api_token=api_token)})


        #response = requests.get(
        #      'https://{host}/api/v0/user/{username}/files/{path}'.format(
        #          host=host, username=username
        #      ),
        #      headers={'Authorization': 'Token {token}'.format(token=token)}
        #  )


        if resp.status_code == 200:
            #print('saving file:')
            #print(resp.content)
            with open(docName, mode='wb') as localfile:
                localfile.write(resp.content)
        else:
            print('Got unexpected status code {}: {!r}'.format(resp.status_code, resp.content))

    except Exception as e:
        print(f'problem in downloadDocToLocalHost: {e}')

    return


def getPurchaseOrderDate(purchaseOrderNbr: int) -> str:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (purchaseOrderNbr,)
        stmt = "select purchaseOrderDate from PurchaseOrder where purchaseOrderNbr = ? and purchaseOrderActive = True"
        cur.execute(stmt, parm)
        purchaseOrderDate = cur.fetchone()
        # conn.commit()
        cur.close()

        return purchaseOrderDate[0]

    except Exception as e:
        print(f'problem in getPurchaseOrderDate: {e}')


def getPurchaseOrderById(orderId: int) -> list:
    try:
        myList = []
        row = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (orderId,)
        stmt = "select * from PurchaseOrder where id = ? and purchaseOrderActive = True"
        cur.execute(stmt, parm)
        row = cur.fetchone()
        # conn.commit()
        cur.close()
        for i in row:
            myList.append(i)

        return myList

    except Exception as e:
        print(f'problem in getPurchaseOrderById: {e}')


def getOrderByOrderNbr(orderNbr: int, securityLevel: int) -> list:
    '''
    if use has security level 5, GOD LEVEL, then retrieve both active and non-active orders.
    if not then retrieve only active records
    '''

    myList = []
    rows = []
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (orderNbr,)
        if securityLevel == constants.GOD_LEVEL:
            stmt = "select * from OrderTbl where orderNbr = ? order by orderSupplierId asc"
        else:
            stmt = "select * from OrderTbl where orderNbr = ? and orderActive = 1 order by orderSupplierId asc"
        cur.execute(stmt, parm)
        rows = cur.fetchall()

        for row in rows:
            myList.append(row)

    except Exception as e:
        print(f'problem in getOrderByOrderNbr: {e}')

    finally:
        conn.commit()
        cur.close()

        return myList  # myList[0][3]


def getMaxOrderId():
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = "select max(id) from OrderTbl"
        cur.execute(stmt)
        row = cur.fetchone()
        # conn.commit()
        cur.close()
        maxOrderId = 0
        if row[0] != None:
            maxOrderId = row[0]

        return maxOrderId

    except Exception as e:
        print(f'problem in getMaxOrderId: {e}')


def getCount(tableName: str) -> int:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = f"select count(*) from {tableName}"
        cur.execute(stmt)
        row = cur.fetchone()
        # conn.commit()
        cur.close()

        count = 0
        if row[0] != None:
            count = row[0]

        return count

    except Exception as e:
        print(f'problem in getCount: {e}')


def getOrderByCount() -> list:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = 'select orderpartdesc, count(orderpartdesc) count from ordertbl group by OrderPartDesc order by count desc'
        cur.execute(stmt)
        rows = cur.fetchall()
        # conn.commit()
        cur.close()

        myList = []
        for row in rows:
            ar = list(row)
            myList.append(ar)

        return myList

    except Exception as e:
        print(f'problem in getOrderbyCount: {e}')


def getOrderByMonth() -> list:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        # stmt = 'SELECT STRFTIME("%m", purchaseorderdate) AS month, COUNT(id) AS count FROM purchaseorder GROUP BY STRFTIME("%m", purchaseorderdate)'
        stmt1 = "SELECT CASE WHEN sTRFTIME('%m', purchaseorderdate) = '01' THEN 'JAN'"
        stmt2 = " WHEN sTRFTIME('%m', purchaseorderdate) = '02' THEN 'FEB'"
        stmt3 = " WHEN sTRFTIME('%m', purchaseorderdate) = '03' THEN 'MAR'"
        stmt4 = " WHEN sTRFTIME('%m', purchaseorderdate) = '04' THEN 'APR'"
        stmt5 = " WHEN sTRFTIME('%m', purchaseorderdate) = '05' THEN 'MAY'"
        stmt6 = " WHEN sTRFTIME('%m', purchaseorderdate) = '06' THEN 'JUN'"
        stmt7 = " WHEN sTRFTIME('%m', purchaseorderdate) = '07' THEN 'JUL'"
        stmt8 =	" WHEN sTRFTIME('%m', purchaseorderdate) = '08' THEN 'AUG'"
        stmt9 =	" WHEN sTRFTIME('%m', purchaseorderdate) = '09' THEN 'SEP'"
        stmt10 = " WHEN sTRFTIME('%m', purchaseorderdate) = '10' THEN 'OCT'"
        stmt11 = " WHEN sTRFTIME('%m', purchaseorderdate) = '11' THEN 'NOV'"
        stmt12 = " WHEN sTRFTIME('%m', purchaseorderdate) = '12' THEN 'DEC'"
        stmt13 = " END, COUNT(id) AS count FROM purchaseorder where substr(purchaseOrderDate, 1, 4) IN (select strftime('%Y', purchaseorderdate) from purchaseorder) GROUP BY STRFTIME('%m', purchaseorderdate);"
        stmt14 = stmt1 + stmt2 + stmt3 + stmt4 + stmt5 + stmt6 + stmt7 + stmt8 + stmt9 + stmt10 + stmt11 + stmt12 + stmt13
        cur.execute(stmt14)
        rows = cur.fetchall()
        # conn.commit()
        cur.close()

        myList = []
        for row in rows:
            ar = list(row)
            myList.append(ar)

        return myList

    except Exception as e:
        print(f'problem in getOrderbyMonth: {e}')


def getUserLanguage(username: str) -> str:
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parm = (username,)
        stmt = "select language from user where username = ? and active is True"
        cur.execute(stmt, parm)
        lang = cur.fetchone()

    except Exception as e:
        print(f'problem in getUserLanguage: {e}')

    finally:
        cur.close()
        conn.close()
        return lang[0]

def createSessionObjects(currentLang: str, session) -> str:
    try:

        if currentLang == 'en-us':
            #----- base.html, adminBase.html, login.html, register.html translations -----
            session['home'] = 'Accueil'
            session['loggedInAs'] = 'Actuellement connecté comme:'
            session['purchaseOrder'] = 'Commande d''achat'
            session['admin'] = 'admin'
            session['create'] = 'créer'
            session['manage'] = 'débrouiller'
            session['purchaser'] = 'acheteur'
            session['department'] = 'département'
            session['supplier'] = 'fournisseur'
            session['user'] = 'utilisateur'
            session['userNm'] = 'Nom d’utilisateur'
            session['pw'] = 'Mot de passe'
            session['invalidpw'] = 'Mot de passe non valide saisi!'
            session['statistics'] = 'statistique'
            session['lang'] = 'fr-ca'
            session['login'] = 'connectez-vous'
            session['register'] = 'registre'
            session['notRegistered'] = 'Vous n’êtes pas enregistré en tant qu’utilisateur, veuillez vous inscrire'
            session['logout'] = 'déconnexion'
            session['alreadyAccount'] = 'Vous avez déjà un compte?'
            session['alreadyLoggedIn'] = 'Vous êtes déjà connecté!'
            session['alreadyRegistered'] = 'Le nom d’utilisateur est déjà enregistré'
            session['registered'] = 'Vous avez été inscrit, veuillez vous connecter'
            session['pleaseLogin'] = 'Veuillez vous connecter!'
            session['securityLevel5'] = 'Niveau de sécurité de 5 requis'
            currentLang = 'fr-ca'
            #----- addSupplier.html -----
            session['addSupplier'] = 'Ajouter un fournisseur'
            session['supplierName'] = 'Nom du fournisseur:'
            session['supplierAddress'] = 'Adresse du fournisseur:'
            session['supplierProv'] = 'Province des fournisseur:'
            session['contactName'] = 'Nom de la personne - ressource:'
            session['telephoneNumber'] = 'Numéro de téléphone:'
            session['email'] = 'Adresse courriel:'
            #----- addDepartment.html -----
            session['addDepartment'] = 'Ajouter un département'
            session['departmentName'] = 'Nom du département:'
            session['departmentActive'] = 'Département actif:'
            session['yes'] = 'Oui'
            session['no'] = 'Non'
            # ----- addOrder.html -----
            session['placeOrder'] = 'Passez votre commande!'
            session['purchaseOrderNumber'] = 'Numéro de bon de commande:'
            session['orderPurchaser'] = 'Veuillez sélectionner un acheteur'
            session['quantity'] = 'quantité'
            session['partNumber'] = 'Numéro de pièce'
            session['description'] = 'Description'
            session['unitPrice'] = 'Prix unitaire'
            session['selectSupplier'] = 'Sélectionner un fournisseur'
            session['addRow'] = 'Ajouter une ligne'
            # ----- addPurchaser.html -----
            session['addPurchaser'] = 'Ajouter un acheteur'
            session['purchaserName'] = 'Nom de l’acheteur'
            session['purchaserDept'] = 'Service des acheteurs'
            session['selectPurchaser'] = 'Veuillez sélectionner un service d''acheteur'
            session['purchaserActive'] = 'Acheteur actif'
            # ----- viewDoc.html -----
            session['viewPrint'] = 'Afficher/Imprimer le bon de commande'
            session['noPrint'] = "Aucune commande d'acheteur à imprimer"
            # ----- purchase order table -----
            session['purchaseOrderDate'] = "Date de commande d'achat"
            session['purchaseOrderTable'] = "Tableau de commande d'achat"
            session['invalidPurchaser'] = "L'utilisateur n'est pas un acheteur"
        else:
            #----- base.html, adminBase.html, login.html, register.html translations -----
            session['home'] = 'Home'
            session['loggedInAs'] = 'Currently logged in as:'
            session['purchaseOrder'] = 'Purchase Order'
            session['admin'] = 'Admin'
            session['create'] = 'Create'
            session['manage'] = 'Manage'
            session['purchaser'] = 'Purchaser'
            session['department'] = 'Department'
            session['supplier'] = 'Supplier'
            session['user'] = 'User'
            session['userNm'] = 'Username'
            session['pw'] = 'Password'
            session['invalidpw'] = 'Invalid password entered!'
            session['statistics'] = 'Statistics'
            session['lang'] = 'en-us'
            session['login'] = 'Login'
            session['register'] = 'Register'
            session['notRegistered'] = 'You are not registered as a user, please register'
            session['logout'] = 'Logout'
            session['alreadyAccount'] = 'Already Have An Account?'
            session['alreadyLoggedIn'] = 'You are already logged in!'
            session['alreadyRegistered'] = 'Username is already registered'
            session['registered'] = 'You have been registered, please login'
            session['pleaseLogin'] = 'Please Login!'
            session['securityLevel5'] = 'Security Level 5 required'
            currentLang = 'en-us'
            #----- addSupplier.html -----
            session['addSupplier'] = 'Add Supplier'
            session['supplierName'] = 'Supplier Name:'
            session['supplierAddress'] = 'Supplier Address:'
            session['supplierProv'] = 'Supplier Province:'
            session['contactName'] = 'Contact Name:'
            session['telephoneNumber'] = 'Telephone Number:'
            session['email'] = 'Email address:'
            #----- addDepartment.html -----
            session['addDepartment'] = 'Add Department'
            session['departmentName'] = 'Department Name:'
            session['departmentActive'] = 'Department active:'
            session['yes'] = 'Yes'
            session['no'] = 'No'
            #----- addOrder.html -----
            session['placeOrder'] = 'Place your Order!'
            session['purchaseOrderNumber'] = 'Purchase Order Number:'
            session['orderPurchaser'] = 'Please select a purchaser'
            session['quantity'] = 'Quantity'
            session['partNumber'] = 'Part Number'
            session['description'] = 'Description'
            session['unitPrice'] = 'Unit Price'
            session['selectSupplier'] = 'select a supplier'
            session['addRow'] = 'Add Row'
            # ----- addPurchaser.html -----
            session['addPurchaser'] = 'Add Purchaser'
            session['purchaserName'] = 'Purchaser Name'
            session['purchaserDept'] = 'Purchaser Department'
            session['selectPurchaser'] = 'Please select a purchaser department'
            session['purchaserActive'] = 'Purchaser active'
            # ----- viewDoc.html -----
            session['viewPrint'] = 'View/Print Purchase Order'
            session['noPrint'] = 'No Purchaser Orders to Print'
            # ----- purchase order table -----
            session['purchaseOrderDate'] = 'Purchase Order Date'
            session['purchaseOrderTable'] = 'Purchase Order Table'
            session['invalidPurchaser'] = 'User is not a purchaser'

        return currentLang

    except Exception as e:
        print(f'problem in createSessionObjects: {e}')


def getActive(tableName: str, colName: str, btrue: bool) -> list:
    resultset: list = []
    try:
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        parms = (btrue, )
        stmt = f"select * from {tableName} where {colName} is ?"
        cur.execute(stmt, parms)
        resultset = cur.fetchall()

    except Exception as e:
        print(f'problem in getActive: {e}')

    finally:
        cur.close()
        conn.close()

        return resultset

def printDoc():
    try:

        '''
        
        SFTP (paying accounts only), this means I can not use import pysftp_extension
        
        
        '''
        from io import BytesIO
        from flask import send_from_directory, send_file
        import glob
        from docx import Document

        import pysftp_extension

        theList = []
        fname = constants.DOC_DIRECTORY + '*.docx'
        docList = glob.glob(fname)

        myhost = 'https://www.pythonanywhere.com/user/wayneraid'
        myUsername = '???'
        myPW = '????'

        remoteDir = 'https://www.pythonanywhere.com/user/wayneraid/files/home/wayneraid/surgenor/app/static/purchaseOrders/'


        with pysftp_extension.Connection(host=myhost, username=myUsername, password=myPW, disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"])) as sftp:
            for doc in docList:
                remotefname = remoteDir + doc
                sftp.get(remotefname, 'c/' + doc)

    except Exception as e:
        print(f'problem in printDoc: {e}')

    finally:
        return


'''
        for i in range(len(docList)):
            x = docList[i].replace('\\', '/')
            x = x.rsplit('/')
            theList.append(x[len(x) - 1])


        theList.sort()
        directory = constants.DOC_DIRECTORY
        for doc in theList:
            fname = directory + doc
            doc = Document()
            f = BytesIO()
            doc.save(f)
            f.seek(0)

            return send_file(f, as_attachment=True, download_name=fname)
'''


def addDocToDeleteQueue(fname: str) -> None:
    try:
        myLogInfo(funcName='addDocToDeleteQueue', msg=fname, myData=fname, user=None, tb=None)
        with open(constants.DOC_DIRECTORY + "deleteQueue.txt", "a") as deleteQueue:
            deleteQueue.write(fname)

    except Exception as e:
        myLogInfo('addDocToDeleteQueue', 'problem in addDocToDeleteQueue', e, None, traceback.format_exc())

    return


def deletePreviousPrintedFiles() -> None:
    try:

        # I was having problems with this func, mostly files couldn't be found so in the end
        # I now create myList and then use myLogInfo to files to be deleted but instead
        # of individually deleting the files I simply delete ALL docx files

        # myLogInfo(funcName='deletePreviousPrintedFiles', msg=None, myData=None, user=None, tb=None)

        with open(constants.DOC_DIRECTORY + "deleteQueue.txt", "r") as deleteQueue:
            for fname in deleteQueue:
                # myLogInfo(funcName='deletePreviousPrintedFiles', msg=fname, myData=fname, user=None, tb=None)
                myList = fname.split('.docx')

                for i in range(0, len(myList) - 1):
                    try:
                        # myLogInfo(funcName='deletePreviousPrintedFiles - for loop', msg=myList[i], myData=None, user=None, tb=None)
                        os.remove(constants.DOC_DIRECTORY + myList[i] + '.docx')
                    except FileNotFoundError:
                        pass  # ignore this error

                break

        # once all *.docx file have been deleted, delete the deleteQueue.txt file
        # in preparation of appending new *.docx files
        os.remove(constants.DOC_DIRECTORY + "deleteQueue.txt")

    except Exception as e:
        myLogInfo(funcName='deletePreviousPrintedFiles', msg='problem in deletePreviousPrintedFiles', myData=e, user=None, tb=traceback.format_exc())

    return


def myLogInfo(funcName: str, msg: str = None, myData=None, user: str = None, tb: str = None) -> None:

    '''
    parms - all parameters are optional except for funcName
    funcName: calling function
    msg: message to be printed
    myData: data to be printed via f string {}
    user: user, doesn't seem to be defined within utilities module???
    tb: traceback information

    my logging info will be written to => wayneraid.pythonanywhere.com.error.log and wayneraid.pythonanywhere.com.server.log
    '''

    try:
        # myDate = datetime.date.today() # format is: yyyy-MM-dd
        myDate = datetime.datetime.now()
        print(f">>> myLogInfo: {myDate} -- funcName => {funcName}. Msg => {msg}. myData => {myData}. User => {user}. Traceback => {tb}.")

    except Exception as e:
        print(f'problem in myLogInfo: {e}. Called by => {funcName}')

    finally:
        return


def getSalesBySupplier() -> list:
    try:
        resultset: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = "select count(*), substr(po, 1, instr(po, '_')-1) as supplier from OrderTbl where substr(PO, instr(PO, '_') + 1, 4) IN (select strftime('%Y', purchaseorderdate) from purchaseorder) group by supplier;"
        cur.execute(stmt)
        resultset = cur.fetchall()
        #conn.commit()
        cur.close()

        return resultset

    except Exception as e:
        print(f'getSalesBySupplier: {e}')


def getSalesByDepartment() -> list:
    try:
        resultset: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = "select count(*), deptname from OrderTbl where substr(PO, instr(PO, '_') + 1, 4) IN (select strftime('%Y', purchaseorderdate) from purchaseorder) group by deptName"
        cur.execute(stmt)
        resultset = cur.fetchall()
        #conn.commit()
        cur.close()

        return resultset

    except Exception as e:
        print(f'getSupplierByDepartment: {e}')


def getSalesByUser() -> list:
    try:
        resultset: list = []
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()
        stmt = "select count(*), orderUsername from OrderTbl where substr(PO, instr(PO, '_') + 1, 4) IN (select strftime('%Y', purchaseorderdate) from purchaseorder) group by orderUserName"
        cur.execute(stmt)
        resultset = cur.fetchall()
        #conn.commit()
        cur.close()

        return resultset

    except Exception as e:
        print(f'getSupplierByUser: {e}')

def removeNonActiveRecords() -> int:
    try:
        recordCount: int = 0
        count: int = 0
        db = getDatabase(constants.DATABASE_NAME)
        conn = getConnection(db)
        cur = conn.cursor()

        # Purchaser
        stmt = "select count(*) from Purchaser where purchaserActive = 0;"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = "insert into ARCHIVE_Purchaser (username, purchaserDeptId, purchaserActive, purchaserDateInActive, purchaserDateCreated) \
                select username, purchaserDeptId, purchaserActive, purchaserDateInActive, purchaserDateCreated \
                from Purchaser where purchaserActive = 0;"
        cur.execute(stmt)
        stmt = 'delete from Purchaser where purchaserActive = 0'
        cur.execute(stmt)

        # Supplier
        stmt = "select count(*) from Supplier where supplierActive = 0"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = 'insert into ARCHIVE_Supplier(supplierName, supplierProv, supplierActive, supplierDateCreated) \
                select supplierName, supplierProv, supplierActive, supplierDateCreated \
                from Supplier where supplierActive = 0;'
        cur.execute(stmt)
        stmt = 'delete from Supplier where supplierActive = 0;'
        cur.execute(stmt)

        # Department
        stmt = "select count(*) from department where active = 0;"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = 'insert into ARCHIVE_Department(deptname, dateCreated, active, dateInActive) \
                select deptname, dateCreated, active, dateInActive \
                from department where active = 0;'
        cur.execute(stmt)
        stmt = 'delete from Department where active = 0;'
        cur.execute(stmt)

        # User
        stmt = "select count(*) from user WHERE active = 0;"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = 'insert into ARCHIVE_User(givenName, surname, username, password, createDate, active, dateInActive, securityLevel) \
                select givenName, surname, username, password, createDate, active, dateInActive, securityLevel \
                from user WHERE active = 0;'
        cur.execute(stmt)
        stmt = 'delete from user where active = 0;'
        cur.execute(stmt)

        # Provincial Tax Rates
        stmt = "select count(*) from ProvincialTaxRates where active = 0;"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = 'insert into ARCHIVE_ProvincialTaxRates(provincialCode, taxRate, label, active) \
                select provincialCode, taxRate, label, active \
                from ProvincialTaxRates where active = 0;'
        cur.execute(stmt)
        stmt = 'delete from ProvincialTaxRates where active = 0;'
        cur.execute(stmt)

        # Order table
        stmt = "select count(*) FROM OrderTbl WHERE OrderActive = 0;"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = 'INSERT INTO ARCHIVE_OrderTbl(OrderNbr, OrderSupplierId, deptName, OrderPartDesc, OrderQuantity, OrderPartPrice, \
                    OrderReceivedDate, OrderReceivedBy, OrderReturnDate, OrderReturnQuantity, PO, OrderUsername, OrderActive) \
                SELECT OrderNbr, OrderSupplierId, deptName, OrderPartDesc, OrderQuantity, OrderPartPrice, OrderReceivedDate, \
                    OrderReceivedBy, OrderReturnDate, OrderReturnQuantity, PO, OrderUsername, OrderActive \
                FROM OrderTbl WHERE OrderActive = 0;'
        cur.execute(stmt)

        # becuz of foreign keys referenced in ordertbl you must first delete the foreign keys recs
        # from purchaseorder or set foreign keys off using pragma

        stmt = 'delete from OrderTbl where OrderActive = 0;'
        cur.execute(stmt)

        # Purchase Order
        stmt = "select count(*)  FROM PurchaseOrder WHERE purchaseOrderActive = 0;"
        cur.execute(stmt)
        count = cur.fetchone()
        recordCount += count[0]

        stmt = 'INSERT INTO ARCHIVE_PurchaseOrder(purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, \
                    purchaseOrderDateDeleted, purchaseOrderNbr, purchaseOrderPurchaserId, purchaseOrderPurchaserDeptId) \
                SELECT purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive, purchaseOrderDateDeleted, \
                    purchaseOrderNbr, purchaseOrderPurchaserId, purchaseOrderPurchaserDeptId \
                FROM PurchaseOrder WHERE purchaseOrderActive = 0;'
        cur.execute(stmt)

        # PRAGMA
        # foreign_keys = OFF;
        # PRAGMA
        # foreign_keys;

        '''
        stmt = 'delete from PurchaseOrder where purchaseOrderNbr in ( \
                select orderNbr \
                from OrderTbl, PurchaseOrder \
                where ordertbl.OrderActive = 0 and PurchaseOrder.purchaseOrderNbr = OrderTbl.OrderNbr);'
        '''
        cur.execute('PRAGMA foreign_keys = OFF;')

        stmt = 'delete from PurchaseOrder where purchaseOrderActive = 0'
        cur.execute(stmt)

        cur.execute('PRAGMA foreign_keys = OFF;')

        conn.commit()
        cur.close()

        return recordCount

    except Exception as e:
        print(f'removeNonActiveRecords: {e}')



