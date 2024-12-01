###################          S T A R T        #################################

# Code begins with the greeting display.
import mysql.connector 
import pyfiglet
text = pyfiglet.figlet_format("welcome to PARKING STATION", font="slant")
cen = "\n".join([line.center(80) for line in text.splitlines()])
print(cen)
print('\n')
from datetime import datetime
now = datetime.now()
print("                         ", now.strftime("%A, %Y-%m-%d %H:%M:%S"))
print('\n')
print("                 Align your vehicle in front of the scan interface ")
print('\n')
import keyboard
print("                               Press 'y' to start...")
keyboard.wait('y')

import cv2 as cv  # Code for OCR Recognition.
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from pytesseract import pytesseract
import os

camera = cv.VideoCapture(0)
if not camera.isOpened():
    print("Error: Could not open the webcam.")
    exit()


def display_with_matplotlib(frame):
    plt.imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB)) 
    plt.title('SCAN SUCCESSFUL           --press "s" to continue')
    plt.axis('off')

    global save_image
    save_image = False

    def on_key(event):
        global save_image
        if event.key == 's':
            save_image = True
            plt.close()

    fig = plt.gcf()
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show(block=True)

# Capture an image from the webcam
while True:
    ret, frame = camera.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    
    display_with_matplotlib(frame)

    if save_image:
        cv.imwrite('user1.jpg', frame)
        break

camera.release()

# Tesseract OCR function
def tesseract():
    
    path_to_tesseract = r"C:\Users\sony\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract

    if not os.path.isfile(path_to_tesseract):
        print("Error: Tesseract executable not found.")
        return ""

    
    image_path = r'C:\Users\sony\Desktop\user1.jpg'

    if not os.path.isfile(image_path):
        print("Error: Saved image not found.")
        return ""

    try:
        
        print("Loading information.......")
        text = pytesseract.image_to_string(PILImage.open(image_path))

        
        return text.strip() if text.strip() else ""
    except Exception as e:
        print("Error during OCR:", e)
        return ""

################################################# My SQL Connection#############################################
def insert_to_database(extracted_text):
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='6728',
            database='vehicle',
            host='127.0.0.1'
        )
        cursor = cnx.cursor()

        insert_query = """
            INSERT INTO Vehicle_Records (Vehicle_Registration_No, Date, Time)
            VALUES (%s, %s, %s)
        """
        data_to_insert = (
            extracted_text.strip(),
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S")
            )
        print(f"Inserting into DB: {data_to_insert}")  
        cursor.execute(insert_query, data_to_insert)
        cnx.commit()
        print("Data registered successfully!")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        cnx.rollback()
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

# Call tesseract and insert the result
extracted_text = tesseract()
if extracted_text:  
    insert_to_database(extracted_text)  
else:
    print("No valid vehicle registration number detected.")

print('\n')
print('\n')
print("                             loading........")
import time
time.sleep(3)
print('\n')

print("                    checking parking slot availability........")
time.sleep(3)

##################################### parking slot availability #####################################
class ParkingLot:
    def __init__(self, num_slots):
        self.num_slots = num_slots
        self.slots = [False] * num_slots  

    def is_slot_available(self, slot_num):
        """Checks if a specific slot is available."""
        if 0 <= slot_num < self.num_slots:
            return not self.slots[slot_num]
        else:
            return False

    def are_slots_available(self, num_slots_required):
        """Checks if a given number of consecutive slots are available."""
        for i in range(self.num_slots - num_slots_required + 1):
            if all(not self.slots[j] for j in range(i, i + num_slots_required)):
                return True
        return False

    def book_slot(self, slot_num):
        """Books a specific slot."""
        if self.is_slot_available(slot_num):
            self.slots[slot_num] = True
            print(f"Slot {slot_num} booked successfully.")
        else:
            print(f"Slot {slot_num} is not available.")


# We assume a ParkingLot with 5 slots
parking_lot = ParkingLot(5)

# Check if a specific slot is available
slot_num = 3
if parking_lot.is_slot_available(slot_num):
    print(f"Slot {slot_num} is available.")
else:
    print(f"Slot {slot_num} is not available.")

# Book the slot
parking_lot.book_slot(slot_num)

# Check if the slot is now booked
if parking_lot.is_slot_available(slot_num):
    print(f"Slot {slot_num} is available.")
else:
    print(f"Slot {slot_num} is not available.")

# Check if there are 2 consecutive slots available
num_slots_required = 2
if parking_lot.are_slots_available(num_slots_required):
    print(f"There are {num_slots_required} consecutive slots available.")
else:
    print(f"There are not {num_slots_required} consecutive slots available.")

