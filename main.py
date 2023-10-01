"""

Author: Aaron Ballesteros
Student ID: 011019047
Start Date: 9/25/2023
Last Modified: 9/28/2023
Description: Package Delivery Service Program
Class: Data Structures and Algorithms II
School: Western Governors University

WGUPS Parcel Service Program: This program delivers packages by finding the nearest node from
the previous node and adds the distance to the total cost (mile). The goal is to minimize the
cost (miles) and deliver the packages in the most efficient way based on the constraints.

"""

# Python core libraries - Functionality
import csv
import datetime
import time

# Third-party libraries - User Interface
from rich.console import Console
from rich.table import Table
from rich.table import box
from rich.text import Text

'''
    ,------------------------------------------------------------------------------------------------,
    |                                HASH TABLE WITH CHAINS CLASS                                    |
    |                                Time Complexity: O(1) - O(n)                                    |
    '------------------------------------------------------------------------------------------------'
    
    Description: This class represents a hash table with chaining implementation, allowing 
                 the storage of key-value pairs. In cases of hash collisions, the colliding 
                 items are stored in a linked list.
    Methods: 
        1. __init__: Initializes the hash table with an initial capacity.
        2. insert: Inserts an item into the hash table.
        3. search: Searches for an item based on the key.
        4. remove: Removes an item from the hash table based on the key.
        5. get_package_id_by_street: Searches for a package based on the street address.
        
    Time Complexity: 
        - insert: O(1) average and O(n) worst case.
        - search: O(1) average and O(n) worst case.
        - remove: O(1) average and O(n) worst case.
        - get_package_id_by_street: O(n) where n is the total number of items in the hash table.

'''


class HashTableWChains:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
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

    def get_package_id_by_street(self, street):
        for bucket in self.table:
            for key, package in bucket:
                if package.street == street:
                    return package.ID
        return "Hub"  # return "Hub" if no package is found aka Source


'''
    ,------------------------------------------------------------------------------------------------,
    |                                        PACKAGES CLASS                                          |
    |                                     Time Complexity: O(1)                                      |
    '------------------------------------------------------------------------------------------------'
    
    Description: This class represents a package with various attributes such as ID, street, 
                 city, state, zip, deadline, weight, notes, status, departureTime, and deliveryTime.
    Methods: 
        1. __init__: Initializes a package object with the given attributes.
        2. __str__: Returns a string representation of the package object.
        3. statusUpdate: Updates the status of the package based on the given time change.
    
    Time Complexity: 
        - __init__: O(1)
        - __str__: O(1)
        - statusUpdate: O(1)

'''


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


# '''
#      | ,------------------------------------------------------------------------------------------------,
#      | |                                PACKAGE DATA LOADING FUNCTION                                   |
#      | |                                     loadPackageData(filename)                                  |
#      | '------------------------------------------------------------------------------------------------'
#      |   Description: This function loads package data from a CSV file. It opens the file and reads the package
#      |                information using the csv.reader. It skips the header row and iterates through each row of
#      |                package data. It extracts the necessary information and creates a Packages object. It then
#      |                inserts the package into the packageHash hash table using the package ID as the key.
#      |
#      |   Time Complexity: O(n)
# '''


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

'''
        ,------------------------------------------------------------------------------------------------,
        |                                          TRUCKS CLASS                                          |
        |                                      Time Complexity: O(1)                                     |
        '------------------------------------------------------------------------------------------------'
        
    Description: This class represents a truck with attributes such as speed, miles, currentLocation, 
                    departTime, and packages.
       
    Time Complexity: O(1)

'''


class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages


# '''
#     | ,------------------------------------------------------------------------------------------------,
#     | |                                       ADDRESS SEARCH FUNCTION                                  |
#     | |                                         address(addresses)                                     |
#     | '------------------------------------------------------------------------------------------------'
#     |   Description: This function searches for an address in the addressCSV list. It iterates through each row
#     |                of the list and checks if the address is present in the third column. If found, it returns
#     |                the corresponding address ID.
#     |
#     |   Time Complexity: O(n)
# '''
def address(addresses):
    for row in AddressCSV:
        if addresses in row[2]:
            return int(row[0])


