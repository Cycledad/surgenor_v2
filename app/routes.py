import datetime as dt
import json
import os

from flask import render_template, request, redirect, url_for, flash, session

from app import app, bcrypt, constants
from app import utilities

import traceback

# from app import models


@app.route('/home')
def home():
    try:

        '''
        if session.get('loggedOn', None)  == None:
            flash('Please login!', 'danger' )
            return redirect(url_for('login'))
        '''
        if 'lang' not in session:
            utilities.createSessionObjects('', session)

    except Exception as e:
        print(f'problem in home: {e}')
 
    return render_template('home.html')


@app.route('/addPurchaser', methods=['GET', 'POST'])
def addPurchaser():
    try:
        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if request.method == "POST":
            req = request.form
            username = req.get('username')
            result = utilities.getUser(username)
            if result is None:
                flash('invalid username in addPurchaser - purchaser must ALREADY be a registered user', 'warning')
                raise Exception('invalid username in addPurchaser')
            #givenName = req.get('givenName')
            #surname = req.get('surname')
            #name = req['pName']
            active = True if req['pActive'] == 'YES' else False  # 1=true, 0=false
            deptName = req['selectDepartment']
            # dateCreated = dt.date.today() - done now in db
            deptId = utilities.getDepartmentId(deptName)
            #parms = (givenName, surname, deptId, active,)
            parms = (username, deptId, active,)
            utilities.insertPurchaser(parms)

    except Exception as e:
        print(f'problem in addPurchaser: {e}')

    listDeptNames = utilities.getALLDepartmentNames()
    return render_template('addPurchaser.html', listDeptNames=listDeptNames)


@app.route('/addDepartment', methods=['GET', 'POST'])
def addDepartment():
    try:
        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if request.method == "POST":
            req = request.form
            deptName = req['deptName']
            active = True if req['deptActive'] == 'YES' else False  # 1=true, 0=false
            # dateCreated = dt.date.today() - now set as default in db
            parms = (deptName, active,)
            utilities.insertDepartment(parms)

    except Exception as e:
        print(f'problem in addDepartment: {e}')

    return render_template('addDepartment.html')


@app.route('/addSupplier', methods=['GET', 'POST'])
def addSupplier():
    try:
        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if request.method == "POST":
            req = request.form
            supplierName = req['supplierName']
            # supplierAddr = req['supplierAddr']
            supplierProv = req['supplierProv']
            # supplierContactName = req['supplierContactName']
            # supplierTel = req['supplierTel']
            # supplierEmail = req['supplierEmail']
            supplierActive = True
            # supplierDateCreated = dt.date.today() - now set as default in db
            parms = (supplierName, supplierProv, supplierActive,)
            utilities.insertSupplier(parms)

    except Exception as e:
        print(f'problem in addSupplier: {e}')

    return render_template('addSupplier.html')


