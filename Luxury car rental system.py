import pandas as pd
import matplotlib.pyplot as plt
import os

# --- File paths (use the files you uploaded) ---
USERS_CSV = "Users.csv"
MEMBERS_CSV = "Members.csv"
CARS_CSV = "Cars.csv"
CARS_BOOKED_CSV = "Cars Booked.csv"
RETURNED_CARS_CSV = "Returned Cars.csv"

# --- Expected headers (match your uploaded CSVs) ---
USERS_COLS = ["User ID", "User Name", "Password"]
MEMBERS_COLS = ["MID", "M Name", "Phone No.", "No. of cars Booked"]
CARS_COLS = ["Car No.", "Car Name", "Brand", "Branch", "Fuel Type", "Cost", "Category"]
CARS_BOOKED_COLS = ["Car Name", "M Name", "Date of Booking", "No. of Days", "Total Cost", "Return Status"]
RETURNED_COLS = ["Car Name", "M Name", "Date of Booking", "No. of Days", "Total Cost", "Return Date"]

def ensure_csv(path, cols):
    """Create CSV with header if file missing or empty."""
    if not os.path.exists(path):
        df = pd.DataFrame(columns=cols)
        df.to_csv(path, index=False)
    else:
        try:
            df = pd.read_csv(path)
            # If file exists but has no columns / empty, re-create header
            if df.shape[1] == 0:
                pd.DataFrame(columns=cols).to_csv(path, index=False)
        except pd.errors.EmptyDataError:
            pd.DataFrame(columns=cols).to_csv(path, index=False)

# Ensure all required CSV files exist
ensure_csv(USERS_CSV, USERS_COLS)
ensure_csv(MEMBERS_CSV, MEMBERS_COLS)
ensure_csv(CARS_CSV, CARS_COLS)
ensure_csv(CARS_BOOKED_CSV, CARS_BOOKED_COLS)
ensure_csv(RETURNED_CARS_CSV, RETURNED_COLS)

print("---------------------------WELCOME TO LUXURY CAR RENTALS---------------------------")

# ----------------------------- Utility helpers -----------------------------
def read_csv_safe(path, expected_cols):
    """Read CSV and ensure expected columns exist (return DataFrame)."""
    df = pd.read_csv(path)
    # Add missing expected columns (keep existing columns and order expected where possible)
    for c in expected_cols:
        if c not in df.columns:
            df[c] = ""
    # Reorder to expected cols + extra columns (preserve expected order)
    cols = [c for c in expected_cols if c in df.columns] + [c for c in df.columns if c not in expected_cols]
    return df[cols]

def save_df_safe(df, path, expected_cols=None):
    """Save dataframe to csv. If expected_cols provided, ensure those columns exist and are first."""
    if expected_cols:
        for c in expected_cols:
            if c not in df.columns:
                df[c] = ""
        cols = [c for c in expected_cols if c in df.columns] + [c for c in df.columns if c not in expected_cols]
        df = df[cols]
    df.to_csv(path, index=False)

# ----------------------------- User functions -----------------------------
def addUser():
    uid = input("Enter User ID: ").strip()
    uname = input("Enter User Name: ").strip()
    pwd = input("Enter Password: ").strip()
    udf = read_csv_safe(USERS_CSV, USERS_COLS)
    # Prevent duplicate User ID
    if (udf["User ID"] == uid).any():
        print("A user with that User ID already exists.")
        return
    udf.loc[len(udf)] = [uid, uname, pwd]
    save_df_safe(udf, USERS_CSV, USERS_COLS)
    print("User added successfully")
    print(udf)

def deleteUser():
    uid = input("Enter a User ID: ").strip()
    udf = read_csv_safe(USERS_CSV, USERS_COLS)
    udf = udf[udf["User ID"] != uid]
    save_df_safe(udf, USERS_CSV, USERS_COLS)
    print("User deleted successfully")
    print(udf)