# '''
#     | ,------------------------------------------------------------------------------------------------,
#     | |                                   DISTANCE BETWEEN ADDRESSES FUNCTION                          |
#     | |                                       Betweenst(addy1, addy2)                                  |
#     | '------------------------------------------------------------------------------------------------'
#     |   Description: This function calculates the distance between two addresses based on the address IDs. It
#     |                retrieves the distance from the distanceCSV list using the address IDs as indices. If the
#     |                distance is empty, it retrieves the distance from the reverse direction. It returns the
#     |                distance as a float.
#     |
#     |   Time Complexity: O(1)
# '''
def betweenst(addy1, addy2):
    distance = DistanceCSV[addy1][addy2]
    if distance == '':
        distance = DistanceCSV[addy2][addy1]
    return float(distance)


'''
            ,------------------------------------------------------------------------------------------------,
            |                               TRUCK DELIVERY SIMULATION FUNCTION                               |
            |                                     Time Complexity: O(n^2)                                    |
            '------------------------------------------------------------------------------------------------'       

      Description: This function simulates the delivery process for a truck. It takes a truck object and
                    truck number as input. It initializes an empty list for en_route packages and an
                    empty list for status logs. It adds the packages from the truck object to the en_route
                    list. It then enters a loop until all packages are delivered. In each iteration, it
                    finds the next package to deliver based on the current location and the distance to
                    each package's street address. It updates the status logs and truck attributes
                    accordingly. Once all packages are delivered, it calculates the distance to return to
                    the hub and updates the status logs and truck attributes. It returns the status logs.
    
      Time Complexity: O(n^2)
'''


