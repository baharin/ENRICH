Installation Instructions
--------------------------------------------
The following steps show how to setup our simulator for NTSS (SOHOSim) whose architecture is illustrated in the following figure:

<p align="center">
  <img src="https://github.com/baharin/ENRICH/blob/main/architectureforgithub.PNG" width="400" height="200" class="centerImage" />
</p>
On Virtualbox:

1. Add a host-only ethernet adapter (tools -> create). Set the an arbitrary IPv4 address (e.g. 192.168.99.2) and network mask to 255.255.255.0. DHCP server is also disabled.
2. Create a linux-based (Ubuntu 20.04) virtual machine and attach the created host-only adapter of step 1 to the virtual machine using the network tab of the setting. This machine will be the SOHO User (userVM). As a result, one IP is associated to this machine.
3. Create a linux-based (linux 2.6 / 3.x / 4.x) virtual machine and add the OpenWrt disc image to it. Next, in setting/network, we attach the newly created host-only adapter of step 1 to adapter 1, and a bridged adapter to adapter 2. The bridged adapter is the network adapter of the laptop (or any adapter that is used to connect to the internet). This machine will be the OpenWrt router (routVM). As a result, this machine will have two IPv4 addresses (one denoting adapter 1 and one denoting adapter 2). Afterwards, in order to specify what type of traffic is routed to each IP of destVM, we need to modify the firewall rules of OpenWrt. Start by typing ```vim /etc/config/firewall``` in the terminal. This will bring up all the firewall rules of routVM. Add the following lines for each IP of destVM to this file:

``` 
config rule
        list proto 'all'
        option target "DSCP'
        option set_dscp 'CSx' #where x is replaced by 0 to 7 indicating each class of NTSS
        option src 'lan'
        list dest_ip '192.168.0.xx' #where dest_ip is replaced by each ip of destVM
        option name 'NAME' #name of this rule
```
4. Create another linux-based (Ubuntu 20.04) virtual machine and attach the network adapter of the laptop (or any adapter that is used to connect to the internet) to adapter 1 (select bridged adapter at this step). This machine will be the traffic destination (destVM). Define 8 IPv4 addresses on this machine where each IP is associated to each NTSS class. To do so, use Network Manager Text User Interface (type ```nmtui``` in terminal) and set 8 IPv4s in the edit connection tab. Note than adapter 2 of routVM and adapter 1 of destVM should be the same.


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

