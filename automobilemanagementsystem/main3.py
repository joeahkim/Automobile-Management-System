import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from PIL import Image, ImageTk
from io import BytesIO


def display_vehicle_inventory():
    # Function to display vehicle inventory in the main panel
    global data_frame_filled

    # Clear the data frame before populating it
    for widget in data_frame.winfo_children():
        widget.destroy()

    if not data_frame_filled:
        mycursor.execute(
            "SELECT image, vehicle_name, model, retail_price, transmission, days_in_stock, location FROM vehicles")
        vehicles = mycursor.fetchall()

        for vehicle in vehicles:
            image_data = vehicle[0]
            image = Image.open(BytesIO(image_data))
            image = image.resize((100, 100), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)
            # Keep reference to the image to prevent garbage collection
            image_references.append(image)

            # Display vehicle data in labels
            vehicle_frame = tk.Frame(data_frame, bg="white")
            vehicle_frame.pack(fill="x", padx=10, pady=5)

            vehicle_image_label = tk.Label(vehicle_frame, image=image)
            vehicle_image_label.image = image  # Keep a reference to the image
            vehicle_image_label.pack(side="left", padx=10)

            vehicle_details = vehicle[1:]
            for detail in vehicle_details:
                detail_label = tk.Label(vehicle_frame, text=detail, bg="white",
                                        font=("Arial", 12))  # Increase font size
                detail_label.pack(side="left", padx=10)

        data_frame_filled = True

    # Reset the data_frame_filled flag
    data_frame_filled = False


def search_pan():
    # Function to toggle the visibility of left_panel_2
    if left_panel_2.winfo_ismapped():
        left_panel_2.grid_remove()
    else:
        left_panel_2.grid(row=1, column=1, sticky="ns")
        left_panel_2.config(height=400)


def update_car_models(*args):
    selected_car_type = car_type_var.get()
    car_models = car_type_models.get(selected_car_type, [])
    car_model_var.set("")
    car_model_combobox['values'] = car_models


