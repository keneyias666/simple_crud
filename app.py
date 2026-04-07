from flask import Flask,render_template,request,redirect,flash
from dbhelper import *

app = Flask(__name__)
app.secret_key = "eliasponkanviruscholo!@#!#$#@"


@app.route("/deleteproduct",methods=['GET'])
def deleteproduct()->None:
    itemcode:str = request.args.get('itemcode') # so ang nahitabo ani kay gi kuha nimo or and itemcode para mabuhat as a string 
    ok:bool = deleteitem('products',itemcode=itemcode) # niya kani mao nani argument na gi kuka nimo ang itemcode gikan sa db helper na database niya ang pangan sa database kay products na table
    if (ok): # condition if okay or true
        flash(f"{itemcode} has been deleted !!","success")
    else: # then else kung dili ok or false
        flash(f"error deleting {itemcode}!!","error")
    return redirect("/") # then mo direct dayon or bali mo refresh dayon ang page mao mani iya e return or bali pasabot ana kay render

@app.route("/saveproduct",methods=['POST'])
def saveproduct()->None:
    itemcode:str = request.form['itemcode']     # kani na lines mao ni ang pag initialize sa mga variables na naa sa database, bali ang mga attributes na naa sa database
    productname:str = request.form['productname']
    unit:str = request.form['unit']
    price:str = request.form['price']
    qty:str = request.form['qty']
    edit:str = request.form['edit']
    old_itemcode:str = request.form.get('old_itemcode', '')    # kani na lines mao ni ang pag initialize sa mga variables na naa sa database, bali ang mga attributes na naa sa database
    
    if edit=="1":
        # If item code changed, we need to update with the old itemcode as WHERE clause or condition niya mao ni siya UPDATE
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
        # kani if mag ADD nakag product and basically imo ra e display ang mga old products na naa sa database then imo e display ang new products na imo gi input
        ok:bool = additem('products',itemcode=itemcode,productname=productname,unit=unit,price=price,qty=qty)
        #
        if ok==True:
            flash("New Product Added Successfully","success")
        else:
            flash("Error Adding Product","error")
        #
    return redirect("/") # bali mao ni siya ang para refresh sa page

@app.route("/")
def index()->None:
    rows:list = getall('products')
    header:list = ['itemcode','product','unit','price','qty','total']
    return render_template("index.html",title="PRODUCTS",data=rows,header=header)
    # kani mao nani imo main route bali mao ni siya ang homepage niya iya ra gi display ang mga products na naa sa database, then gi gamit niya ang format sa html pag render sa template
    # para naay design and format

if __name__=="__main__": #kani mao ni bali rason nganong maka type ka lahos sa cmd or sa terminal sa py app.py kay bali pag e call nimo ang name sa program mo automatic mangita siya sa main niya iya e run
    app.run(debug=True) # kani is kanang mag update ka sa code mo automatic mo debug or mo update sa changes niya, ma display imo changes sag running ang program itself