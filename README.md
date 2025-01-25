AN OBSERVATION SCHEDULING SYSTEM FOR RADIO TELESCOPE ARRAY
===
This is an astronomical observation scheduling system, which aims at optimizing the observation plan of the telescope to improve the observation efficiency and quality. The system provides a user-friendly interface, allowing users to select observation targets, set observation parameters and generate observation plans.   
When used, it includes the following functions
* Generate the pitch value trajectory of the target source in the **SOURCE.TXT** file for 24 hours.
* Sort the observation order of the target source in the **SOURCE.TXT** file.
* Generate calibration source trajectory in **source-dingbiao.txt** file (covering all 24 sky regions).
* UV coverage prediction for arrays present in **config_uv.ini** file.
* The above functions can provide results at any time.
* The plot is created using the matplotlib function in Python.
  
Getting started
===
  To understand the target source of execution, you can view the built-in observation file(source.txt/dingbiao.txt).To know array information, you can check the init.txt file.
* After preparing the observation file(source.txt/dingbiao.txt/init.txt), run the main function.
* **PyQt5** is used as its UI interface, and an error occurs when using it. Please update the corresponding database.

Execute program
===
Trajectory fitting
------
*  When you click browse to select the source file to be observed, click the submit button to draw the pitch trajectory diagram of the radio source.
*  The left part of the display information status bar displays the current stellar universal time information, and the right part displays the simulation time of this trajectory fitting, the antenna serial number currently used and the pitch azimuth information of the first radio source.
*  For the address problem, you can manually enter the longitude dimension in the address input field and then click the tracking button and the new address that can be entered to fit the pitch trajectory of the radio source.
  
Intelligent sorting
------
* Enter the observation time on the left side at the bottom of the display information status bar and click the import time button.
* If it is necessary to input the lowest pitch value in the pitch input section, filter out values smaller than this value.
* When modifying the antenna address, enter the new address in the "Address Input" field to replace the default address.
* Click the "Sort" button to select the corresponding file and execute it to obtain the sorted trajectory map.
  
calibration source
---
* After storing the appropriate calibration source in advance in the **source-dingbiao.txt** file, click the "Browse" button in the lower left corner to select the file and obtain the calibration source covering the entire day area.

uv coverage
---
* You can change the start time, end time, step size, array used, and target source of UV coverage in the **config_uv.ini** file
* Click the "UV" button in the bottom right corner of the interface to obtain the UV fixed time coverage map of the array in the **config_uv.ini** file.

Credit
===
If you use **astronomical observation** for research, please cite:
* paper **AN OBSERVATION SCHEDULING SYSTEM FOR RADIO TELESCOPE ARRAY**
Before attributing better methods to software development and maintenance, please consider me as a co-author of the dependent publication

Acknowledgement
===
The uv coverage module was developed based on an integrated VLBI simulator, namely [VNSIM](https://github.com/ZhenZHAO/VNSIM).
