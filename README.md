ENRICH -- robustnEss aNalysis for tRaffIC sHaping
------------------------------------------------------------------------
ENRICH (robustnEss ANalysis for tRaffIC SHaping) is an approach for identifying non-robust behaviours of Network Traffic Shaping Systems (NTSS). NTSS is composed of a set 𝐶 ={c<sub>1</sub>, . . ., c<sub>n</sub>} of 𝑛 classes. Each class c<sub>i</sub> has a bandwidth range [0..bwR<sub>i</sub>] where bwR<sub>i</sub> is the maximum bandwidth value of the traffic going through c<sub>i</sub>. ENRICH recieves as input a tuple (tr<sub>1</sub>, . . .,tr<sub>n</sub>) where each tr<sub>i</sub> is the bandwidth of the input traffic applied to class c<sub>i</sub>. The output of ENRICH is ranges on input traffics that lead to system’s non-robust behaviours.  ENRICH utilizes our robustness measure, adaptive random testing and machine learning decision trees to characterize non-robust behaviours.

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
On Virtualbox:

1. Add a host-only ethernet adapter (tools -> create). Set the an arbitrary IPv4 address (e.g. 192.168.99.2) and network mask to 255.255.255.0. DHCP server is also disabled.
2. Create a linux-based (Ubuntu 20.04) virtual machine and attach the host-only adapter (which was created in step 1) to the virtual machine using the network tab of the setting. This machine will be the SOHO User (userVM). As a result, one IP is associated to this machine.
3. Create a second linux-based (Ubuntu 20.04) virtual machine and attach the network adapter of the laptop (or any adapter that is used to connect to the internet) to adapter 1 (select bridged adapter at this step). This machine will be the traffic destination (destVM). Define 8 IPv4 addresses on this machine. Later in step 4, we will associate each IP to each NTSS class. To do so, use Network Manager Text User Interface (type ```nmtui``` in terminal) and set 8 IPv4s in the edit connection tab.
4. Create a linux-based (linux 2.6 / 3.x / 4.x) virtual machine and add the OpenWrt disc image to it. Next, in setting/network, attach the newly created host-only adapter to adapter 1, and a bridged adapter to adapter 2. The bridged adapter is the network adapter of the physical machine (or any adapter that is used to connect to the internet). As a result, this machine will have two IPv4 addresses (one denoting adapter 1 and one denoting adapter 2). This machine will be the router (routVM). Note that adapter 2 of routVM and adapter 1 of destVM should be the same. Afterwards, to associate each IP of destVM to each NTSS class (i.e. to prioritize traffic) we need to fist mark the traffics that are routed to each IP. To do so, we modify the firewall rules of OpenWrt. Start by typing ```vim /etc/config/firewall``` in the terminal. This will bring up all the firewall rules of routVM. Add the following lines for each IP of destVM to this file:

``` 
config rule
        list proto 'all'
        option target "DSCP'
        option set_dscp 'CSx' #where x is replaced by 0 to 7 indicating different traffic types
        option src 'lan'
        list dest_ip '192.168.0.xx' #where '192.168.0.xx' is replaced by each ip of destVM
        option name 'NAME' #name of the rule
```
For example, by doing so, we mark the traffic routed to 192.168.0.20 as CS0, to 192.168.0.21 as CS1, ..., to 192.168.0.27 as CS7. Next, we use the diffserv8 mapping of CAKE to specify priorities to each IP (or each CSx class). In other words, differv8 and ``` tc qdisc ``` commands allow us to modify the internal mapping and configurations of NTSS. This part is already done in the code of ENRICH and BASELINE.

Next, we install nuttcp and dpinger:
* Nuttcp is installed on userVm. It can be either downloaded from http://nuttcp.net/nuttcp/nuttcp-8.1.4/nuttcp.c or directly installed by running the following command in terminal ```sudo apt-get install nuttcp```.
* In order to install dpinger on OpenWrt, we need to first follow the steps on building an OpenWrt image in: https://openwrt.org/docs/guide-developer/toolchain/use-buildsystem. Next, we add the code of dpinger as a package to this image and *remake* the image. For simplicity, dpinger code can be added to the userVM by cloning the dpinger github repository (https://github.com/dennypage/dpinger). 

The config file (config.ini) is used to configure the settings of ENRICH and BASELINE codes. The file contains different sections covering information of the VMs (see table below):

<table style="width:40%" class = "center">
  <tr>
    <th>Section</th>
    <th>Information</th>
  </tr>
  <tr>
    <td>routVM</td>
    <td> 
    	<ul>
  			<li>IP of adapter 1 (lan)</li>
  			<li>Username</li>
			<li>Password</li>
  			<li>TotalBandwidth</li>
		</ul>  
    </td>
  </tr>
  <tr>
    <td>userVM</td>
    <td>
      <ul>
        <li>IP of adapter 1</li>
        <li>Username</li>
        <li>Password</li>
      </ul> 
    </td>
  </tr>
    <tr>
    <td>destVM</td>
    <td>
      <ul>
        <li>List of 8 IPs</li>
      </ul> 
    </td>
  </tr>
  <tr>
    <td>dpinger</td>
    <td>
      <ul>
        <li>Path to the report file</li>
        <li>Name of report file</li>
      </ul> 
    </td>
  </tr>
  
</table>
