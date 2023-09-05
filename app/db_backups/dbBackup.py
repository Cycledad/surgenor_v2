import os
import datetime
from app import utilities

# set local for testing purposes
local = True

try:

    x = datetime.datetime.now()
    yr = x.strftime("%G")
    mth = x.strftime("%m")
    dd = x.strftime("%d")

    # _2023_12_31
    d = '_' + yr + '_' + mth + '_' + dd

    '''
    1. backup database
    2. Clean  database
    
    '''


    if local:
        src = r'C:\Users\wayne\surgenor_v2\app\mysite.db'
        dest = r'C:\Users\wayne\surgenor_v2\app\mysite' + d + '.db'

        # BACKUP
        print('local')
        print('src: ' + src)
        print('dest: ' + dest)
        cmd = f'copy "{src}" "{dest}"'
        print('cmd: ' + cmd)

        os.system(cmd)
        # os.system(f'{cmd}')
        # os.system('cmd /c "Your Command Prompt Command"')
        # os.system('copy source.txt destination.txt')
        # cmd = f'copy "{src}" "{dst}"'

    else:
        src = r'/home/wayneraid/surgenor/app/mysite.db'
        dest = r'/home/wayneraid/surgenor/app/db_backups' + '/mysite' + d + '.db'

        # BACKUP
        print('server')
        print('src: ' + src)
        print('dest: ' + dest)
        os.system("cp " + src + " " + dest)

    # CLEANUP
    utilities.removeNonActiveRecords()


except Exception as e:
    print(f'error found - {e}')