# ----------------------------- Cars -----------------------------
def addNewCar():
    try:
        carno = int(input("Enter a Car Number: ").strip())
    except ValueError:
        print("Car Number must be an integer.")
        return
    carname = input("Enter Name of the Car: ").strip()
    brand = input("Enter brand of the Car: ").strip()
    branch = input("Enter branch: ").strip()
    fueltype = input("Enter fuel type of the car: ").strip()
    try:
        cost = int(input("Enter cost of rent per day: ").strip())
    except ValueError:
        print("Cost must be an integer.")
        return
    category = input("Enter category of the car: ").strip()

    cdf = read_csv_safe(CARS_CSV, CARS_COLS)
    if (cdf["Car No."] == carno).any() or (cdf["Car Name"] == carname).any():
        print("A car with the same number or name already exists.")
        return
    cdf.loc[len(cdf)] = [carno, carname, brand, branch, fueltype, cost, category]
    save_df_safe(cdf, CARS_CSV, CARS_COLS)
    print("Car added successfully!")

def searchCar():
    carname = input("Enter a Car name: ").strip()
    cdf = read_csv_safe(CARS_CSV, CARS_COLS)
    df = cdf.loc[cdf["Car Name"].astype(str) == carname]
    if df.empty:
        print("No cars found with the given name")
    else:
        print("Car details are:")
        print(df)

def deleteCar():
    try:
        carno = int(input("Enter a car number: ").strip())
    except ValueError:
        print("Car Number must be an integer.")
        return
    cdf = read_csv_safe(CARS_CSV, CARS_COLS)
    cdf = cdf[cdf["Car No."] != carno]
    save_df_safe(cdf, CARS_CSV, CARS_COLS)
    print("Car Deleted Successfully")
    print(cdf)

def showCars():
    print(read_csv_safe(CARS_CSV, CARS_COLS))

# ----------------------------- Members -----------------------------
def addNewMember():
    try:
        mid = int(input("Enter a member id: ").strip())
    except ValueError:
        print("Member ID must be an integer.")
        return
    mname = input("Enter member name: ").strip()
    try:
        phoneno = input("Enter phone number: ").strip()
    except ValueError:
        print("Invalid phone number.")
        return
    mdf = read_csv_safe(MEMBERS_CSV, MEMBERS_COLS)
    if (mdf["MID"] == mid).any():
        print("Member with this MID already exists.")
        return
    mdf.loc[len(mdf)] = [mid, mname, phoneno, 0]
    save_df_safe(mdf, MEMBERS_CSV, MEMBERS_COLS)
    print("New Member added successfully!")
    print(mdf)

def searchMember():
    mname = input("Enter a member name: ").strip()
    mdf = read_csv_safe(MEMBERS_CSV, MEMBERS_COLS)
    df = mdf.loc[mdf["M Name"].astype(str) == mname]
    if df.empty:
        print("No members found with the given name")
    else:
        print("Member details are:")
        print(df)

def deleteMember():
    try:
        mid = int(input("Enter a member id: ").strip())
    except ValueError:
        print("Member ID must be an integer.")
        return
    mdf = read_csv_safe(MEMBERS_CSV, MEMBERS_COLS)
    mdf = mdf[mdf["MID"] != mid]
    save_df_safe(mdf, MEMBERS_CSV, MEMBERS_COLS)
    print("Member deleted successfully")
    print(mdf)

def showMembers():
    print(read_csv_safe(MEMBERS_CSV, MEMBERS_COLS))

