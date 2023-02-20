try:
    from flask import Flask
    import requests


    from flask_bcrypt import Bcrypt

    # from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    session = requests.Session()


    bcrypt = Bcrypt(app)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

    # from app.constants import DATABASE_NAME
    import app.constants as constants
    from app import utilities, routes

    dbName = utilities.getDatabase(constants.DATABASE_NAME)
    conn = utilities.getConnection(dbName)  # create db if it doesn't already exist
    conn.close()

    if constants.RELOAD_DATABASE:
        utilities.reloadDatabase()


    # app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    # db = SQLAlchemy(app)

    # from app import routes

    # from sqlalchemy as db
    # engine = db.create_engine("sqlite:///site.db")
    # engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # result = utilities.getUnitDesc(1)

    # result = utilities.getTableItem(1, 'supplier', 'supplierName')
    # print(result)

    # result = utilities.getTableItemById(1, 'part', 'partDesc')
    # print(result)


except Exception as e:
    print(f'issue in __init__.py => {e}')