def show_login_window():
    # Function to display the login window
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.resizable(False, False)
    # Disable interaction with the main window
    login_window.grab_set()

    username_label = ttk.Label(login_window, text="Username:")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(login_window)
    username_entry.pack(pady=5)

    password_label = ttk.Label(login_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    def login():
        # Function to check login credentials
        username = username_entry.get()
        password = password_entry.get()

        # Query to check user credentials
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        mycursor.execute(query, (username, password))
        user = mycursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            login_window.destroy()
            # After successful login, display user input form
            add_record_window = tk.Toplevel(root)
            add_record_window.title("Add Record")
            add_record_window.geometry("400x600")
            add_record_window.resizable(False, True)

            # Disable interaction with the main window
            add_record_window.grab_set()

            # Image selection
            def select_image():
                file_path = filedialog.askopenfilename(filetypes=(("Image files", "*.jpg;*.png;*.jpeg"), ("All files", "*.*")))
                image_entry.delete(0, tk.END)
                image_entry.insert(0, file_path)

            ttk.Label(add_record_window, text="Vehicle Image:").pack(pady=5)
            image_entry = ttk.Entry(add_record_window)
            image_entry.pack(pady=5)
            ttk.Button(add_record_window, text="Select Image", command=select_image).pack(pady=5)

            # Other entries
            ttk.Label(add_record_window, text="Vehicle Name:").pack(pady=5)
            vehicle_name_entry = ttk.Entry(add_record_window)
            vehicle_name_entry.pack(pady=5)

            ttk.Label(add_record_window, text="Model:").pack(pady=5)
            model_entry = ttk.Entry(add_record_window)
            model_entry.pack(pady=5)

            ttk.Label(add_record_window, text="Retail Price:").pack(pady=5)
            retail_price_entry = ttk.Entry(add_record_window)
            retail_price_entry.pack(pady=5)

            ttk.Label(add_record_window, text="Transmission:").pack(pady=5)
            transmission_entry = ttk.Entry(add_record_window)
            transmission_entry.pack(pady=5)

            ttk.Label(add_record_window, text="Days in Stock:").pack(pady=5)
            days_in_stock_entry = ttk.Entry(add_record_window)
            days_in_stock_entry.pack(pady=5)

            ttk.Label(add_record_window, text="Location:").pack(pady=5)
            location_entry = ttk.Entry(add_record_window)
            location_entry.pack(pady=5)

            def add_record():
                # Function to add a record to the database
                vehicle_name = vehicle_name_entry.get()
                model = model_entry.get()
                retail_price = retail_price_entry.get()
                transmission = transmission_entry.get()
                days_in_stock = days_in_stock_entry.get()
                location = location_entry.get()

                # Read image file
                image_path = image_entry.get()
                if image_path:
                    with open(image_path, "rb") as file:
                        image_data = file.read()
                else:
                    image_data = None

                query = "INSERT INTO vehicles (image, vehicle_name, model, retail_price, transmission, days_in_stock, location) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (image_data, vehicle_name, model, retail_price, transmission, days_in_stock, location)

                try:
                    mycursor.execute(query, values)
                    mydb.commit()
                    messagebox.showinfo("Success", "Record added successfully!")
                    # Clear entry fields
                    vehicle_name_entry.delete(0, tk.END)
                    model_entry.delete(0, tk.END)
                    retail_price_entry.delete(0, tk.END)
                    transmission_entry.delete(0, tk.END)
                    days_in_stock_entry.delete(0, tk.END)
                    location_entry.delete(0, tk.END)
                    image_entry.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error occurred: {err}")

            # Add record button
            ttk.Button(add_record_window, text="Add Record", command=add_record).pack(pady=10)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    ttk.Button(login_window, text="Login", command=login).pack(pady=10)


def logout():
    # Logout logic
    global logged_in  # Access the global variable
    logged_in = False  # Update the login status
    header_icon.config(image=user_icon)


# Create search button in left panel 2
def search():
    selected_car_model = car_model_var.get()
    selected_price_range = price_var.get()
    selected_location = location_var.get()

    # Extracting price range limits
    price_range_limits = selected_price_range.split("-")
    min_price = int(price_range_limits[0].replace("ksh", "").replace(",", ""))
    max_price = int(price_range_limits[1].replace("ksh", "").replace(",", ""))

    # Formulating the SQL query
    query = "SELECT image, vehicle_name, model, retail_price, transmission, days_in_stock, location " \
            "FROM vehicles WHERE vehicle_name = %s AND retail_price >= %s AND retail_price <= %s AND location = %s"
    mycursor.execute(query, (selected_car_model, min_price, max_price, selected_location))
    vehicles = mycursor.fetchall()

    # Clearing previous data
    for widget in data_frame.winfo_children():
        widget.destroy()

    for vehicle in vehicles:
        image_data = vehicle[0]
        image = Image.open(BytesIO(image_data))
        image = image.resize((100, 100), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        # Keep reference to the image to prevent garbage collection
        image_references.append(image)

        # Display vehicle data in labels
        vehicle_frame = tk.Frame(data_frame, bg="white")
        vehicle_frame.pack(fill="x", padx=10, pady=5)

        vehicle_image_label = tk.Label(vehicle_frame, image=image)
        vehicle_image_label.image = image  # Keep a reference to the image
        vehicle_image_label.pack(side="left", padx=10)

        vehicle_details = vehicle[1:]
        for detail in vehicle_details:
            detail_label = tk.Label(vehicle_frame, text=detail, bg="white", font=("Arial", 12))
            detail_label.pack(side="left", padx=10)


def on_mousewheel(event):
    canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

def on_key(event):
    if event.keysym == 'Down':
        canvas.yview_scroll(1, "units")
    elif event.keysym == 'Up':
        canvas.yview_scroll(-1, "units")

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="Your_username",
    password="Your_password",
    database="Your_database"
)

# Create a cursor object
mycursor = mydb.cursor()

# Create main window
root = tk.Tk()
root.title("Automobile Management System")
root.geometry("900x700")
root.resizable(True, True)

# Provide the full path to the theme directory
theme_dir = r"C:\Users\ADMIN\Downloads\Forest-ttk-theme-master\forest-light.tcl"

root.tk.call("source", theme_dir)

ttk.Style().theme_use('forest-light')
# Header
header_frame = tk.Frame(root, height=50)
header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

# Header label
header_label = tk.Label(header_frame, text="Automobile Management System", font=("Arial", 14))
header_label.pack(side="left")

# Header icon
user_icon = tk.PhotoImage(file="user.png")  # Replace "user.png" with the path to your user icon
resized_user_icon = user_icon.subsample(15, 15)  # Adjust the values as needed
header_icon = tk.Label(header_frame, image=resized_user_icon, cursor="hand2")
header_icon.pack(side="right")

# Create left side panels
left_panel_1 = tk.Frame(root, width=200, height=400)
left_panel_1.grid(row=1, column=0, sticky="ns")

left_panel_2 = tk.Frame(root, width=200, height=400)
left_panel_2.grid(row=1, column=1, sticky="ns")

# Create main panel
main_panel = tk.Frame(root, width=400, height=400)
main_panel.grid(row=1, column=2, sticky="nsew")

# Search Frame
search_frame = tk.Frame(main_panel, height=50)
search_frame.pack(fill="x")

# Create buttons and labels for left panel 1
inventory_icon = tk.PhotoImage(file="car-icon.png")
inventory_button = tk.Button(left_panel_1, image=inventory_icon, command=display_vehicle_inventory, bd=0,
                             cursor="hand2")
inventory_button.pack(pady=10)

search_icon = tk.PhotoImage(file="wrench-icon.png")
search_button = tk.Button(left_panel_1, image=search_icon, command=search_pan, bd=0, cursor="hand2")
search_button.pack(pady=10)

settings_icon = tk.PhotoImage(file="setting-icon.png")
settings_button = tk.Button(left_panel_1, image=settings_icon, bd=0, cursor="hand2")
settings_button.pack(pady=10)

settings_label = tk.Label(left_panel_1)
settings_label.pack(pady=10)

# Create labels for left panel 2
car_type_models = {
    "Sedan": ["Toyota Camry", "Honda Accord", "Nissan Altima"],
    "SUV": ["Land Rover Range Rover", "Toyota RAV4", "Honda CR-V"],
    "Truck": ["Ford F-150", "Chevrolet Silverado", "Ram 1500"],
    "Van": ["Chrysler Pacifica", "Toyota Sienna", "Honda Odyssey"]
}

car_types_label = tk.Label(left_panel_2, text="Car Types:")
car_types_label.pack(pady=5)

car_types = list(car_type_models.keys())
car_type_var = tk.StringVar()
car_type_var.set(car_types[0])
car_type_combobox = ttk.Combobox(left_panel_2, textvariable=car_type_var, values=car_types, state="readonly")
car_type_combobox.pack(pady=5)
car_type_combobox.bind("<<ComboboxSelected>>", update_car_models)

car_models_label = tk.Label(left_panel_2, text="Car Models:")
car_models_label.pack(pady=5)

car_model_var = tk.StringVar()
car_model_combobox = ttk.Combobox(left_panel_2, textvariable=car_model_var, state="readonly")
car_model_combobox.pack(pady=5)

prices_label = tk.Label(left_panel_2, text="Prices:")
prices_label.pack(pady=5)

prices = ["0-499,999ksh", "500,000-999,999ksh", "1,000,000-4,000,000ksh", "4,000,001-10,000,000ksh",
          "10,000,001-30,000,000ksh"]
price_var = tk.StringVar()
price_combobox = ttk.Combobox(left_panel_2, textvariable=price_var, values=prices, state="readonly")
price_combobox.pack(pady=5)

locations_label = tk.Label(left_panel_2, text="Locations:")
locations_label.pack(pady=5)

locations = ["Nakuru", "Kisumu", "Mombasa", "Kericho", "Nyeri", "Nairobi"]
location_var = tk.StringVar()
location_combobox = ttk.Combobox(left_panel_2, textvariable=location_var, values=locations, state="readonly")
location_combobox.pack(pady=5)

# Search Button for the search field
search_button = ttk.Button(left_panel_2, text="Search", command=search)
search_button.pack(pady=5)

# Create label for main panel
search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

add_vehicle_button = ttk.Button(search_frame, text="Add Vehicle")
add_vehicle_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Create canvas and scrollbar for data frame
canvas = tk.Canvas(main_panel)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(main_panel, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame on the canvas to hold the data
data_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=data_frame, anchor="nw")
data_frame.bind("<MouseWheel>", on_mousewheel)
root.bind("<Down>", on_key)
root.bind("<Up>", on_key)
# Load images to prevent garbage collection
image_references = []

# Tracking isf the data frame has been filled
data_frame_filled = False

# Adjust row and column weights to make main panel resizable
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Binding click event to show login window
header_icon.bind("<Button-1>", lambda event: show_login_window())

# Sign-out icon
signout_icon = tk.PhotoImage(file="signout.png")

# Login status
logged_in = False


root.iconbitmap('automobile.ico')
# Run the main loop
root.mainloop()
