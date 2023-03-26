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
    if request.method == "GET":
        return render_template("dashboard.html", data=tracker.dashboard_info())

    elif request.method == "POST":
        try:
            name = request.form.get("name")
            quantity = request.form.get("quantity")
            modifier = request.form.get("modifier")
            type = request.form.get("type")

            if type == "edit":
                tracker.medicine_quantity(name, int(quantity))
                tracker.change_modifier(name, int(modifier))

            elif type == "delete":
                tracker.delete_medicine(name)
            
            elif type == "add":
                tracker.add_new(name.upper(), int(quantity), int(modifier))

            return redirect(url_for("dashboard"))
        
        except:
            return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)