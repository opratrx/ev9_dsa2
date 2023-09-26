import csv
import datetime


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
        f"\nTruck #{truck_num} metrics:\n"
        "———————————————————————————————————————————————\n"
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
        return "Package ID | Address                                   | City             | Zip Code | Weight | Status"

    def statusUpdate(self, timeChange):
        if self.deliveryTime is None:
            self.status = "At the hub"
        elif timeChange < self.departureTime:
            self.status = "At the hub"
        elif timeChange < self.deliveryTime:
            self.status = "En route"
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


# Create a global list to hold our delivery logs
delivery_logs = []


# Update truckDeliverPackages to append to the delivery_logs instead of print
def truckDeliverPackages(truck, truck_num):
    enroute = []
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
            f"  \x1b[1;37m[Truck #{truck_num}]    \x1b[1;31m✘\tstopped\t\t\t[{truck.time}]\t\t\t{truck.miles:.1f} miles driven.   \033[34;2m\t{nextPackage.street},"
            f" {nextPackage.city}, {nextPackage.state}, {nextPackage.zip}\033[0m")
        print(statusStops)

        truck.packages.append(nextPackage.ID)
        enroute.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime

        # Indicates that the package has been delivered
        statusDelivered = f"  \x1b[1;37m[Truck #{truck_num}]    \033[32;2m✔︎\tdelivered\t\t[{truck.time}]   \033[34;2m\t\t\t\t\t\t\t\tPackage {nextPackage.ID}.\033[0m"
        print(statusDelivered)

    return_distance = Betweenst(addresss(truck.currentLocation), addresss("4001 South 700 East"))
    truck.miles += return_distance
    truck.time += datetime.timedelta(hours=return_distance / 18)

    # Indicates when the truck has arrived at the hub
    statusHub = f"  \x1b[1;31m\033[38;2;243;134;48m[Truck #{truck_num}]    ⬆︎\treturn\t\t\t[{truck.time}]\t\t\t{truck.miles:.1f} miles driven.   \t4001 South 700 East (hub)\033[0m"
    print(statusHub)


truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                            [1, 29, 7, 30, 8, 34, 40, 13, 39, 14, 15, 16, 19, 20, 37])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),
                            [6, 5, 21, 4, 24, 23, 26, 22, 10, 11, 31])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                            [17, 12, 25, 28, 32, 3, 18, 36, 38, 27, 35, 2, 33, 9])


print("⎢ Truck #    ⎢ Status           ⎢ Time              ⎢ Miles                 ⎢ Address or Package #")
print("——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
truckDeliverPackages(truck1, 1)
truck2.departTime = min(truck1.time, truck3.time)
truckDeliverPackages(truck2, 2)
truckDeliverPackages(truck3, 3)

print("\nDelivery complete for all trucks!\n")
# TODO: Display all metrics, such as total distance traveled by each truck, total time spent, etc.
print(log_truck_metrics_with_date(truck1, 1))
print(log_truck_metrics_with_date(truck2, 2))
print(log_truck_metrics_with_date(truck3, 3))

# Calculate the corrected total time in hours
total_time_corrected = (
    (truck1.time.total_seconds() - truck1.departTime.total_seconds())
    + (truck2.time.total_seconds() - truck2.departTime.total_seconds())
    + (truck3.time.total_seconds() - truck3.departTime.total_seconds())
) / 3600  # Convert total seconds to hours

# Calculate the total distance and total packages delivered
total_distance = truck1.miles + truck2.miles + truck3.miles
total_packages_delivered = len(truck1.packages) + len(truck2.packages) + len(truck3.packages)


print(f"\nTotal metrics:\n"
      f"———————————————————————————————————————————————")
print("Total Distance: ", total_distance)
print(f"Total Time Spent: {total_time_corrected:.1f} hours")
print("Total Packages Delivered: ", total_packages_delivered)