# ----------------------------- Booking -----------------------------
def bookCar():
    carname = input("Enter car name: ").strip()
    cdf = read_csv_safe(CARS_CSV, CARS_COLS)
    car = cdf.loc[cdf["Car Name"].astype(str) == carname]
    if car.empty:
        print("No Car found in the records")
        return

    mname = input("Enter member name: ").strip()
    mdf = read_csv_safe(MEMBERS_CSV, MEMBERS_COLS)
    member = mdf.loc[mdf["M Name"].astype(str) == mname]
    if member.empty:
        print("No such Member found")
        return

    dateofbooking = input("Enter date of booking (e.g. 2025-11-19): ").strip()
    try:
        numberofdays = int(input("Enter the number of days booked: ").strip())
    except ValueError:
        print("Number of days must be an integer.")
        return

    # get cost as scalar
    cost_val = int(car.iloc[0]["Cost"])
    total_cost = numberofdays * cost_val

    print("^" * 40)
    print("      BILL GENERATED   ")
    print("^" * 40)
    print("Car Rented:", carname)
    print("Name of Member:", mname)
    print("Cost per Day:", cost_val)
    print("Total Rental Cost:", total_cost)
    print("^" * 40)

    bdf = read_csv_safe(CARS_BOOKED_CSV, CARS_BOOKED_COLS)
    bdf.loc[len(bdf)] = [carname, mname, dateofbooking, numberofdays, total_cost, ""]
    save_df_safe(bdf, CARS_BOOKED_CSV, CARS_BOOKED_COLS)

    # update member's "No. of cars Booked"
    idx = mdf[mdf["M Name"].astype(str) == mname].index
    if not idx.empty:
        i = idx[0]
        try:
            mdf.at[i, "No. of cars Booked"] = int(mdf.at[i, "No. of cars Booked"]) + 1
        except Exception:
            mdf.at[i, "No. of cars Booked"] = 1
        save_df_safe(mdf, MEMBERS_CSV, MEMBERS_COLS)

    print("Car booked successfully")
    print(read_csv_safe(CARS_BOOKED_CSV, CARS_BOOKED_COLS))

def returnCar():
    mname = input("Enter member name: ").strip()
    carname = input("Enter car name: ").strip()
    rdf = read_csv_safe(CARS_BOOKED_CSV, CARS_BOOKED_COLS)

    mask = (rdf["Car Name"].astype(str) == carname) & (rdf["M Name"].astype(str) == mname)
    matched = rdf[mask]
    if matched.empty:
        print("No such booking found")
        return

    print("Booking found:")
    print(matched)
    ans = input("Are you sure you want to return the car (yes/no)? ").strip().lower()
    if ans != "yes":
        print("Return operation cancelled")
        return

    return_date = input("Enter return date (e.g. 2025-11-20): ").strip()

    # Append the matched rows to Returned Cars CSV with Return Date
    returned_df = read_csv_safe(RETURNED_CARS_CSV, RETURNED_COLS)
    for _, row in matched.iterrows():
        returned_df.loc[len(returned_df)] = [
            row["Car Name"],
            row["M Name"],
            row["Date of Booking"],
            row["No. of Days"],
            row["Total Cost"],
            return_date
        ]
    save_df_safe(returned_df, RETURNED_CARS_CSV, RETURNED_COLS)

    # Remove the bookings from Cars Booked CSV
    rdf = rdf[~mask]
    save_df_safe(rdf, CARS_BOOKED_CSV, CARS_BOOKED_COLS)

    # decrement member's No. of cars Booked
    mdf = read_csv_safe(MEMBERS_CSV, MEMBERS_COLS)
    idx = mdf[mdf["M Name"].astype(str) == mname].index
    if not idx.empty:
        i = idx[0]
        try:
            newval = int(mdf.at[i, "No. of cars Booked"]) - 1
            mdf.at[i, "No. of cars Booked"] = max(0, newval)
        except Exception:
            mdf.at[i, "No. of cars Booked"] = 0
        save_df_safe(mdf, MEMBERS_CSV, MEMBERS_COLS)

    print("Car returned successfully and moved to", RETURNED_CARS_CSV)

# ----------------------------- Show / Delete Booked -----------------------------
def showbookedCars():
    rdf = read_csv_safe(CARS_BOOKED_CSV, CARS_BOOKED_COLS)
    if rdf.empty:
        print("No active bookings.")
        return
    print(rdf)
    print("^" * 50)
    print("Car Name\tMember Name\tBill Amount")
    for _, r in rdf.iterrows():
        print(f"{r['Car Name']}\t{r['M Name']}\t{r['Total Cost']}")
    print("^" * 50)