@app.route('/addOrder', methods=['GET', 'POST'])
def addOrder():
    try:
        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if request.method == "POST":
            req = request.form
            #print(f'This is a request - {req}')
            resultList = list(req.values())

            # 1st update the purchaseOrder table then update the order table
            purchaseOrderNbr = resultList[0]
            purchaserName = resultList[1]
            if purchaserName == 'None':
                #flash(session['invalidPurchaser'], 'warning')
                flash(session['invalidPurchaser'], 'danger')
                raise Exception(f'User {purchaserName} is not authorized to purchase')

            purchaserId = utilities.getPurchaserId(session['username'])
            purchaserDeptId = utilities.getPurchaserDeptId(session['username'])
            utilities.insertPurchaseOrder(purchaseOrderNbr, purchaserId, purchaserDeptId)

            # resultList minus 3 gives total nbr of order items, less PONbr and purchaser
            # take total nbr of order items and divide by 5 gives nbr of recs to insert

            resultList.insert(2, session['username'])

            nbrOfOrderItems = len(resultList) - 3  # first 3 items are the same for all orders
            nbrOfRecs = int(nbrOfOrderItems / 4)  # 5 is the nbr of items per rec

            i: int = 3
            for idx in range(0, nbrOfRecs):
                if idx == nbrOfRecs:
                    break
                orderNbr = purchaseOrderNbr
                username = resultList[2]
                supplierName = resultList[i]
                i += 1
                quantity = resultList[i]
                i += 1
                #partNbr = resultList[i]
                #i += 1
                partDesc = resultList[i]
                i += 1
                unitPrice = resultList[i]
                i += 1

                # parms = (orderNbr, partDesc, supplierName, quantity, unitPrice, session['username'])
                parms = (purchaseOrderNbr, partDesc, supplierName, quantity, unitPrice, session['username'])
                #parms = (orderNbr, partNbr, partDesc, supplierName, quantity, unitPrice, session['username'])

                # creates order in the orderTbl ... there can be many orders for one purchase order
                utilities.insertOrder(parms)

           # now that ALL orders have been created, create the print doc in directory static/purchaseOrders ...

            orderList = utilities.getOrderByOrderNbr(purchaseOrderNbr, session['securityLevel'])
            utilities.createPrintDoc(orderList)

            return render_template('home.html')

    except Exception as e:
        print(f'problem in addOrder: {e}')

    purchaseOrderNbr = utilities.getOrderNbr()
    purchaseOrderNbr += 1
    utilities.updateOrderNbr(purchaseOrderNbr)

    # having concurrency issues regarding po nbr so now use code above
    #
    # #orderNbr = utilities.getMaxOrderNbr() #Kevin asks that po number start at 1000
    # if orderNbr < 1000:
    #    orderNbr = 1000
    # else:
    #    orderNbr += 1

    purchaserName = utilities.getPurchaser(session['username'])

    #listPurchaserName = utilities.getALLPurchasers()
    # listPurchaserName = utilities.getALLITEMS('purchaser', 'purchaserName')
    #listPartDesc = utilities.getALLPartDesc()
    # listPartDesc = utilities.getALLITEMS('part', 'partDesc')
    #listPartNbr = utilities.getALLPartNbr()
    # listPartNbr = utilities.getALLITEMS('part', 'partNbr')
    listSupplierNames = utilities.getALLSupplierName()
    # listSupplierNames = utilities.getALLITEMS('supplier', 'SupplierName')
    #listUnits = utilities.getALLITEMS('UNIT', 'UnitDesc')
    #return render_template('addOrder.html', listPartDesc=listPartDesc, purchaserName=purchaserName, listSupplierNames=listSupplierNames,
    #                       listUnits=listUnits, orderNbr=orderNbr, username=session['username'], lang=session['lang'])
    return render_template('addOrder.html', purchaserName=purchaserName, listSupplierNames=listSupplierNames,
                           orderNbr=purchaseOrderNbr, username=session['username'], lang=session['lang'])

    # return render_template('addOrder.html', purchaserName=purchaserName, listSupplierNames=listSupplierNames,
    #                       orderNbr=orderNbr, username=session['username'], lang=session['lang'])
    #return render_template('addOrder.html', listPartDesc=listPartDesc, listPartNbr=listPartNbr,
    #                       listPurchaserName=listPurchaserName, listSupplierNames=listSupplierNames,
    #                       listUnits=listUnits, orderNbr=orderNbr, username=session['username'], lang=session['lang'])


@app.route('/addPart', methods=['GET', 'POST'])
def addPart():
    try:
        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if request.method == 'POST':
            req = request.form

            # ternary if statement => <expr1> if <conditional_expr> else <expr2> =>  s = 'minor' if age < 21 else 'adult'
            # inStock = 1 if req['partInStock'] == 'on' else 0  #where 1=True, 0=False
            # query = db.insert(Student).values(Id=1, Name='Matthew', Major="English", Pass=True)
            # Result = conn.execute(query)

            # stmt = "insert into Part(id, partNbr, partDesc, partQuantity, partInStock, 'partDateCreated') values ( :partNbr, :partDesc, :partQuantity, :partInStock)"
            # stmt = "insert into Part(partNbr, partDesc, partSupplier, partQuantity, partInStock, partDateCreated) values (:partNbr, :partDesc, :partSupplier, :partQuantity, :partInStock, :partDateCreated)"

            dtCreated = dt.date.today()
            inStock: bool = True if req['partInStock'] == 'YES' else False  # 1=true, 0=false
            supplierName = req['selectSupplier']
            supplierId = utilities.getSupplierId(supplierName)

            params = (req['partNbr'], req['partDesc'], supplierId, req['partQuantity'], inStock, dtCreated)
            utilities.insertPart(params)

    except Exception as e:
        print(f'problem in addPart: {e}')

    listSupplierNames = utilities.getALLITEMS('supplier', 'SupplierName')
    listUnits = utilities.getALLITEMS('UNIT', 'UnitDesc')
    listPurchaserName = utilities.getALLPurchasers()
    # .getALLITEMS('purchaser', 'purchaserName')

    return render_template('addPart.html', listSupplierNames=listSupplierNames, listUnits=listUnits,
                           listPurchaserName=listPurchaserName)


@app.route('/adminHome')
def adminHome():
    try:
        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('home'))

    except Exception as e:
        print(f'problem in adminHome: {e}')

    return render_template('AdminBase.html')

