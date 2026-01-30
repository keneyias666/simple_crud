from sqlite3 import connect,Row
from icecream import ic

database:str = "crud.db"

def getprocess(sql:str)->list:
    global database
    conn = connect(database)
    conn.row_factory = Row
    cursor = conn.cursor()
    cursor.execute(sql)
    ic(sql)
    rows:list = cursor.fetchall()
    conn.close()
    return rows
    
def postprocess(sql)->bool:
    global database
    ok:bool = False
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute(sql)
        ic(sql)
        conn.commit()
        conn.close()
        ok = True
    except:
        ic(f"SQL Error:{sql}")
    return ok
    
def getall(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql)

def additem(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    values:list = list(kwargs.values())
    fld:str = "`,`".join(keys)
    dat:str = "','".join(values)
    sql:str = f"INSERT INTO `{table}`(`{fld}`) VALUES('{dat}')"
    ic(sql)
    return postprocess(sql)
    
def deleteitem(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    values:list = list(kwargs.values())
    sql:str = f"DELETE FROM `{table}` WHERE `{keys[0]}`='{values[0]}'"
    return postprocess(sql)
    
def updateitem(table:str,**kwargs)->None:
    keys:list = list(kwargs.keys())
    values:list = list(kwargs.values())
    fld:list = []
    where_key = keys[0]
    where_value = values[0]
    
    # If old_itemcode is provided, use it for WHERE clause
    if 'old_itemcode' in kwargs:
        where_key = 'old_itemcode'
        where_value = kwargs['old_itemcode']
        # Skip old_itemcode in the SET clause
        for i in range(len(keys)):
            if keys[i] != 'old_itemcode':
                fld.append(f"`{keys[i]}`='{values[i]}'")
    else:
        # Original behavior: skip first key-value for WHERE clause
        for i in range(1,len(values)):
            fld.append(f"`{keys[i]}`='{values[i]}'")
    
    fld_val:str = ",".join(fld)
    sql:str = f"UPDATE `{table}` SET {fld_val} WHERE `itemcode`='{where_value}'"
    return postprocess(sql) 