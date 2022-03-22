ENRICH -- robustnEss aNalysis for tRaffIC sHaping
------------------------------------------------------------------------
ENRICH (robustnEss ANalysis for tRaffIC SHaping) is an approach for identifying non-robust behaviours of Network Traffic Shaping Systems (NTSS). NTSS is composed of a set 𝐶 ={𝑐1, . . .,𝑐𝑛} of 𝑛 classes. Each class 𝑐𝑖 has a bandwidth range [0..bwR𝑖] where bwR𝑖 is the maximum bandwidth value of the traffic going through 𝑐𝑖. ENRICH recieves as input a tuple (tr1, . . .,tr𝑛) where each tr𝑖 is the bandwidth of the input traffic applied to class 𝑐𝑖. The output of ENRICH is ranges on input traffics that lead to system’s non-robust behaviours.  ENRICH utilizes our robustness measure, adaptive random testing and machine learning decision trees to characterize non-robust behaviours.

* Test Generation (1). Generate a set of test inputs for NTSS such that robustness measure for some test inputs is below robustness threshold and for some others is above robustness threshold.
* Model Building (2). Given a test suite build models that help us recognize the conditions under which the system exhibits its non-robust behaviour. We use decision tree regression models in our work.
* Search Space Reduction (3). Using the Regression Tree generated in the second step we find the conditions under which the system reveals its non-robust behaviour. These conditions are then used in the next iteration to reduce the search space and are finally returned as the output of ENRICH. 


<p align="center">
  <img src="https://github.com/baharin/ENRICH/blob/main/ENRICH.PNG" width="400" height="200" class="centerImage" />
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
* OpenWrt 19.0.7 (https://downloads.openwrt.org/releases/19.07.8/targets/x86/64/)
* nuttcp 8.1.4 (http://nuttcp.net/nuttcp/nuttcp-8.1.4/nuttcp.c)
* dpinger (https://github.com/dennypage/dpinger)

Installation Instructions
--------------------------------------------
The following steps show how to setup our simulator for NTSS (SOHOSim) whose architecture is illustrated in the following figure:


![architectureforgithub](https://user-images.githubusercontent.com/25382501/159575154-184381d7-96ef-44e0-a0b2-f847b68c0458.PNG)