def deletebookedCars():
    carname = input("Enter a car name: ").strip()
    bdf = read_csv_safe(CARS_BOOKED_CSV, CARS_BOOKED_COLS)
    before = len(bdf)
    bdf = bdf[bdf["Car Name"].astype(str) != carname]
    save_df_safe(bdf, CARS_BOOKED_CSV, CARS_BOOKED_COLS)
    print(f"Deleted {before - len(bdf)} booked entries for car '{carname}'")
    print(bdf)

# ----------------------------- Charts -----------------------------
def showCharts():
    print("Press 1 - Cars and their Rental Cost")
    print("Press 2 - Number of Cars booked by members")
    ch = input("Enter your choice: ").strip()
    if ch == "1":
        df = read_csv_safe(CARS_CSV, CARS_COLS)
        if df.empty:
            print("No car data to plot.")
            return
        df.plot(x="Car Name", y="Cost", kind="bar")
        plt.xlabel("Car Name")
        plt.ylabel("Cost per day")
        plt.show()
    elif ch == "2":
        df = read_csv_safe(CARS_BOOKED_CSV, CARS_BOOKED_COLS)
        if df.empty:
            print("No booking data to plot.")
            return
        counts = df.groupby("M Name").size().sort_values(ascending=False)
        counts.plot(kind="bar")
        plt.xlabel("Member Name")
        plt.ylabel("Number of Active Bookings")
        plt.show()
    else:
        print("Invalid choice for charts.")

# ----------------------------- Login & Menu -----------------------------
def login():
    uid = input("Enter User ID: ").strip().lower()
    uname = input("Enter User Name: ").strip().lower()
    pwd = input("Enter Password: ").strip().lower()

    df = read_csv_safe(USERS_CSV, USERS_COLS)

    # Convert CSV values to lowercase for case-insensitive comparison
    df["uid_lower"] = df["User ID"].astype(str).str.strip().str.lower()
    df["uname_lower"] = df["User Name"].astype(str).str.strip().str.lower()
    df["pwd_lower"] = df["Password"].astype(str).str.strip().str.lower()

    user = df[
        (df["uid_lower"] == uid) &
        (df["uname_lower"] == uname) &
        (df["pwd_lower"] == pwd)
    ]

    if user.empty:
        print("Invalid login credentials")
        return False

    print("Login Successful!")
    return True


def showMenu():
    print("----------------------------------------------------------------------------------------")
    print("                               LUXURY CAR RENTALS                                       ")
    print("----------------------------------------------------------------------------------------")
    print("1 - Add a User")
    print("2 - Delete a User")
    print("3 - Add a New Car")
    print("4 - Search for a Car")
    print("5 - Delete a Car")
    print("6 - Show all Cars")
    print("7 - Add a New Member")
    print("8 - Search for a Member")
    print("9 - Delete a Member")
    print("10 - Show all Members")
    print("11 - Book a Car")
    print("12 - Return a Car")
    print("13 - Show all Booked Cars")
    print("14 - Delete a Booked Car")
    print("15 - View Charts")
    print("16 - Exit")
    try:
        return int(input("Enter your choice: ").strip())
    except ValueError:
        return -1

# ----------------------------- Main loop -----------------------------
if login():
    while True:
        ch = showMenu()
        if ch == 1:
            addUser()
        elif ch == 2:
            deleteUser()
        elif ch == 3:
            addNewCar()
        elif ch == 4:
            searchCar()
        elif ch == 5:
            deleteCar()
        elif ch == 6:
            showCars()
        elif ch == 7:
            addNewMember()
        elif ch == 8:
            searchMember()
        elif ch == 9:
            deleteMember()
        elif ch == 10:
            showMembers()
        elif ch == 11:
            bookCar()
        elif ch == 12:
            returnCar()
        elif ch == 13:
            showbookedCars()
        elif ch == 14:
            deletebookedCars()
        elif ch == 15:
            showCharts()
        elif ch == 16:
            break
        else:
            print("Invalid Option Selected")
