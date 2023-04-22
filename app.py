from flask import Flask, render_template, request, redirect, url_for, flash
from resources.tracker import Medicine

app = Flask(__name__)
app.secret_key = "i like secret toasty keys"
tracker = Medicine()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    message = request.args.get("message")
    if request.method == "GET":
        tracker.update_quantity()
        return render_template("dashboard.html", data=tracker.dashboard_info(), message = message)

    elif request.method == "POST":
        try:
            message = ""
            name = request.form.get("name")
            old_name = request.form.get("oldname")
            quantity = request.form.get("quantity")
            addquantity = request.form.get("addquantity")
            modifier = request.form.get("modifier")
            type = request.form.get("type")

            if type == "edit":
                quantity = float(quantity) + float(addquantity)
                message += "\n" + tracker.medicine_quantity(name, float(quantity))
                message += "\n" + tracker.change_modifier(name, float(modifier))
                if old_name != name:
                    message = "\n" + tracker.change_name(old_name, name)

            elif type == "delete":
                message = tracker.delete_medicine(name)
            
            elif type == "add":
                message = tracker.add_new(name.upper(), float(quantity), float(modifier))

            return redirect(url_for("dashboard", message=message))
        
        except:
            message = "Could not update. Unknown error"
            return redirect(url_for("dashboard", message=message))

if __name__ == "__main__":
    app.run(debug=True)