@app.route('/resetUserPassword', methods=['GET', 'POST'])
def resetUserPassword():
    try:
        # if already logged in
        #if not session.get('loggedOn', None) is None:
        #    flash(session['alreadyLoggedIn'], 'info')
        #    return redirect(url_for('home'))
        username = ''

        if request.method == 'POST':
            req = request.form
            username = req['username']
            pw = req['password']
            #registered = utilities.
            # getUserRegistered(username)
            result = utilities.getUser(username)
            if result is None:
                registered = False
            else:
                registered = result[6]
            if not registered:
                flash('username not registered or is not active', 'danger')
                #return redirect(url_for('resetUserPassword'))
            else:
                hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
                #hashed_pw = utilities.getPassword(username)
                # TO COMPARE PASSWORD FOR VALIDITY
                pw_check = bcrypt.check_password_hash(hashed_pw, pw)
                if not pw_check:
                    flash('password not valid', 'danger')
                    #return redirect(url_for('resetUserPassword'))
                else:
                    # session['loggedOn'] = True
                    # session['securityLevel'] = utilities.getUserSecurityLevel(username)
                    # session['lang'] = 'en-us'  # english is default language
                    # session['username'] = username
                    # utilities.createSessionObjects('fr', session) #send 'fr' so that 'en' lang is loaded ... yeah I know .... wtf ...
                    success = utilities.updateUserPassword(username, hashed_pw)
                    if success:
                        flash('Password Updated!', 'success')
                    else:
                        flash('Problem updating password, check err log', 'danger')

                    #return redirect(url_for('resetUserPassword'))

    except Exception as e:
        print(f'problem in resetUserPassword: {e}')

    #send username as a parm so that entered username remains in input textbox after submission
    return render_template('resetUserPassword.html', username=username)  # passed user and password validation


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        # if already logged in
        if not session.get('loggedOn', None) is None:
            flash(session['alreadyLoggedIn'], 'info')
            return redirect(url_for('home'))

        if request.method == 'POST':
            req = request.form
            username = req['username']
            pw = req['password']
            #registered = utilities.getUserRegistered(username)
            result = utilities.getUser(username)
            if result is None:
                registered = False
            else:
                registered = result[6]
            if not registered:
                flash(session['notRegistered'], 'danger')
                return redirect(url_for('register'))
            else:
                # hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
                hashed_pw = utilities.getPassword(username)
                # TO COMPARE PASSWORD FOR VALIDITY
                pw_check = bcrypt.check_password_hash(hashed_pw, pw)
                if not pw_check:
                    flash(session['invalidpw'], 'danger')
                    return redirect(url_for('login'))
                else:
                    session['loggedOn'] = True
                    session['securityLevel'] = utilities.getUserSecurityLevel(username)
                    session['lang'] = 'en-us'  # english is default language
                    session['username'] = username
                    # utilities.createSessionObjects('fr', session) #send 'fr' so that 'en' lang is loaded ... yeah I know .... wtf ...

                    return redirect(url_for('home'))

    except Exception as e:
        print(f'problem in login: {e}')

    return render_template('login.html')  # passed user and password validation


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:

        if not session.get('loggedOn', None) is None:
            flash(session['alreadyLoggedIn'], 'info')
            return redirect(url_for('home'))

        if request.method == 'POST':
            req = request.form
            givenName = req.get('givenName')
            surname = req.get('surname')
            username = req['username']
            pw = req['password']
            hashed_pw = bcrypt.generate_password_hash(pw).decode('utf-8')
            # TO COMPARE PASSWORD FOR VALIDITY
            pw_check = bcrypt.check_password_hash(hashed_pw, pw)
            result = utilities.getUser(username)
            if result is None:
                registered = False
            else:
                registered = result[6]
            if registered:
                flash(session['alreadyRegistered'], 'danger')
                # return redirect(url_for('login'))
            else:
                utilities.registerUser(username, hashed_pw, givenName, surname)
                flash(session['registered'], 'success')
                return redirect(url_for('login'))

    except Exception as e:
        flash(f'{e}', 'danger')
        print(f'problem in register: {e}')

    return render_template('register.html')