print("THANK YOU FOR VISITING LUXURY CAR RENTALS")


// Load car gallery dynamically
const cars = [
    { name: 'Lamborghini Huracan', image: 'https://images.unsplash.com/photo-1544829099-b9a0e3421cfb?w=400', price: '$500/day' },
    { name: 'Ferrari 488', image: 'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=400', price: '$600/day' },
    { name: 'Rolls-Royce Ghost', image: 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400', price: '$800/day' },
    { name: 'Bentley Continental', image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', price: '$700/day' }
];

const gallery = document.getElementById('car-gallery');
cars.forEach(car => {
    const card = `
        <div class="col-md-3 mb-4">
            <div class="card">
                <img src="${car.image}" class="card-img-top" alt="${car.name}">
                <div class="card-body">
                    <h5 class="card-title">${car.name}</h5>
                    <p class="card-text">${car.price}</p>
                    <a href="#booking" class="btn btn-gold">Book Now</a>
                </div>
            </div>
        </div>
    `;
    gallery.innerHTML += card;
});

// Handle booking form submission
document.getElementById('booking-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const car = document.getElementById('car').value;
    const date = document.getElementById('date').value;
    
    if (name && email && car && date) {
        document.getElementById('booking-message').innerHTML = `<div class="alert alert-success">Thank you, ${name}! Your booking for ${car} on ${date} has been submitted. We'll contact you at ${email} soon.</div>`;
        this.reset();
    } else {
        document.getElementById('booking-message').innerHTML = `<div class="alert alert-danger">Please fill in all fields.</div>`;
    }
});

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Luxury Car Rental — Book Your Ride</title>

  <!-- Bootstrap 5 CSS (CDN) -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- Font Awesome for icons -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">

  <!-- Custom styles -->
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
  <!-- NAVBAR -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <i class="fas fa-car-side me-2 brand-icon"></i>
        Luxury Car Rental
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navCollapse">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="navCollapse" class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><a class="nav-link active" href="#cars">Cars</a></li>
          <li class="nav-item"><a class="nav-link" href="#how">How it works</a></li>
          <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
          <li class="nav-item"><a class="btn btn-outline-light ms-2" href="#cars">Book now</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- HERO -->
  <header class="hero bg-image text-white d-flex align-items-center">
    <div class="container text-center py-6">
      <h1 class="display-5 fw-bold">Drive the dream today.</h1>
      <p class="lead mb-4">Premium cars, transparent pricing, white-glove service.</p>
      <a href="#cars" class="btn btn-lg btn-primary me-2">Browse cars</a>
      <a href="#how" class="btn btn-lg btn-outline-light">How it works</a>
    </div>
  </header>

  <!-- FEATURES -->
  <section id="how" class="py-5">
    <div class="container">
      <div class="row text-center g-4">
        <div class="col-md-4">
          <div class="feature p-4 shadow-sm rounded">
            <i class="fa-solid fa-calendar-check fa-2x mb-3 text-primary"></i>
            <h5>Easy booking</h5>
            <p class="mb-0">Reserve in seconds with our intuitive booking flow.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="feature p-4 shadow-sm rounded">
            <i class="fa-solid fa-shield-halved fa-2x mb-3 text-primary"></i>
            <h5>Fully insured</h5>
            <p class="mb-0">Comprehensive coverage for all rentals and add-ons.</p>
          </div>
        </div>
        <div class="col-md-4">
          <div class="feature p-4 shadow-sm rounded">
            <i class="fa-solid fa-wrench fa-2x mb-3 text-primary"></i>
            <h5>24/7 support</h5>
            <p class="mb-0">White-glove concierge available around the clock.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CARS GRID -->
  <section id="cars" class="py-5 bg-light">
    <div class="container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="h3 mb-0">Available Cars</h2>
        <div>
          <small class="text-muted">Sort:</small>
          <select id="sortSelect" class="form-select d-inline-block w-auto ms-2">
            <option value="popular">Most popular</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
          </select>
        </div>
      </div>

      <div id="carsGrid" class="row g-4">
        <!-- Car card example (repeat/inject for each car) -->
        <div class="col-md-6 col-lg-4">
          <div class="card shadow-sm h-100">
            <img src="https://images.unsplash.com/photo-1542367597-59cc3f5b0f45?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" class="card-img-top" alt="Mercedes S-Class">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">Mercedes S-Class</h5>
              <p class="card-text text-muted">Luxury sedan — 5 seats, automatic</p>
              <div class="mt-auto d-flex justify-content-between align-items-center">
                <div>
                  <span class="h5 mb-0">$250</span>
                  <small class="text-muted">/ day</small>
                </div>
                <div>
                  <button class="btn btn-primary btn-book" data-name="Mercedes S-Class" data-price="250">Book</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card shadow-sm h-100">
            <img src="https://images.unsplash.com/photo-1549923746-c502d488b3ea?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" class="card-img-top" alt="BMW 7 Series">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">BMW 7 Series</h5>
              <p class="card-text text-muted">Executive performance — 5 seats</p>
              <div class="mt-auto d-flex justify-content-between align-items-center">
                <div>
                  <span class="h5 mb-0">$230</span>
                  <small class="text-muted">/ day</small>
                </div>
                <div>
                  <button class="btn btn-primary btn-book" data-name="BMW 7 Series" data-price="230">Book</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6 col-lg-4">
          <div class="card shadow-sm h-100">
            <img src="https://images.unsplash.com/photo-1603898037225-6b39b0b9e02a?q=80&w=1200&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" class="card-img-top" alt="Porsche Cayenne">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">Porsche Cayenne</h5>
              <p class="card-text text-muted">Sport SUV — 5 seats, AWD</p>
              <div class="mt-auto d-flex justify-content-between align-items-center">
                <div>
                  <span class="h5 mb-0">$320</span>
                  <small class="text-muted">/ day</small>
                </div>
                <div>
                  <button class="btn btn-primary btn-book" data-name="Porsche Cayenne" data-price="320">Book</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Add more car cards as needed -->
      </div>
    </div>
  </section>

  <!-- CONTACT / FOOTER -->
  <footer id="contact" class="py-5 bg-dark text-white">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <h5>Contact</h5>
          <p class="text-muted">Email: hello@luxurycarrental.example • Phone: +1 (555) 123-4567</p>
        </div>
        <div class="col-md-6 text-md-end">
          <p class="mb-0">&copy; <span id="yr"></span> Luxury Car Rental. All rights reserved.</p>
        </div>
      </div>
    </div>
  </footer>

  <!-- BOOKING MODAL -->
  <div class="modal fade" id="bookingModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <form id="bookingForm" class="modal-content needs-validation" novalidate>
        <div class="modal-header">
          <h5 class="modal-title">Book vehicle</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Car</label>
            <input id="carName" class="form-control" readonly>
          </div>
          <div class="row g-2 mb-3">
            <div class="col">
              <label class="form-label">Start</label>
              <input id="startDate" type="date" class="form-control" required>
            </div>
            <div class="col">
              <label class="form-label">End</label>
              <input id="endDate" type="date" class="form-control" required>
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Full name</label>
            <input id="fullName" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input id="email" type="email" class="form-control" required>
          </div>

          <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
              <strong>Total:</strong> <span id="totalPrice" class="h5">$0</span>
            </div>
            <div>
              <small class="text-muted" id="priceNote">Price per day: $0</small>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button type="submit" class="btn btn-primary">Confirm booking</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Bootstrap 5 JS + Popper (CDN) -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

  <!-- Custom JS -->
  <script src="js/scripts.js"></script>
</body>
</html>




