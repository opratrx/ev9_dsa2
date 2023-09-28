import csv
import datetime
from rich.console import Console
from rich.table import Table
from rich.table import box
from rich.text import Text

BOLDORANGE = "\x1b[1;31m\033[38;2;243;134;48m"
RESET = "\033[0m"

# Extracting log details and adding them to the Rich Table
def create_and_print_table(status_logs):

    # Create a Table object and define its columns
    table = Table(show_header=True, header_style="bold rgb(255,165,0)", box=box.ROUNDED)
    table.add_column("Truck", style="bold rgb(255,255,255)", justify="center", width=12)
    table.add_column("Status", style="bold", width=19)
    table.add_column("Time", style="bold", width=18)
    table.add_column("Miles", style="bold rgb(224,224,224)", width=18)
    table.add_column("Address or Package #", style="bold", width=33)

    # Parse each log and add it as a row to the table
    for log in status_logs:
        parts = log.split(",")

        # Extracting truck number, status, time, and miles
        truck_num = parts[0]
        status = parts[1]
        time = parts[2]
        miles = parts[3]

        # Extracting address or package number
        address_or_package = parts[4]

        # Apply coloring based on the status
        if status.lower() == "delivered":
            status = "[green]Delivered[/green]"
        elif status.lower() == "stopped":
            status = "[yellow]Stopped[/yellow]"
        elif status.lower() == "return":
            status = "[red]Return[/red]"

        # Adding the extracted values as a new row to the table
        table.add_row(truck_num, status, time, miles, address_or_package)

    # Return the table to be printed later
    return table


def create_and_print_package_table(package):
    # Create a Console object
    console = Console(color_system="256")

    # Create a Table object and define its columns
    table = Table(show_header=True, header_style="bold rgb(255,165,0)", box=box.ROUNDED)
    table.add_column("ID", style="bold rgb(255,165,0)", width=8)
    table.add_column("Street", style="dim", width=20)
    table.add_column("Deadline", style="dim", width=15)
    table.add_column("Weight", style="dim", width=12)
    table.add_column("Status", style="dim", width=15)
    table.add_column("Departed", style="dim", width=15)
    table.add_column("Delivered", style="dim", width=15)

    # Adding status with style
    status = package.status
    if status.lower() == "delivered":
        status_text = Text(status, style="bold green")
    elif status.lower() == "hub":  # Explicit condition for 'Hub' status
        status_text = Text(status, style="bold red")
    else:  # Adjust as needed for other statuses
        status_text = Text(status, style="yellow")

    # Adding a row to the table with the package details
    table.add_row(str(package.ID), package.street, package.deadline, package.weight, status_text,
                  str(package.departureTime), str(package.deliveryTime))

    # Print the table
    console.print(table)


# Define the log_truck_metrics_with_date function within your code
def log_truck_metrics_with_date(truck, truck_num):
    # Calculate the drive time in hours
    drive_time = truck.time.total_seconds() / 3600 - truck.departTime.total_seconds() / 3600  # 1 hour = 3600 seconds

    # Use a recent date as the base date for Departure and Return Time
    base_date = datetime.datetime(2023, 9, 25).date()  # Replace with the actual recent date you want to use

    # Add the base date to the departure and return time and format them to include date and time information
    departure_datetime = datetime.datetime.combine(base_date, datetime.datetime.min.time()) + truck.departTime
    return_datetime = datetime.datetime.combine(base_date, datetime.datetime.min.time()) + truck.time
    departure_time_str = departure_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return_time_str = return_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Create a formatted string with the truck metrics
    metrics_str = (
        f"\n\x1b[1;31m\033[38;2;243;134;48mTruck #{truck_num} metrics:\n"
        "———————————————————————————————————————————————\n\033[0m"
        f"Departure Time: {departure_time_str}\n"
        f"Return Time: {return_time_str}\n"
        f"Drive Time: {drive_time:.2f} hours\n"
        f"Total Distance: {truck.miles:.1f} miles\n"
    )

    return metrics_str


