# C950 - WGUPS Delivery Tracking System


The Western Governors University Parcel Service (WGUPS) needs to determine the best route and delivery distribution for their Daily Local Deliveries. The Salt Lake City DLD route has three trucks, two drivers, and an average of 40 packages to deliver each day; each package has specific criteria and delivery requirements.

Your task is to write code that determines and presents a solution delivering all 40 packages, listed in the attached “WGUPSPackage File,” on time, according to their criteria while reducing the total number of miles traveled by the trucks. The “Salt Lake City Downtown Map” provides each address’s location, and the “WGUPS Distance Table” provides the distance between each address (note: mileage on the distance files may not match distances on the map)

The supervisor (user) needs the means to check the status of any given package at any given time using package IDs. The report should also include the **delivery times**, **which packages are at the hub**, and **en route**. The intent is to use this program for this specific location and use the same program in different cities as WGUPS expands its business. As such, you will need to include detailed comments following the industry-standards to make your code easy to read and justifying the decisions you made while writing your program.

## Progress & Updates

> #### 9/26/23 - Initial Commit
>Uploading the current structure of the main components to the software. This commit is the basic functionality of the program before implementing anything further such as the user interface. For the moment, this is a basic layout and foundational draft.
> 
> ---
> #### 9/28/23 - Implemented a Working User Interface
>Implemented a working user interface and will be incorporating a better design in the next few updates. For the time being, this will serve as the first draft of the user interface.
> 
> ---
> #### 9/28/23 - Improved User Interface Using the Textualize Rich Library
>Improving the look and feel of the user interface using the Rich library to oraganize the package delivery process into a data table.
> 
> ---
> #### 9/28/23 - Improved CLI and Added Algorithm Analysis + Status Checks for Each Process in the Algorithm.
>Improving the CLI and added a status check for each step in the process of the Greedy / Nearest Neighbor Algorithm for Analysis.
> 
> ---
> #### 9/29/23 - Added Input Validation, View Package by Parameter, and Improved CLI for UI / UX.
>Implemented input validation throughout each step of the program. Implemented the view by package parameter feature: to view individual parameters of each package ID. Added more table styling to the new feature. For an overall improved user experience and program functionality. All program requirements / specifications are met.
