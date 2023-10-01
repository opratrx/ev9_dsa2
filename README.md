# <span style="color:orange;">C950 - WGUPS Delivery Tracking System &nbsp; ![Header](https://img.shields.io/badge/-Project-ff6600)
> [!WARNING]
> This project is currently a work in progress as of September 30, 2023. Please be aware that functionalities might be incomplete, and there might be frequent updates or changes.


<br><br>

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) `General Project Information`

The Western Governors University Parcel Service (WGUPS) is tasked with determining the best route and delivery distribution for their Daily Local Deliveries in Salt Lake City.
<br><br>
## Overview
The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day; each package has specific criteria and delivery requirements.
<br><br>
## Objective
The aim is to write efficient code that presents a solution for delivering all 40 packages on time, according to their criteria, while minimizing the total number of miles traveled by the trucks. The code should also allow the supervisor to check the status of any given package at any given time using package IDs, and it should report delivery times, which packages are at the hub, and which are en route.
<br><br>
## User Interface
A user-friendly interface has been developed and improved utilizing the Rich library to present the package delivery process in a clean and organized manner.

![Alt Text](https://github.com/opratrx/opratrx/blob/master/DSA2.gif?raw=true)

<br><br><br><br>


## Progress & Updates
![#00FF00](https://via.placeholder.com/15/00FF00/000000?text=+) `Commit Information`
###### 9/26/23 - Initial Commit 

> [!NOTE]
> Uploading the current structure of the main components to the software. This commit is the basic functionality of the program before implementing anything further such as the user interface. For the moment, this is a basic layout and foundational draft.
> 

###### 9/28/23 - Implemented a Working User Interface

> [!NOTE]
> Implemented a working user interface and will be incorporating a better design in the next few updates. For the time being, this will serve as the first draft of the user interface.
> 

###### 9/28/23 - Improved User Interface Using the Textualize Rich Library

> [!NOTE]
> Improving the look and feel of the user interface using the Rich library to oraganize the package delivery process into a data table.
> 

###### 9/28/23 - Improved CLI and Added Algorithm Analysis + Status Checks for Each Process in the Algorithm.

> [!NOTE]
> Improving the CLI and added a status check for each step in the process of the Greedy / Nearest Neighbor Algorithm for Analysis.
> 

###### 9/29/23 - Added Input Validation, View Package by Parameter, and Improved CLI for UI / UX.

> [!NOTE]
> Implemented input validation throughout each step of the program. Implemented the view by package parameter feature: to view individual parameters of each package ID. Added more table styling to the new feature. For an overall improved user experience and program functionality. All program requirements / specifications are met.
>

###### 9/30/23 - Added Documentation

> [!NOTE]
> Added documentation for each class and method in the program including the ReadMe Documentation.

###### 10/01/23 - Fixed Input Validation for Package Lookup
> [!NOTE]
> Fixed input validation for the package lookup feature. 
<br><br><br><br>
# Documentation
![#FFA500](https://via.placeholder.com/15/FFA500/000000?text=+) `Project Documentation`
<br><br>
### HashTableWChains Class
This class represents a hash table with chaining implementation.
<br><br>
#### Methods
- `__init__(self, initial_capacity=40)`: Initializes the hash table with an initial capacity. Creates an empty table with empty lists as buckets.
- `insert(self, key, item)`: Inserts an item into the hash table based on the calculated hash value of the key.
- `search(self, key)`: Searches for an item in the hash table based on the key.
- `remove(self, key)`: Removes an item from the hash table based on the key.
- `get_package_id_by_street(self, street)`: Searches for a package in the hash table based on the street address.
<br><br><br><br>
### Packages Class
This class represents a package with various attributes such as ID, street, city, state, zip, deadline, weight, notes, status, departureTime, and deliveryTime.
<br><br>
#### Methods
- `__init__(self, ID, street, city, state, zip, deadline, weight, notes, status='At Hub', departureTime=None, deliveryTime=None)`: Initializes a package object with the given attributes.
- `__str__(self)`: Returns a string representation of the package object.
- `statusUpdate(self, timeChange)`: Updates the status of the package based on the given time change.
<br><br><br><br>
### Trucks Class
This class represents a truck with attributes such as speed, miles, currentLocation, departTime, and packages.
<br><br>
#### Methods
- `__init__(self, speed, miles, currentLocation, departTime, packages)`: Initializes a truck object with the given attributes.
<br><br><br><br>
### Functions
- `loadPackageData(filename)`: Loads package data from a CSV file and inserts it into the packageHash hash table.
- `addresss(address)`: Searches for an address in the addressCSV list and returns the corresponding address ID.
- `Betweenst(addy1, addy2)`: Calculates the distance between two addresses based on the address IDs.
- `truckDeliverPackages(truck, truck_num)`: Simulates the delivery process for a truck.
- `create_and_print_parameter_table(package, param_choice)`: Creates and prints a table with the specified parameter for a package.
- `create_and_print_table(status_logs)`: Creates and prints a table with the status logs.
- `create_and_print_package_table(package)`: Creates and prints a table with the details of a package.
- `log_truck_metrics_with_date(truck, truck_num)`: Generates a string with the metrics of a truck.
- `print_total_metrics(total_distance, total_time_corrected, total_packages_delivered)`: Creates and prints a table with the total metrics of all trucks.
- `main()`: The main entry point of the program.


<br><br>

<br><br>
## Nearest Neighbor Algorithm
![#9900FF](https://via.placeholder.com/15/9900FF/000000?text=+) `Algorithm Analysis`
#### Description
The `truckDeliverPackages` function is a variation of the Nearest Neighbor Algorithm, a Greedy Algorithm used to find the shortest possible route that visits a given set of points.
<br><br>
#### Overview
The function aims to minimize the total travel distance for each truck and effectively deliver all packages assigned to the truck based on the provided constraints.
<br><br>
#### Algorithm Steps
 1. **Initialization:** The function initializes various local variables, such as `en_route` to store packages currently in transit and `status_logs` to store logs of the delivery process.
 2. **Package Assignment:** The function assigns the initial set of packages to the truck and sets their status to `en_route`.
 3. **Delivery Loop:** The function enters a loop where, at each iteration, it selects the nearest package to the current location and delivers it. The loop continues until all packages are delivered.
   - For each package in transit, it calculates the distance to the package and selects the package with the minimum distance.
   - Certain packages have constraints (e.g., package IDs 25, 6) that must be satisfied.
   - After selecting the next package, the function logs the status, updates the truck's location, time, and miles, and marks the package as delivered.
   - The process is repeated until there are no more packages in `en_route`.
 4. **Return to Hub:** After delivering all packages, the truck returns to the hub. The distance to return is added to the total miles, and the return status is logged.
 5. **Status Logs:** The function returns the `status_logs` representing the delivery process of the truck.

<br><br>
#### Pseudocode:

```python
def truckDeliverPackages(truck, truck_num):
    en_route = []  # to hold packages that are in delivery process
    status_logs = []  # to hold the status logs of the delivery process
    
    # add the packages from the truck object to the en_route list
    for package in truck.packages:
        en_route.append(package)
    
    while en_route:  # continue until all packages are delivered
        # find the next package to deliver based on current location and distance to each package's delivery address
        next_package = find_next_package(truck.currentLocation, en_route)
        
        # update status logs and truck attributes
        update_status_and_logs(truck, next_package, status_logs)
        
        # update the status of the delivered package and remove it from en_route list
        next_package.status = "Delivered"
        en_route.remove(next_package)
        
    # calculate the distance to return to the hub and update status_logs and truck attributes
    return_to_hub(truck, status_logs)
    
    return status_logs  # return the status logs of the delivery process
```
<br><br>
### Implementation Details
- The function makes use of helper functions like `addresss` and `Betweenst` to get address indices and calculate distances between addresses, respectively.
- It utilizes the `datetime.timedelta` class to manage and update the time efficiently during the delivery process.
- The function carefully handles the status of each package at different times and logs each status change, including stops, deliveries, and returns.
- Special considerations and constraints are applied for specific package IDs (e.g., package IDs 25, 6).
<br><br>
### Visualization
Prepares a visual representation (a table) of the algorithm's progress using the Rich Library.
<br><br>
### Time Complexity
O($n^2$) due to the nested loops where the algorithm iterates over the packages in transit for each delivery.
<br><br><br><br>
![BigO](https://github.com/opratrx/opratrx/blob/master/big-ochart.png?raw=true)
<br><br><br><br>
### Example
If the truck is at location A, and there are packages to be delivered at locations B, C, and D, the function will calculate the distance from A to B, A to C, and A to D, and select the location with the minimum distance.