print('\n')
print('\n')

#################################parking slot navigation using turtle
time.sleep(3)
import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("#acfafa")
screen.title("Navigation Pane")
screen.setup(width=600, height=415)

# Create a turtle object
pen = turtle.Turtle()
pen.speed(0)

# Draw "Go" text
pen.penup()
pen.goto(-200, 0)
pen.pendown()
pen.write("Go", align="center", font=("Consolas", 14, "normal"))

# Draw the arrow 
pen.penup()
pen.goto(-180, 0)
pen.pendown()
pen.pensize(2)
pen.pencolor("blue")
pen.forward(100)
pen.right(90)
pen.forward(100)
pen.left(90)
pen.forward(62)
pen.left(90)
pen.forward(50)
pen.right(90)
pen.forward(70)  


pen.right(150)
pen.forward(10)
pen.backward(10)
pen.right(60)
pen.forward(10)
pen.backward(10)
pen.left(150)

# Draw the rectangles
pen.penup()
pen.goto(20, 50)
pen.pendown()
pen.pencolor("black")
pen.pensize(1)
for _ in range(5):
    for _ in range(2):
        pen.forward(30)
        pen.right(90)
        pen.forward(50)
        pen.right(90)
    pen.penup()
    pen.forward(40)
    pen.pendown()

# Hide the turtle
pen.hideturtle()


turtle.done()
time.sleep(3)
turtle.Screen().bye()


import mysql.connector


print('\n')
print('\n')
print('\n')

figlet = pyfiglet.Figlet(font='mini')
ascii_art = figlet.renderText('Your vehicle is safely parked at the spot and is under strict surveillance')
width = 80  
t= "\n".join(line.center(width) for line in ascii_art.split("\n"))
print(t)

figlet = pyfiglet.Figlet(font='small')
ascii_art = figlet.renderText('just press   "r"   after you return to receive your vehicle')
width = 80  
t11= "\n".join(line.center(width) for line in ascii_art.split("\n"))
print(t11)
# Function to calculate the parking fare based on time difference
def calculate_fare(in_time, out_time):
    parking_duration = (out_time - in_time).total_seconds() / 3600  
    rate_per_hour = 50  
    fare = max(1, round(parking_duration)) * rate_per_hour  
    return fare

# Function to update out time and fare in the database
def update_out_time_and_fare(vehicle_no):
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='6728',
            database='vehicle',
            host='127.0.0.1'
        )
        cursor = cnx.cursor()

        # Get the in time of the vehicle from the database
        select_query = """
            SELECT Date, Time FROM Vehicle_Records WHERE Vehicle_Registration_No = %s ORDER BY S_No DESC LIMIT 1
        """
        cursor.execute(select_query, (vehicle_no,))
        result = cursor.fetchone()

        if not result:
            print("Error: Vehicle record not found.")
            return

        # Parse the in time from the database record
        in_time = datetime.strptime(f"{result[0]} {result[1]}", "%Y-%m-%d %H:%M:%S")
        out_time = datetime.now()  # Current time as out time
        Total_Fare = calculate_fare(in_time, out_time)  # Calculate fare

        # Update the out time and fare in the database
        update_query = """
            UPDATE Vehicle_Records 
            SET Out_Time = %s, Total_Fare = %s
            WHERE Vehicle_Registration_No = %s AND Out_Time IS NULL
        """
        cursor.execute(update_query, (out_time.strftime("%H:%M:%S"), Total_Fare, vehicle_no))
        cnx.commit()

        print(f"\nVehicle {vehicle_no} has checked out.")
        print('\t')
        print(f"Out Time: {out_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n")
        print("\n")
        print(f"                            Total Parking Fare is : ")
        figlet = pyfiglet.Figlet(font='small')
        ascii_art = figlet.renderText(f"₹{Total_Fare} RS.")
        width = 80  
        t112= "\n".join(line.center(width) for line in ascii_art.split("\n"))
        print(t112)
        

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        cnx.rollback()
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

# Wait for the user to press 'r' and calculate the fare
keyboard.wait('r')
print("Recording out time and calculating fare...")
vehicle_registration_no = extracted_text  # Assuming `extracted_text` holds the vehicle number from OCR
update_out_time_and_fare(vehicle_registration_no)





##################################################0###  PAYMENT time ############################################

print('\n')

print("                             press 'd' to complete transaction")
import cv2
keyboard.wait('d')
import matplotlib.image as img   
testImage = img.imread(r'C:\Users\sony\Downloads\qr.jpeg') 
plt.axis("off")
plt.title("Scan to Pay using UPI")
plt.imshow(testImage)
plt.show()