# HashTable with Chaining
class HashTableWChains:
    def __init__(self, initialcapacity=40):
        self.table = []
        for i in range(initialcapacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
                return True
        return False


# Package Class
class Packages:
    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status='At Hub', departureTime=None,
                 deliveryTime=None):
        self.deliveryTime = deliveryTime
        self.departureTime = departureTime
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    def __str__(self):
        return (self.ID, self.street, self.deadline, self.weight, self.status,
                self.departureTime, self.deliveryTime)

    def statusUpdate(self, timeChange):
        if self.deliveryTime is None:
            self.status = "Hub"
        elif timeChange < self.departureTime:
            self.status = "Hub"
        elif timeChange < self.deliveryTime:
            self.status = "En-route"
        else:
            self.status = "Delivered"
        if self.ID == 9:
            if timeChange > datetime.timedelta(hours=10, minutes=20):
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"


# Load package data from CSV
def loadPackageData(filename):
    with open(filename) as packagess:
        packageInfo = csv.reader(packagess, delimiter=',')
        next(packageInfo)
        for package in packageInfo:
            pID = int(package[0])
            pStreet = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At the Hub"
            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)
            packageHash.insert(pID, p)


# Initialize HashTable
packageHash = HashTableWChains()

# Load CSV data
with open("addressCSV.csv") as addyCSV:
    AddressCSV = csv.reader(addyCSV)
    AddressCSV = list(AddressCSV)
with open("distanceCSV.csv") as disCSV:
    DistanceCSV = csv.reader(disCSV)
    DistanceCSV = list(DistanceCSV)

# Load package data
loadPackageData('packageCSV.csv')


# Truck Class
class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages


# Helper functions for address and distance lookup
def addresss(address):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])


def Betweenst(addy1, addy2):
    distance = DistanceCSV[addy1][addy2]
    if distance == '':
        distance = DistanceCSV[addy2][addy1]
    return float(distance)


def truckDeliverPackages(truck, truck_num):
    enroute = []
    status_logs = []

    for packageID in truck.packages:
        package = packageHash.search(packageID)
        enroute.append(package)
    truck.packages.clear()
    while len(enroute) > 0:
        nextAddy = 2000
        nextPackage = None
        for package in enroute:
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                break
            if Betweenst(addresss(truck.currentLocation), addresss(package.street)) <= nextAddy:
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                nextPackage = package

        # Indicates when the truck has stopped at the delivery location.
        statusStops = (
            f"{truck_num},stopped,{truck.time},{truck.miles:.1f},{nextPackage.street}")
        status_logs.append(statusStops)

        truck.packages.append(nextPackage.ID)
        enroute.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime

        # Indicates that the package has been delivered
        statusDelivered = f"{truck_num},delivered,{truck.time} , ,Package {nextPackage.ID}"
        status_logs.append(statusDelivered)

    return_distance = Betweenst(addresss(truck.currentLocation), addresss("4001 South 700 East"))
    truck.miles += return_distance
    truck.time += datetime.timedelta(hours=return_distance / 18)

    # Indicates when the truck has arrived at the hub
    statusHub = f"{truck_num},return,{truck.time},{truck.miles:.1f},4001 South 700 East (hub)"
    status_logs.append(statusHub)
    return status_logs


'''
************************************************************************************************
                                     USER INTERFACE SECTION
                            UI / UX Design and Program Initialization
************************************************************************************************
'''


