ENRICH -- robustnEss aNalysis for tRaffIC sHaping
------------------------------------------------------------------------
ENRICH (robustnEss ANalysis for tRaffIC SHaping) is an approach for identifying non-robust behaviours of Network Traffic Shaping Systems (NTSS). NTSS is composed of a set 𝐶 ={𝑐1, . . .,𝑐𝑛} of 𝑛 classes. Each class 𝑐𝑖 has a bandwidth range [0..bwR𝑖] where bwR𝑖 is the maximum bandwidth value of the traffic going through 𝑐𝑖. ENRICH recieves as input a tuple (tr1, . . .,tr𝑛) where each tr𝑖 is the bandwidth of the input traffic applied to class 𝑐𝑖. The output of ENRICH is ranges on input traffics that lead to system’s non-robust behaviours.  ENRICH utilizes our robustness measure, adaptive random testing and machine learning decision trees to characterize non-robust behaviours.

* <p> <b> Test Generation (1). </b> Generate a set of test inputs for NTSS such that robustness measure for some test inputs is below robustness threshold and for some others is above robustness threshold. </p>
* <p> <b> Model Building (2). </b> Given a test suite build models that help us recognize the conditions under which the system exhibits its non-robust behaviour. We use decision tree regression models in our work. </p>
* <p> <b> Search Space Reduction (3). </b> Using the Regression Tree generated in the second step we find the conditions under which the system reveals its non-robust behaviour. These conditions are then used in the next iteration to reduce the search space and are finally returned as the output of ENRICH. </p>


<p align="center">
  <img src="https://github.com/baharin/ENRICH/blob/main/ENRICH.PNG" width="450" height="200" class="centerImage" />
</p>

License 
--------------------------------------------
add license here

Content Description
----------------------------------------------
add description here

Prerequisite
---------------------------------------------
add prerequisite here
* Python 3.8.10
* Virtual Box 6.1
* Ubuntu 20.04 disc image (https://ubuntu.com/download/desktop)
* OpenWrt 19.0.7 (https://downloads.openwrt.org/releases/19.07.8/targets/x86/64/)
* nuttcp 8.1.4 (http://nuttcp.net/nuttcp/nuttcp-8.1.4/nuttcp.c)
* dpinger (https://github.com/dennypage/dpinger)

Installation Instructions
--------------------------------------------
The following steps show how to setup our simulator for NTSS (SOHOSim) whose architecture is illustrated in the following figure:

<p align="center">
  <img src="https://github.com/baharin/ENRICH/blob/main/architectureforgithub.PNG" width="400" height="200" class="centerImage" />
</p>

1. Add a host-only ethernet adapter (tools -> create). Set the an arbitrary IPv4 address (e.g. 192.168.99.2) and network mask to 255.255.255.0. DHCP server is also disabled.
2. Create a linux-based (Ubuntu 20.04) virtual machine and attach the created host-only adapter of step 1 to the virtual machine in the network tab of the setting. This machine will be the SOHO User (userVM). MENTION THIS VM HAS ONE IP.
3. Create another linux-based (Ubuntu 20.04) virtual machine and attach the network adapter of the laptop (or any adapter that is used to connect to the internet) to adapter 1 (select bridged adapter at this step). This machine will be the traffic destination (destVM). MENTION 8 IPS HERE.
4. Create a third linux-based (linux 2.6 / 3.x / 4.x) virtual machine and add the OpenWrt disc image to it. Next, go to setting/network and set adapter 1 to the host-only ethernet adapter, and adapter 2 to bridged adapter and select the network adapter of the laptop. This machine will be the OpenWrt router (routVM).
Note than adapter 2 of routVM and adapter of destVM should be the same. MENTION THAT THIS MACHINE HAS TWO IPS. MENTION HOW TO ADD THE MAPPING IN FIREWALL RULES.

Next, we install nuttcp and dpinger:
* Nuttcp is installed on userVm. It can be either downloaded from http://nuttcp.net/nuttcp/nuttcp-8.1.4/nuttcp.c or directly installed by running the following command in terminal ```sudo apt-get install nuttcp```.
* In order to install dpinger on OpenWrt, we need to first follow the steps on building an OpenWrt image in: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem. Next, we add the code of dpinger as a package to this image and *remake* the image. For simplicity, dpinger code can be added to the userVM as well. 

The config file (config.ini) is used to configure the setting of the ENRICH code. The file contains different sections covering information of the VMs (see table below):