@app.route('/api/data/manageDepartment/<action>/<value>', methods=['GET'])
@app.route('/api/data/manageDepartment', methods=['GET'])
# api/data/manageDepartment?action=update&value=1,Executive,2023-01-04,5'
def apimanageDepartment():
    myList: list = []
    aList: list = []

    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'update':
        value = request.args.get('value', '')
        myList = value.split(',')
        id = myList[0]
        dept = myList[1]
        dateCreated = myList[2]
        active = myList[3]
        dateInActive = myList[4]
        utilities.updateDepartment(id, dept, dateCreated, active, dateInActive)

    '''
    if action == "delete" or active == False:
        id = request.args.get('value', '')
        utilities.deleteDepartment(id)
    '''

    # reload tabulator.js table
    resultList = utilities.getTable('Department')
    for row in resultList:
        aList = (row[0], row[1], row[2], row[3], row[4])
        d1 = dict(enumerate(aList))
        myList.append(d1)

    x = json.dumps(myList)

    return x


@app.route('/manageDepartment')
def manageDepartment():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('adminHome'))

    except Exception as e:
        print(f'problem in manageDepartment: {e}')

    return render_template('manageDepartment.html')


@app.route('/api/data/manageParts/<action>/<value>', methods=['GET'])
@app.route('/api/data/manageParts', methods=['GET'])
# api/data/manageParts?action=update&value=1,Executive,2023-01-04,5'
def apimanageParts():
    myList: list = []
    aList: list = []

    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'update':
        value = request.args.get('value', '')
        myList = value.split(',')
        id = myList[0]
        partNbr = myList[1]
        partDesc = myList[2]
        partSupplierId = myList[3]
        partQuantity = myList[4]
        partInStock = myList[5]
        partDateOutOfStock = myList[6]
        partDateCreated = myList[7]

        utilities.updateParts(id, partNbr, partDesc, partSupplierId, partQuantity, partInStock, partDateOutOfStock,
                              partDateCreated)

    '''
    if action == "delete" or active == False:
        id = request.args.get('value', '')
        utilities.deleteDepartment(id)
    '''

    # reload tabulator.js table
    resultList = utilities.getTable('Part')
    for row in resultList:
        aList = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        d1 = dict(enumerate(aList))
        myList.append(d1)

    x = json.dumps(myList)

    return x


@app.route('/manageParts')
def manageParts():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('adminHome'))

    except Exception as e:
        print(f'problem in manageParts: {e}')

    return render_template('manageParts.html')


@app.route('/api/data/managePurchaseOrder/<action>/<orderId>/<quantity>', methods=['GET'])
@app.route('/api/data/managePurchaseOrder/<action>/<orderId>/<dt_order_received>/<dt_order_returned>',
           methods=['GET'])  # /api/data?orderid=1&dt=28-12-2022
@app.route('/api/data/managePurchaseOrder', methods=['GET'])
def data(orderId=None, dt_order_received=None, dt_order_returned=None, quantity=None):
    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'updateOrderDate':
        value = request.args.get('value', '')
        myList = value.split(',')
        orderId = int(myList[0])
        dt_order_received = myList[1]
        dt_order_returned = myList[2]
        if dt_order_received == 'null':
            dt_order_received = ''
        if dt_order_returned == 'null':
            dt_order_returned = ''

        utilities.updateOrderReceivedDate(orderId, dt_order_received, dt_order_returned)

    if action == 'updateReturnQuantity':
        value = request.args.get('value', '')
        myList = value.split(',')
        orderId = int(myList[0])
        quantity = int(myList[1])
        utilities.updateOrderQuantity(orderId, quantity, 'orderReturnQuantity')

    if action == 'updateOrderQuantity':
        value = request.args.get('value', '')
        myList = value.split(',')
        orderId = int(myList[0])
        orderQuantity = int(myList[1])
        utilities.updateOrderQuantity(orderId, orderQuantity, 'OrderQuantity')

    if action == 'printOrder':
        value = request.args.get('value', '')
        myList = value.split(',')
        orderNbr = int(myList[0])
        orderList = utilities.getOrderByOrderNbr(orderNbr, session['securityLevel'])
        utilities.createPrintDoc(orderList)

        # utilities.printDoc()

        # return render_template('viewDoc.html', docName=docPath)
        # session['fname'] = fname
        # return redirect(url_for('viewDoc'))
        # filename = 'generatedDoc_132106.docx'
        # directory = '/home/wayneraid/surgenor/app/'
        # filename = 'generatedDoc_479247.docx'
        # directory = "C:\\Users\\wayne\\APP\\app\\"

        # send_from_directory(directory, filename, as_attachment=True)

    if action == 'receivedBy':
        value = request.args.get('value', '')
        myList = value.split(',')
        id = int(myList[0])
        receivedBy = myList[1]
        parms = (receivedBy, id,)
        utilities.updateOrderReceivedBy(parms)

    if action == 'activeFlg':
        value = request.args.get('value', '')
        myList = value.split(',')
        id = int(myList[0])
        active = int(myList[1])
        parms = (active, id,)
        utilities.updateActiveFlg(parms)

    securityLevel = session['securityLevel']
    resultList = utilities.getALLPurchaseOrders(securityLevel)  # returns a list of a list, so indice 1 = row, indice 2 = col within row, i.e. mylist[0][1]
    mylist: list = []
    alist: list = []
    for row in resultList:
        #replace username with given name and surname
        purchaserName = utilities.getPurchaser(row[2])
        alist = (row[0], row[1], purchaserName, row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],
            row[13], row[14], row[15], row[16], row[17])

        #alist = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],
        #    row[13], row[14], row[15], row[16], row[17])

        d1 = dict(enumerate(alist))
        mylist.append(d1)

    # return {'data': mylist} => use this format for datatables.js, dict of lists

    x = json.dumps(mylist)

    return x  # arry list