def main():
    # Print Title
    print(BOLDORANGE + "\n\n\nWestern Governors University Parcel Service" + RESET)

    # Initialize truck objects (truck1, truck2, truck3) here
    truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                    [1, 29, 7, 30, 8, 34, 40, 13, 39, 14, 15, 16, 19, 20, 37])
    truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),
                    [6, 5, 21, 4, 24, 23, 26, 22, 10, 11, 31])
    truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                    [17, 12, 25, 28, 32, 3, 18, 36, 38, 27, 35, 2, 33, 9])

    # Initialize status logs for each truck
    status_logs_truck1 = truckDeliverPackages(truck1, 1)
    truck2.departTime = min(truck1.time, truck3.time)
    status_logs_truck2 = truckDeliverPackages(truck2, 2)
    status_logs_truck3 = truckDeliverPackages(truck3, 3)

    # Display overall miles for all the trucks
    print("The overall miles are:", (truck1.miles + truck2.miles + truck3.miles))

    # Main program loop
    while True:
        # Display the menu to the user and get the user's choice
        user_choice = input(BOLDORANGE + "\n\n\nWhat would you like to do?" + RESET + "\n\td - Begin Delivery Simulation\n\tl - Lookup Package Status\n\tq - Quit\n> ")

        # If the user chooses to quit, exit the program
        if user_choice.lower() == 'q':
            break

        # If the user chooses to begin the delivery simulation
        elif user_choice.lower() == 'd':
            print("\n\n\nBeginning delivery simulation...\n\n\n")

            # Print Delivery Logs (statusStops, statusDelivered, statusHub)

            # Creating the table
            table1 = create_and_print_table(status_logs=status_logs_truck1)
            table2 = create_and_print_table(status_logs=status_logs_truck2)
            table3 = create_and_print_table(status_logs=status_logs_truck3)
            console = Console(color_system="256")

            # Printing the truck metrics and tables
            print("\n\x1b[1;31m\033[38;2;243;134;48mDelivery complete for all trucks!\033[0m\n")
            print(log_truck_metrics_with_date(truck1, 1))
            console.print(table1)
            print(log_truck_metrics_with_date(truck2, 2))
            console.print(table2)
            print(log_truck_metrics_with_date(truck3, 3))
            console.print(table3)

            # Calculate the corrected total time in hours
            total_time_corrected = (
                                           (truck1.time.total_seconds() - truck1.departTime.total_seconds())
                                           + (truck2.time.total_seconds() - truck2.departTime.total_seconds())
                                           + (truck3.time.total_seconds() - truck3.departTime.total_seconds())
                                   ) / 3600  # Convert total seconds to hours

            # Calculate the total distance and total packages delivered
            total_distance = truck1.miles + truck2.miles + truck3.miles
            total_packages_delivered = len(truck1.packages) + len(truck2.packages) + len(truck3.packages)

            # Printing the total metrics for all trucks
            print(f"\n\n\x1b[1;31m\033[38;2;243;134;48mTotal metrics:\033[0m\n"
                  f"\x1b[1;31m\033[38;2;243;134;48m———————————————————————————————————————————————\033[0m")
            print("Total Distance: ", total_distance)
            print(f"Total Time Spent: {total_time_corrected:.1f} hours")
            print("Total Packages Delivered: ", total_packages_delivered)

        # If the user chooses to lookup package status
        elif user_choice.lower() == 'l':
            user_time = input(
                "\n\x1b[1;31m\033[38;2;243;134;48m Please input the time in 24-hour [HH:MM] format you wish to view the package statuses for, e.g., enter 14:30 for 2:30 PM:\033[0m \n> ")
            (h, m) = user_time.split(":")
            time_change = datetime.timedelta(hours=int(h), minutes=int(m))

            try:
                single_entry = [int(input(
                    "\n\n\x1b[1;31m\033[38;2;243;134;48mPlease enter the package ID [1-40] you wish to view, or enter to view all packages:\033[0m \n> "))]
            except ValueError:
                single_entry = range(1, 41)  # Assuming range is from 1 to 40 packages

            for package_id in single_entry:
                package = packageHash.search(package_id)
                package.statusUpdate(time_change)
                create_and_print_package_table(package)


if __name__ == "__main__":
    main()
