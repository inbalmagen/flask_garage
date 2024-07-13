from flask import Flask, redirect, render_template, request, url_for

users = [{"name": "inbal", "password": "111"}]
    
    # {"name": "dor", "password": "222"}
    # {"name": "danielle", "password": "333"}     
         

app = Flask(__name__)

car1 = {"id": "1", "number": "111-111", "urgent": True, "problems": ["gear", "breaks"], "image": "https://res.cloudinary.com/midrag/image/upload/c_scale,w_1400,q_auto,f_auto/Cms/gzxece10vhxs6sm7gy7x.jpg"}
car2 = {"id": "2", "number": "222-222", "urgent": True,"problems": ["gear", "engine"], "image": "https://pic1.calcalist.co.il/PicServer3/2017/02/12/702870/CAL0308656_l.jpg"}
car3 = {"id": "3", "number": "333-333", "urgent": False, "problems": ["engine", "breaks"], "image": "https://www.hon.co.il/wp-content/uploads/2019/04/asfanut.jpg"}
car4 = {"id": "4", "number": "444-444", "urgent": True, "problems": ["gear", "breaks"], "image": "https://thecar.co.il/wp-content/uploads/2018/01/PHOTOS-by-Noam-Wind_119-1024x683.jpg"}
car5 = {"id": "5", "number": "555-555", "urgent": False, "problems": ["gear", "engine"], "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5XHl_vUEcJpjEUQCOVcwQrEd-Uxx5T8Msdw&s"}
car6 = {"id": "6", "number": "666-666", "urgent": False, "problems": ["engine", "breaks"], "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSdCszi23Ry3hTlhVcYkpp_KEVwgOWnObBFwg&s"}
cars = [car1, car2, car3, car4, car5, car6]

@app.route("/")
def cars_list():
    # Get filters from query parameters
    problem_filter = request.args.get('problem', '').lower()
    urgent = request.args.get('urgent', '')
    search = request.args.get('search', '').lower()

    filtered_cars = cars

    # Apply problem filter
    if problem_filter:
        filtered_cars = [car for car in filtered_cars if problem_filter in car.get('problems', [])]

    # Apply urgent filter
    if urgent == "true":
        filtered_cars = [car for car in filtered_cars if car.get('urgent')]

    # Apply search filter
    if search:
        filtered_cars = [car for car in filtered_cars if search in car['number'].lower() or any(search in problem.lower() for problem in car.get('problems', []))]

    return render_template("car_list.html", car_list=filtered_cars)

# @app.route("/login/", methods=["POST", "GET"])
# def login():  
#     if request.method == "POST":

#         return render_template("login.html")

# @app.route("/profile")
# def profile():
#     return render_template("profile.html")


# @app.route("/")
# def cars_list():
#     # handling problem filter
#     problem_filter = request.args.get('problem','').lower()
#     if problem_filter:
#         filtered_cars = []
#         for car in cars:
#             if problem_filter in car.get('problems',[]):
#                 filtered_cars.append(car)
#     else:
#         filtered_cars = cars  # Return all cars if no problem filter is requested

#     # handling urgent after problem filter
#     urgent = request.args.get('urgent','')
#     if urgent == "true":
#         new_cars = [car for car in filtered_cars if car.get('urgent')]
#     else:
#         new_cars = filtered_cars

    # return render_template("car_list.html", car_list=new_cars)

    
@app.route("/single_car/<id>")
def single_car(id):
    for car in cars:
         if car["id"] == id: #if you have found this id → return ↓
            return render_template("single_car.html", car=car) #else, return ↓
    return render_template("single_car.html", car=None) #can go to "error_page.html"


@app.route("/add_car/")
def add_car():
    print("****** Adding car")
    return render_template("add_car.html")

@app.route("/add_to_list/", methods=["POST", "GET"])
def add_to_list():
     if request.method == "POST":
        cNumber = request.form.get("cNumber")
        cId = request.form.get("cId")
        cProblems = request.form.get("cProblems")
        cURL = request.form.get("cURL")
        print("****** Adding to list", cNumber, cId, cProblems, cURL)
        return f"Added to list: {cNumber}, {cId}, {cProblems}, {cURL}"

@app.route("/delete_car/<id>", methods=["POST"])
def delete_car(id):
    global cars
    cars = [car for car in cars if car["id"] != id]
    return redirect(url_for('cars_list'))

@app.route("/edit_car/<id>")
def edit_car(id):
    car_to_edit = None
    for car in cars:
        if car["id"] == id:
            car_to_edit = car
            break
    if car_to_edit:
        return render_template("edit_car.html", car=car_to_edit)
    return redirect(url_for('cars_list'))

@app.route("/update_car/<id>", methods=["POST"])
def update_car(id):
    for car in cars:
        if car["id"] == id:
            car["number"] = request.form.get("cNumber")
            car["urgent"] = request.form.get("cUrgent") == "true"
            car["problems"] = request.form.get("cProblems").split(',')
            car["image"] = request.form.get("cURL")
            break
    return redirect(url_for('cars_list'))

@app.route("/login/", methods=["POST", "GET"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        for user in users:
            if user.get("name") == username and user.get("password") == password:
                print("logged in!")
                return redirect("/")
        message = "Problem in username or password"
        print("POST!!!!!!!!!! got:", username, password)
    else:
        print("GET!!!!!!!!")

    return render_template("login.html", message=message)
    
   
if __name__ == "__main__":
    app.run(debug=True, port=9000)