@app.route('/managePurchaseOrder', methods=['GET', 'POST'])
def managePurchaseOrder():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        # all users need to managePurchaseOrders not just admin
        # if session['securityLevel'] < constants.GOD_LEVEL:
        #    flash(session['securityLevel5'], 'warning')
        #    return redirect(url_for('adminHome'))

    except Exception as e:
        print(f'problem in managePurchaseOrder: {e}')

    return render_template('managePurchaseOrder.html')


@app.route('/logout')
def logout():
    # session.pop('loggedOn')
    # session.pop('securityLevel')
    session.clear()
    return redirect(url_for('home'))


@app.route('/api/data/manageSupplier/<action>/<value>', methods=['GET'])
@app.route('/api/data/manageSupplier', methods=['GET'])
# api/data/manageSupplier?action=update&value=1,Executive,2023-01-04,5'
def apimanageSupplier():
    myList: list = []
    aList: list = []

    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'update':
        value = request.args.get('value', '')
        myList = value.split(',')
        id = int(myList[0])
        supplierName = myList[1]
        supplierProv = myList[2]
        supplierDateInActive = myList[3]
        supplierDateCreated = myList[4]
        # supplierAddr = myList[2]
        # supplierProv = myList[3]
        # supplierTel = myList[4]
        # supplierEmail = myList[5]
        # supplierContact = myList[6]
        # supplierActive = myList[7]
        # supplierDateInActive = myList[8]
        # supplierDateCreated = myList[9]

        utilities.updateSupplier(id, supplierName, supplierProv, supplierDateInActive, supplierDateCreated)

        # utilities.updateSupplier(id, supplierName, supplierAddr, supplierProv, supplierTel, supplierEmail,
        #                         supplierContact, supplierActive, supplierDateInActive, supplierDateCreated)

    # reload tabulator.js table
    resultList = utilities.getTable('Supplier')
    for row in resultList:
        aList = (row[0], row[1], row[2], row[3], row[4])
        d1 = dict(enumerate(aList))
        myList.append(d1)

    x = json.dumps(myList)

    return x
    # return (myList)


@app.route('/api/data/managePurchaseOrderTable/<action>/<value>', methods=['GET'])
@app.route('/api/data/managePurchaseOrderTable', methods=['GET'])
def apimanagePurchaseOrderTable():
    myList: list = []
    aList: list = []

    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'update':
        value = request.args.get('value', '')
        myList = value.split(',')
        id = int(myList[0])
        purchaseOrderDate = myList[1]
        purchaseOrderReceivedDate = myList[2]
        purchaseOrderActive = myList[3]
        purchaseOrderDateDeleted = myList[4]
        purchaseOrderNbr = myList[5]
        purchaseOrderPurchaserId = myList[6]
        purchaseOrderPurchaserDeptId = myList[7]

        utilities.updatePurchaseOrderTable(id, purchaseOrderDate, purchaseOrderReceivedDate, purchaseOrderActive,
                                           purchaseOrderDateDeleted, purchaseOrderNbr,
                                           purchaseOrderPurchaserId, purchaseOrderPurchaserDeptId)

    # reload tabulator.js table
    resultList = utilities.getTable('PurchaseOrder')
    for row in resultList:
        aList = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        d1 = dict(enumerate(aList))
        myList.append(d1)

    x = json.dumps(myList)

    return x


@app.route('/manageSupplier')
def manageSupplier():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        # if session['securityLevel'] < constants.GOD_LEVEL:
        #    flash(session['securityLevel5'], 'warning')
        #    return redirect(url_for('Adminhome'))

    except Exception as e:
        print(f'problem in manageSupplier: {e}')

    return render_template('manageSupplier.html')


