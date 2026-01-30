from flask import Flask,render_template,request,redirect,flash
from dbhelper import *

app = Flask(__name__)
app.secret_key = "lizsyanddennisdurano!@#!#$#@"


@app.route("/deleteproduct",methods=['GET'])
def deleteproduct()->None:
    itemcode:str = request.args.get('itemcode')
    ok:bool = deleteitem('products',itemcode=itemcode)
    if (ok):
        flash(f"{itemcode} has been deleted !!","success")
    else:
        flash(f"error deleting {itemcode}!!","error")
    return redirect("/")

@app.route("/saveproduct",methods=['POST'])
def saveproduct()->None:
    itemcode:str = request.form['itemcode']
    productname:str = request.form['productname']
    unit:str = request.form['unit']
    price:str = request.form['price']
    qty:str = request.form['qty']
    edit:str = request.form['edit']
    old_itemcode:str = request.form.get('old_itemcode', '')
    
    if edit=="1":
        # If item code changed, we need to update with the old itemcode as WHERE clause
        if old_itemcode and old_itemcode != itemcode:
            ok:bool = updateitem('products',old_itemcode=old_itemcode,itemcode=itemcode,productname=productname,unit=unit,price=price,qty=qty)
        else:
            ok:bool = updateitem('products',itemcode=itemcode,productname=productname,unit=unit,price=price,qty=qty)
        #
        if ok==True:
            flash("Product Updated Successfully","success")
        else:
            flash("Error Updating Product","error")
        #
    else:    
        ok:bool = additem('products',itemcode=itemcode,productname=productname,unit=unit,price=price,qty=qty)
        #
        if ok==True:
            flash("New Product Added Successfully","success")
        else:
            flash("Error Adding Product","error")
        #
    return redirect("/")

@app.route("/")
def index()->None:
    rows:list = getall('products')
    header:list = ['itemcode','product','unit','price','qty','total']
    return render_template("index.html",title="PRODUCTS",data=rows,header=header)
    
if __name__=="__main__":
    app.run(debug=True)