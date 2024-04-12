from flask import Flask, render_template, url_for, flash, redirect, abort
from forms import AddItemForm, EditItemForm, AddPaidMoneyForm
import datetime
from replit import db
import os
app = Flask(__name__)
app.secret_key = os.environ["APP_SECRET_KEY"]

def floatToMoney(value):

   return f"{float(value):.2f}"

def reset():
  db['itemList'] = []
  db['paid'] = 0
  print("All items reset.")
  exit(0)

itemList = db['itemList']
paid = db['paid']

@app.route("/")
@app.route("/home")
def home():
  total=0
  for item in db['itemList']:
    total+=float(item[1])

  return render_template('home.html', title = "Home page", items=db['itemList'][::-1], total=floatToMoney(total), owed=floatToMoney(float(total-db['paid'])), paid=floatToMoney(db['paid']))

@app.route("/add-item", methods=["GET", "POST"])
def addItem():
  form = AddItemForm()
  if form.validate_on_submit():

    print(form.price.data)
    print(form.title.data)

    currentDate = datetime.datetime.now()
    dateToDisplay = str(currentDate.strftime("%m-%d-%Y"))
    id = len(db['itemList']) + 1

    db['itemList'].append([str(form.title.data), floatToMoney(form.price.data), dateToDisplay, id])
    flash("Success! Item has been added.", 'success')
    return redirect(url_for("home"))

  return render_template('add_item.html', title = "Add Item", form=form)

@app.route("/log_entry/<int:id>")
def entryPage(id):
  return render_template('postPage.html', title="Post", post = db['itemList'][id-1])

@app.route("/log_entry/<int:id>/delete")
def deleteEntry(id):
  db['itemList'].pop(id-1)
  for item in db['itemList']:
    if item[3] > id:
      item[3] -= 1
  flash("The list entry has been deleted successfully.", 'success')
  return redirect(url_for("home"))

@app.route("/log_entry/<int:id>/update", methods=["GET", "POST"])
def updateEntry(id):
  form = EditItemForm()
  entry = db['itemList'][id-1]
  if form.validate_on_submit():
    # print(form.price.data)
    # print(form.title.data)
    # print(form.date.data.strftime("%m-%d-%Y"))
    if form.title.data:
      entry[0] = form.title.data
    if form.price.data:
      entry[1] = floatToMoney(float(form.price.data))
    if form.date.data:
      entry[2] = form.date.data.strftime("%m-%d-%Y")
    flash("Listing edited successfully!", "success")
    return redirect(url_for("home"))
  return render_template('edit_item.html', form=form, title="Update Log Entry")

@app.route('/add-paid-money', methods = ["GET", "POST"])
def addPaidMoney():
  form = AddPaidMoneyForm()
  if form.validate_on_submit():
    print(db['paid'])
    print(form.amount.data)
    db['paid']+=float(form.amount.data)
    flash("Success!", 'success')
    return redirect(url_for('home'))
  return render_template('add_paid_money.html', title='Add Paid Money', form=form)

@app.route('/prices')
def prices():
  return render_template('prices.html', title='Prices')
app.run(host='0.0.0.0', port=8080, debug=True)