@app.route('/managePurchaseOrderTable')
def managePurchaseOrderTable():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('adminHome'))

    except Exception as e:
        print(f'problem in managePurchaseOrderTable: {e}')

    return render_template('managePurchaseOrderTable.html')


@app.route('/api/data/managePurchaser/<action>/<value>', methods=['GET'])
@app.route('/api/data/managePurchaser', methods=['GET'])
# api/data/managePurchaser?action=update&value=1,Executive,2023-01-04,5'
def apimanagePurchaser():
    myList: list = []
    aList: list = []

    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'update':
        value = request.args.get('value', '')
        myList = value.split(',')

        id = int(myList[0])
        username = myList[1]
        purchaserDeptId = myList[2]
        purchaserActive = myList[3]
        purchaserDateInActive = myList[4]
        purchaserDateCreated = myList[5]

        utilities.updatePurchaser(id, username, purchaserDeptId, purchaserActive, purchaserDateInActive, purchaserDateCreated)

    # reload tabulator.js table
    resultList = utilities.getTable('Purchaser')
    for row in resultList:
        aList = (row[0], row[1], row[2], row[3], row[4], row[5])
        d1 = dict(enumerate(aList))
        myList.append(d1)

    x = json.dumps(myList)

    return x
    # return (myList)


@app.route('/managePurchaser')
def managePurchaser():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('adminHome'))

    except Exception as e:
        print(f'problem in managePurchaser: {e}')

    return render_template('managePurchaser.html')


@app.route('/api/data/manageProvincialTaxRates', methods=['GET'])
def apimanageProvincialTaxRates():
    try:
        # set arg to '' not present
        action = request.args.get('action', '')

        # if args ARE passed
        if action == 'update':
            # set arg to '' if not present
            value = request.args.get('value', '')
            myList = value.split(',')

            id = int(myList[0])
            provincialCode = myList[1]
            taxRate = myList[2]
            label = myList[3]
            # active = myList[4] - now set as default in db
            parms = (provincialCode, taxRate, label, id,)
            # save update
            utilities.updateProvincialTaxRates(parms)  # save update

        # reload tabulator
        myList = []
        resultList = utilities.getTable('ProvincialTaxRates')
        for row in resultList:
            aList = (row[0], row[1], row[2], row[3], row[4])
            d1 = dict(enumerate(aList))
            myList.append(d1)

        x = json.dumps(myList)

        return x

    except Exception as e:
        print(f"problem in manageProvincialTaxRates: {e}.  User => {session['username']}")


@app.route('/api/data/manageUser/<action>/<value>', methods=['GET'])
@app.route('/api/data/manageUser', methods=['GET'])
# api/data/managePurchaser?action=update&value=1,Executive,2023-01-04,5'
def apimanageUser():
    myList: list = []
    aList: list = []

    # set arg to '' not present
    action = request.args.get('action', '')

    # if args ARE passed
    if action == 'update':
        value = request.args.get('value', '')
        myList = value.split(',')

        id = int(myList[0])
        givenName = myList[1]
        surname = myList[2]
        username = myList[3]
        password = myList[4]
        createDate = myList[5]
        active = myList[6]
        dateInactive = myList[7]
        securityLevel = myList[8]

        utilities.updateUser(id, givenName, surname, username, password, createDate, active, dateInactive, securityLevel)

    # reload tabulator.js table
    resultList = utilities.getTable('User')
    for row in resultList:
        aList = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        d1 = dict(enumerate(aList))
        myList.append(d1)

    x = json.dumps(myList)

    return x


@app.route('/manageProvincialTaxRates')
def manageProvincialTaxRates():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('adminHome'))

    except Exception as e:
        print(f"problem in manageProvincialTaxRates: {e}.  User => {session['username']}")

    return render_template('manageProvincialTaxRates.html')


@app.route('/manageUser')
def manageUser():
    try:

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        if session['securityLevel'] < constants.GOD_LEVEL:
            flash(session['securityLevel5'], 'warning')
            return redirect(url_for('adminHome'))

    except Exception as e:
        print(f"problem in manageUser: {e}.  User => {session['username']}")

    return render_template('manageUser.html')