def truckDeliverPackages(truck, truck_num):
    # Initialize a table for logging status of algorithms
    table = Table(title="\n[bold][yellow]Algorithm Progress for Truck #" + str(truck_num) + "[/yellow][/bold]",
                  show_header=True, header_style="bold rgb(255,165,0)", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Current Node", justify="right")
    table.add_column("Candidates", justify="right")
    table.add_column("Chosen Node", justify="right")
    table.add_column("Chosen Cost", justify="right")
    table.add_column("Total Cost", justify="right")

    en_route = []
    status_logs = []

    for packageID in truck.packages:
        package = packageHash.search(packageID)
        en_route.append(package)
    truck.packages.clear()

    while len(en_route) > 0:
        nextAddy = 2000
        nextPackage = None
        candidates = []

        # Log the state of en route before the for loop
        # en_route_ids = ", ".join(str(package.ID) for package in en_route)

        # Uncomment to print the status check in the console - Algorithm Analysis
        # console.print(f"\n[yellow]En route before loop:[/yellow] {en_route_ids}")

        for package in en_route:
            # Log the state of the package being considered
            # considering_ids = ", ".join(str(package.ID) for package in en_route)

            # Uncomment to print the status check in the console - Algorithm Analysis
            # console.print(f"[green]Considering package:[/green] {considering_ids}")

            # Uncomment to view the package street in addition to its ID
            # console.print(f"\n[green]Considering package:[/green] {package.ID} at [white]{package.street}[/white]")

            candidates.append(package.ID)

            # Log the state of candidates after appending
            # candidates_ids = ", ".join(str(candidate) for candidate in candidates)

            # Uncomment to print the status check in the console - Algorithm Analysis
            # console.print(f"[orange]Candidates after appending:[/orange] {candidates_ids}")

            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = betweenst(address(truck.currentLocation), address(package.street))
                break

            if betweenst(address(truck.currentLocation), address(package.street)) <= nextAddy:
                nextAddy = betweenst(address(truck.currentLocation), address(package.street))
                nextPackage = package

        # Initialize table parameters for each decision
        # current_node = truck.currentLocation
        candidates_ids = ", ".join(str(candidate) for candidate in candidates)
        current_package_id = packageHash.get_package_id_by_street(truck.currentLocation)
        chosen_node = nextPackage.street if nextPackage else "N/A"
        chosen_package_id = packageHash.get_package_id_by_street(chosen_node) if nextPackage else "N/A"
        chosen_cost = nextAddy
        total_cost = truck.miles + chosen_cost

        table.add_row(
            Text(str(current_package_id), style="black on yellow", justify="center"),
            Text(str(candidates_ids), style="bold green", justify="left"),
            Text(str(chosen_package_id), style="black on green", justify="center"),
            Text(str(round(chosen_cost, 2)), style="bold red"),
            Text(str(round(total_cost, 2)), style="bold red")
        )

        # Indicates when the truck has stopped at the delivery location.
        statusStops = (
            f"{truck_num},stopped,{truck.time},{truck.miles:.1f},{nextPackage.street}")
        status_logs.append(statusStops)

        truck.packages.append(nextPackage.ID)
        en_route.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime

        # Indicates that the package has been delivered
        statusDelivered = f"{truck_num},delivered,{truck.time} , ,Package {nextPackage.ID}"
        status_logs.append(statusDelivered)

    return_distance = betweenst(address(truck.currentLocation), address("4001 South 700 East"))
    truck.miles += return_distance
    truck.time += datetime.timedelta(hours=return_distance / 18)

    # Indicates when the truck has arrived at the hub
    statusHub = f"{truck_num},return,{truck.time},{truck.miles:.1f},4001 South 700 East (hub)"
    status_logs.append(statusHub)

    # Uncomment to print the status check in the console - Algorithm Analysis
    # console.print(table)

    return status_logs


'''
 ,------------------------------------------------------------------------------------------------,
 |                                     USER INTERFACE SECTION                                     |
 |                            UI / UX Design and Program Initialization                           |
 '------------------------------------------------------------------------------------------------'
'''

# Global color settings for the user interface
BOLDORANGE = "\x1b[1;31m\033[38;2;243;134;48m"
RESET = "\033[0m"


    # '''
    #     | ,------------------------------------------------------------------------------------------------,
    #     | |                              PARAMETER TABLE CREATION FUNCTION                                 |
    #     | |                       create_and_print_parameter_table(package, param_choice)                  |
    #     | '------------------------------------------------------------------------------------------------'
    #     |   Description: This function creates and prints a table with the specified parameter for a package.
    #     |                It takes a package object and a parameter choice as input. It creates a table with
    #     |                appropriate columns based on the parameter choice. It retrieves the value of the
    #     |                parameter from the package object and adds it to the table. If the parameter choice
    #     |                is 'h', it adds all parameters to the table. It then prints the table.
    #     |
    #     |   Time Complexity: O(1)
    # '''

def create_and_print_parameter_table(package, param_choice):
    # Create a Console object
    console = Console(color_system="256")
    param_dict = {'a': 'street', 'b': 'city', 'c': 'zip', 'd': 'state', 'e': 'deadline', 'f': 'weight', 'g': 'status',
                  'h': 'all'}

    # If user chooses to view all parameters, add columns for all parameters and fill in the values.
    if param_choice == 'h':
        table = Table(title=f"\n[bold][yellow]Details for Package #{package.ID}[/yellow][/bold]", show_header=True,
                      header_style="bold rgb(255,165,0)", box=box.ROUNDED)
        table.add_column("Address")
        table.add_column("City")
        table.add_column("Zip Code")
        table.add_column("State")
        table.add_column("Deadline")
        table.add_column("Weight")
        table.add_column("Status")

        # Adding status with style
        status = package.status
        if status.lower() == "delivered":
            status_text = Text(status, style="bold green")
        elif status.lower() == "hub":  # Explicit condition for 'Hub' status
            status_text = Text(status, style="bold red")
        else:  # Adjust as needed for other statuses
            status_text = Text(status, style="yellow")

        table.add_row(package.street, package.city, package.zip, package.state, package.deadline, package.weight,
                      status_text)

    # If user chooses to view a specific parameter, create a table with a single column for that parameter and fill in the value.
    else:
        param = param_dict[param_choice]
        table = Table(title=f"\n[bold][yellow]{param.capitalize()} for Package #{package.ID}[/yellow][/bold]",
                      show_header=True,
                      header_style="bold rgb(255,165,0)", box=box.ROUNDED)
        table.add_column(param.capitalize())

        # Get the status using getattr to fetch the value of the attribute named by the param variable
        status = getattr(package, param)

        # Apply coloring based on the status
        if status.lower() == "delivered":
            status_text = Text(status, style="bold green")
        elif status.lower() == "hub":  # Explicit condition for 'Hub' status
            status_text = Text(status, style="bold red")
        else:  # Adjust as needed for other statuses
            status_text = Text(status, style="yellow")

        table.add_row(status_text)  # Add the styled status text as a row to the table without converting it to a string

    console.print(table)  # Print the table to the console

    # '''
    #     | ,------------------------------------------------------------------------------------------------,
    #     | |                                  STATUS LOGS TABLE FUNCTION                                    |
    #     | |                                  create_and_print_table(status_logs)                           |
    #     | '------------------------------------------------------------------------------------------------'
    #     |   Description: This function creates and prints a table with the status logs. It takes a list of
    #     |                status logs as input. It creates a table with appropriate columns and adds each
    #     |                status log as a row to the table. It then prints the table.
    #     |
    #     |   Time Complexity: O(n)
    # '''


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
        log_time = parts[2]
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
        table.add_row(truck_num, status, log_time, miles, address_or_package)

    # Return the table to be printed later
    return table

    # '''
    #     | ,------------------------------------------------------------------------------------------------,
    #     | |                               PACKAGE DETAILS TABLE FUNCTION                                   |
    #     | |                             create_and_print_package_table(package)                            |
    #     | '------------------------------------------------------------------------------------------------'
    #     |   Description: This function creates and prints a table with the details of a package. It takes a
    #     |                package object as input. It creates a table with appropriate columns and adds the
    #     |                package details as a row to the table. It then prints the table.
    #     |
    #     |   Time Complexity: O(1)
    # '''


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
    table.add_column("Delivered", style="bold yellow", width=15)

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

    # '''
    #     | ,------------------------------------------------------------------------------------------------,
    #     | |                               TRUCK METRICS LOGGING FUNCTION                                   |
    #     | |                         log_truck_metrics_with_date(truck, truck_num)                          |
    #     | '------------------------------------------------------------------------------------------------'
    #     |   Description: This function generates a string with the metrics of a truck. It takes a truck object
    #     |                and truck number as input. It calculates the drive time, departure time, return time,
    #     |                and total distance. It formats the metrics as a string and returns it.
    #     |
    #     |   Time Complexity: O(1)
    # '''


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


# '''
#     | ,------------------------------------------------------------------------------------------------,
#     | |                                  TOTAL METRICS TABLE FUNCTION                                  |
#     | |                                     print_total_metrics()                                      |
#     | '------------------------------------------------------------------------------------------------'
#     |   Description: This function creates and prints a table with the total metrics of all trucks. It takes
#     |                the total distance, total time corrected, and total packages delivered as input. It creates
#     |                a table with appropriate columns and adds the metrics as a row to the table. It then prints
#     |                the table.
#     |
#     |   Time Complexity: O(1)
# '''


def print_total_metrics(total_distance, total_time_corrected, total_packages_delivered):
    # Create console and table objects
    console = Console(color_system="256")

    table = Table(title="\n\n[bold][yellow]Total Metrics[/yellow][/bold]", show_header=True,
                  header_style="bold rgb(255,165,0)", box=box.ROUNDED)

    # Add columns to the table
    table.add_column("Total Distance")
    table.add_column("Total Time Spent (hours)")
    table.add_column("Total Packages Delivered")

    # Add a single row with the metric values
    table.add_row(str(total_distance), f"{total_time_corrected:.1f}", str(total_packages_delivered))

    # Print the table to console
    console.print(table)


'''
     ,------------------------------------------------------------------------------------------------,
     |                                         MAIN FUNCTION                                          |
     |                                    Time Complexity: O(n^2)                                     |
     '------------------------------------------------------------------------------------------------'

   Description: This function is the main entry point of the program. It displays a welcome message and
                initializes three truck objects. It simulates the delivery process for each truck and
                stores the status logs. It calculates the total distance, total time corrected, and total
                packages delivered. It then enters a loop to interact with the user. The user can choose to
                begin the delivery simulation, lookup package status, or quit the program. If the user chooses
                to begin the delivery simulation, it prints the status logs and truck metrics. If the user
                chooses to lookup package status, it prompts for a time and package ID, and then prints the
                package details or parameter value.
   
   Time Complexity: O(n^2)

'''


def main():
    console = Console(color_system="256")
    # Print Title
    print(BOLDORANGE + "\n\n\nWestern Governors University Parcel Service" + RESET)
    print("Author: Aaron Ballesteros")
    print("ID: 011019047")
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

    # Calculate the corrected total time in hours
    total_time_corrected = (
                                   (truck1.time.total_seconds() - truck1.departTime.total_seconds())
                                   + (truck2.time.total_seconds() - truck2.departTime.total_seconds())
                                   + (truck3.time.total_seconds() - truck3.departTime.total_seconds())
                           ) / 3600  # Convert total seconds to hours

    # Calculate the total distance and total packages delivered
    total_distance = truck1.miles + truck2.miles + truck3.miles
    total_packages_delivered = len(truck1.packages) + len(truck2.packages) + len(truck3.packages)

    print_total_metrics(total_distance, total_time_corrected, total_packages_delivered)

    # Main program loop
    while True:
        # Display the menu to the user and get the user's choice
        user_choice = input(
            BOLDORANGE + "\n\n\nWhat would you like to do?" + RESET + "\n\td - Begin Delivery Simulation\n\tl - Lookup Package Status\n\tq - Quit\n> ")

        # If the user chooses to quit, exit the program
        if user_choice.lower() == 'q':
            break

        # If the user chooses to begin the delivery simulation
        elif user_choice.lower() == 'd':
            console.print("\n\n\n[yellow]Beginning delivery simulation...[/yellow]\n\n\n")
            time.sleep(1)

            # Print Delivery Logs (statusStops, statusDelivered, statusHub)

            # Creating the table
            table1 = create_and_print_table(status_logs=status_logs_truck1)
            table2 = create_and_print_table(status_logs=status_logs_truck2)
            table3 = create_and_print_table(status_logs=status_logs_truck3)
            console = Console(color_system="256")

            # Printing the truck metrics and tables
            console.print("\n[bold][green]Delivery complete for all trucks![green][/bold]\n")
            time.sleep(0.5)
            print(log_truck_metrics_with_date(truck1, 1))
            time.sleep(0.5)
            console.print(table1)
            time.sleep(0.5)
            print(log_truck_metrics_with_date(truck2, 2))
            time.sleep(0.5)
            console.print(table2)
            time.sleep(0.5)
            print(log_truck_metrics_with_date(truck3, 3))
            time.sleep(0.5)
            console.print(table3)

            print_total_metrics(total_distance, total_time_corrected, total_packages_delivered)

        elif user_choice.lower() == 'l':
            while True:
                # User inputs time
                user_time = input(
                    BOLDORANGE + "\nPlease input the time in 24-hour [HH:MM] format you wish to view the package statuses for, e.g., enter 14:30 for 2:30 PM:" + RESET + "\n> ")
                # Split the entered time by ":"
                time_parts = user_time.split(":")
                # Check if the entered time is in correct format and after 08:00
                if len(time_parts) == 2 and time_parts[0].isdigit() and time_parts[1].isdigit():
                    h, m = map(int, time_parts)
                    if 8 <= h < 24 and 0 <= m < 60:
                        time_change = datetime.timedelta(hours=h, minutes=m)
                        break  # Exit the loop if valid time is entered
                    else:
                        console.print("[red]Invalid time! Please enter a time after 08:00.[/red]")
                else:
                    console.print("[red]Invalid format! Please enter time in HH:MM format.[/red]")
            while True:
                try:
                    package_id = input(
                        BOLDORANGE + "\n\nPlease enter the package ID you wish to view, or press Enter to view all packages:" + RESET + "\n> ")
                    if package_id:  # if the user didn't press Enter
                        package_id = int(
                            package_id)  # try to convert to integer. This will raise ValueError if it fails.
                        if package_id < 1 or package_id > 40:  # assuming package_id should be positive.
                            raise ValueError("Package ID must be a positive number.")
                        packages_to_view = [packageHash.search(package_id)]
                        break  # if conversion to integer succeeded, exit the loop
                    else:
                        packages_to_view = [packageHash.search(i) for i in range(1, 41)]  # Assuming 40 packages
                        break  # if the user pressed Enter, exit the loop
                except ValueError as e:
                    # Display error message to user and continue the loop
                    console.print(
                        f"[red]Invalid input! {str(e)} Please enter a valid package ID or press Enter for all packages.[/red]")
            if package_id:
                while True:
                    param_choice = input(BOLDORANGE + "\n\nSelect the parameter you want to view:\n" + RESET +
                                         "\ta - Address\n\tb - City\n\tc - Zip Code\n\td - State\n\te - Deadline\n\tf - Weight\n\tg - Status\n\th - All\n> ").lower()
                    param_dict = {'a': 'street', 'b': 'city', 'c': 'zip', 'd': 'state', 'e': 'deadline', 'f': 'weight',
                                  'g': 'status', 'h': 'all'}
                    if param_choice not in param_dict:
                        console.print("[red]Invalid choice! Please select a valid option.[/red]")
                    else:
                        # Display selected parameter for the entered package ID
                        package = packages_to_view[0]
                        package.statusUpdate(time_change)
                        create_and_print_parameter_table(package, param_choice)
                        break
            else:
                # Display all parameters using create_and_print_package_table for all packages
                for package in packages_to_view:
                    package.statusUpdate(time_change)
                    create_and_print_package_table(package)



if __name__ == "__main__":
    main()
