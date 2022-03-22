ENRICH -- robustnEss aNalysis for tRaffIC sHaping
------------------------------------------------------------------------
ENRICH (robustnEss ANalysis for tRaffIC SHaping) is an approach for identifying non-robust behaviours of Network Traffic Shaping Systems (NTSS). NTSS is composed of a set 𝐶 ={𝑐1, . . .,𝑐𝑛} of 𝑛 classes. Each class 𝑐𝑖 has a bandwidth range [0..bwR𝑖] where bwR𝑖 is the maximum bandwidth value of the traffic going through 𝑐𝑖. ENRICH recieves as input a tuple (tr1, . . .,tr𝑛) where each tr𝑖 is the bandwidth of the input traffic applied to class 𝑐𝑖. The output of ENRICH is ranges on input traffics that lead to system’s non-robust behaviours.  ENRICH utilizes our robustness measure, adaptive random testing and machine learning decision trees to characterize non-robust behaviours.

* (1) Step1. Test Generation. Generate a set of test inputs for NTSS such that robustness measure for some test inputs is below robustness threshold and for some others is above robustness threshold.
* (2) Step2. Model Building.
* (3) Step3. Search Space Reduction. 


<p align="center">
  <img src="https://github.com/baharin/ENRICH/blob/main/ENRICH.PNG" width="400" height="200" class="centerImage" />
</p>