@app.route('/viewDoc', methods=['GET', 'POST'])
def viewDoc():
    try:
        from flask import send_from_directory
        import glob
        theList = []

        if session.get('loggedOn', None) is None:
            flash(session['pleaseLogin'], 'danger')
            return redirect(url_for('login'))

        utilities.myLogInfo(funcName='viewDoc', msg=None, myData=None, user=session['username'], tb=None)

        utilities.deletePreviousPrintedFiles()

        fileTemplate = constants.DOC_DIRECTORY + '*.docx'
        docList = glob.glob(fileTemplate)
        # separate filenames from directory name
        for i in range(len(docList)):
            x = docList[i].replace('\\', '/')
            x = x.rsplit('/')
            theList.append(x[len(x) - 1])

        if request.method == 'POST':

            req = request.form

            #print(f'viewdoc post - req is: {req}')
            # executing LOCALLY

            # executing on SERVER
            # directory = '/home/wayneraid/surgenor/app/'

            # was getting permission err, so now change permission to ALL access, print, and then switch back to write protect
            # problem in viewDoc: [Errno 13] Permission denied: '/home/wayneraid/surgenor/app/static/purchaseOrders/GMC_2023-01-18_001.docx'
            # write protect document, IROTH = can be read by others
            # fname = req['selFile']
            # filePathName = directory + fname
            # os.chmod(filePathName, stat.S_IRWXO )

            # fname = req['selFile']

            # clear any flash messages - doesnt seem to work
            # session.pop('_flashes', None)

            fname = request.form.get('selFile', '')
            utilities.myLogInfo(funcName='viewDoc', msg='post - fname', myData=fname, user=session['username'], tb=None)

            if len(docList) == 0:
                # utilities.myLogInfo(funcName='viewDoc', msg=' post - len(docList) == 0', myData=docList, user=session['username'], tb=None)
                return render_template('viewDoc.html', docList=['no files found'])
            elif fname == '':
                # utilities.myLogInfo(funcName='viewDoc', msg='post - happens when submit button is pressed with no selection', myData=fname,
                #                    user=session['username'], tb=None)
                # this happens when submit button is pressed with no selection
                return render_template('viewDoc.html', docList=theList)
            elif fname not in theList:
                # didnt like the way this looked .... flash('Document not available to print', 'warning')
                return render_template('viewDoc.html', docList=theList)
            else:
                utilities.addDocToDeleteQueue(fname)
                #utilities.myLogInfo(funcName='viewDoc', msg='post - just BEFORE call to send_from_directory',
                #                    myData=fname,
                #                    user=session['username'], tb=None)

                # remove fname from list before sending
                #theList.remove(fname)
                return send_from_directory(constants.DOC_DIRECTORY, fname, as_attachment=True)


                #utilities.myLogInfo(funcName='viewDoc', msg='post - just AFTER call to send_from_directory',
                #                    myData=fname,
                #                    user=session['username'], tb=None)

        if len(docList) < 1:
            utilities.myLogInfo(funcName='viewDoc', msg='len(docList) < 1', myData=docList, user=session['username'], tb=None)
            return render_template('viewDoc.html', docList=['no files found'])

        return render_template('viewDoc.html', docList=theList)

    except Exception as e:
        utilities.myLogInfo(funcName='viewDoc', msg='problem in viewDoc', myData=None, user=session['username'], tb=traceback.format_exc())

    finally:

        # return redirect(url_for('viewDoc'))

        '''
        if len(theList) == 0:
            return render_template('viewDoc.html', docList=['no files found'])
        else:
            return render_template('viewDoc.html', docList=theList)
        '''

# no longer used as per Kevin Fri Feb 17, 2023
@app.route('/stats', methods=['GET'])
def stats():
    # not used
    try:
        activeDepts: list = []
        inActiveDepts: list = []
        activePurchasers: list = []
        inActivePurchasers: list = []
        activeSuppliers: list = []
        inActiveSuppliers: list = []
        activeUsers: list = []
        inActiveUsers: list = []
        purchaseOrders = utilities.getCount('purchaseOrder')
        orders = utilities.getCount('orderTbl')
        users = utilities.getCount('user')
        suppliers = utilities.getCount('supplier')
        purchaser = utilities.getCount('purchaser')
        department = utilities.getCount('department')

        activeDepartments = utilities.getActive('department', 'active', True)
        for each in activeDepartments:
            activeDepts.append(each[1])

        inActiveDepartments = utilities.getActive('department', 'active', False)
        for each in inActiveDepartments:
            inActiveDepts.append(each[1])

        activePurchasersInTable = utilities.getActive('purchaser', 'purchaseractive', True)
        for each in activePurchasersInTable:
            activePurchasers.append(each[1])

        inActivePurchasersInTable = utilities.getActive('purchaser', 'purchaseractive', False)
        for each in inActivePurchasersInTable:
            inActivePurchasers.append(each[1])

        activeSuppliersInTable = utilities.getActive('supplier', 'supplieractive', True)
        for each in activeSuppliersInTable:
            activeSuppliers.append(each[1])

        inActiveSuppliersInTable = utilities.getActive('supplier', 'supplieractive', False)
        for each in inActiveSuppliersInTable:
            inActiveSuppliers.append(each[1])

        activeUsersInTable = utilities.getActive('user', 'active', True)
        for each in activeUsersInTable:
            activeUsers.append(each[1])

        inActiveUsersInTable = utilities.getActive('user', 'active', False)
        for each in inActiveUsersInTable:
            inActiveUsers.append(each[1])

        # countActiveDepartments = utilities.getCountActive(tableName)
        # countinActiveDepartments = utilities.getCountinActive(tableName)
        orderByCount = utilities.getOrderByCount()
        orderbyMonth = utilities.getOrderByMonth()

        return render_template('stats.html', purchaseOrders=purchaseOrders, orders=orders, users=users,
                               suppliers=suppliers,
                               purchaser=purchaser, department=department, orderByCount=orderByCount,
                               orderByMonth=orderbyMonth, activeDepts=activeDepts, inActiveDept=inActiveDepts,
                               activePurchasers=activePurchasers,
                               inActivePurchasers=inActivePurchasers, activeSuppliers=activeSuppliers,
                               inActiveSuppliers=inActiveSuppliers,
                               activeUsers=activeUsers, inActiveUsers=inActiveUsers)

    except Exception as e:
        print(f'problem in stats: {e}')


