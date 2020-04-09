The purpose of this web tool is to help experimentalists working on the crystallisation of proteins to optimise their hit conditions by efficiently exploring the nearby crystallisation conditions. In initial crystallisation trials, researchers count on the commercial screens to obtain crystals. Once a crystal is obtained, the idea is to optimise these conditions again and again, until they have optimal crystallisation conditions, which give big, well-diffracted crystals most of the times. On each step of this process, we search for conditions in a close range around the hit conditions.

A common struggle during protein crystallisation is that once an initial crystal has been obtained from a commercial screen, the optimisation of the hit conditions is not trivial. The task becomes even more challenging when users try to optimise some of the newest, more sophisticated screens. These screens have many complex conditions and a large number of variables (salts, buffers, precipitant, additives, pH, temperature…). The drawback of these screens are that as the complexity increases, the strangles of designing an optimisation strategy increases as well. This tool is aiming to address this issue using condition search methods: grid search and Latin hypercube sampling. 

## Use OptiScreen Tool 

Try it online [here](https://ramp-mdl.appspot.com)

## Run OptiScreen Tool locally (for development)

Use requirements.txt to install all dependencies: 
```
pip install -r requirements.txt 
pip freeze > requirements.txt 
```

Then you can run the tool using run_RAMPCT.py:
```
python run_RAMPCT.py 
open http://0.0.0.0:8050/
```

## Deploy with gcloud 
To deploy the code in gcloud:
1. Open a virtual environment

2. Install all the requirement packages (requirements.txt)

3. Install [Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-macos) 

4. Connect to gcloud account 

5. Run the following
```
gcloud app deploy 
gcloud browse 
```

## Acknowledgements 
Initial version of this tool was based on [SyCoFinder](https://github.com/ltalirz/sycofinder)

## Contact
For information please contact apostolop.virginia@gmail.com