@app.route('/language', methods=['GET'])
def language():
    try:
        if constants.currentLang is None:
            constants.currentLang = 'en-us'

        constants.currentLang = utilities.createSessionObjects(constants.currentLang, session)

        # return render_template('home.html')
        return redirect(request.referrer)

    except Exception as e:
        print(f'problem in language: {e}')


@app.route('/getPurchaserName', methods=['GET'])
def getPurchaserName():
    try:
        names = utilities.getALLPurchasers()

        return json.dumps(names)

    except Exception as e:
        print(f'problem in getPurchasername: {e}')


@app.route('/getLanguage', methods=['GET'])
def getLanguage() -> str:
    try:
        lang = session['lang']
        #lang = json.dumps(lang)

        return lang

    except Exception as e:
        print(f'problem in getLanguage: {e}')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        supplierLabels: list = []
        supplierData: list = []
        myList = utilities.getSalesBySupplier()
        for row in myList:
            supplierLabels.append(row[1])
            supplierData.append(row[0])

        deptLabels: list = []
        deptData: list = []
        myList = utilities.getSalesByDepartment()
        for row in myList:
            deptLabels.append(row[1])
            deptData.append(row[0])

        userLabels: list = []
        userData: list = []
        myList = utilities.getSalesByUser()
        for row in myList:
            userLabels.append(row[1])
            userData.append(row[0])

        monthLabels: list = []
        monthData: list = []
        myList = utilities.getOrderByMonth()
        for row in myList:
            monthLabels.append(row[0])
            monthData.append(row[1])



        return render_template('dashboard.html', supplierLabels=supplierLabels, supplierData=supplierData,
                               deptLabels=deptLabels, deptData=deptData,
                               userLabels=userLabels, userData=userData,
                               monthLabels=monthLabels, monthData=monthData)

    except Exception as e:
        print(f'problem in dashboard: {e}')


@app.route('/restorePurchaseOrder', methods=['GET', 'POST'])
def restorePurchaseOrder():
    try:
        if request.method == 'POST':
            req = request.form
            PONbr = req['PONbr']
            # determine if PONbr is in archive database
            isPOArchived = utilities.isPOArchived(PONbr)
            if isPOArchived:
                rtn = utilities.restoreOrderTbl(PONbr)
                if rtn:
                    rtn = utilities.restorePurchaseOrderTbl(PONbr)
                    if rtn:
                        utilities.deleteARCHIVEDOrder(PONbr)
                        utilities.deleteARCHIVEDPurchaseOrder(PONbr)
                        flash(f'Purchase Order {PONbr} Restored ', 'danger')
                else:
                    flash(f'ISSUE restoring Purchase Order {PONbr}, check error log', 'danger')
            else:
                flash(f'Purchase Order {PONbr} not found in ARCHIVE', 'danger')

    except Exception as e:
        print(f'problem in restorePurchaseOrder: {e}')


    return render_template('restorePurchaseOrder.html')


@app.route('/archiveInActiveRecords', methods=['GET', 'POST'])
def archiveInActiveRecords():
    try:
        if request.method == 'POST':
            count = utilities.removeNonActiveRecords()
            flash(f'{count} InActive records archived!', 'warning')
    except Exception as e:
        print(f'problem in archiveInActiveRecords: {e}')
    finally:
        return render_template('archiveInActiveRecords.html')

