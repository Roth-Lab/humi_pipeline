Software Instructions for manuscript Eirew et al, Accurate determination of CRISPR-mediated gene fitness in transplantable tumours

The code pipeline to infer guide fitness from pooled in vivo screens is available for download from https://github.com/aroth85/humi_pipeline. Full instructions for installation (including dependency Snakemake), format of input files and run time options and is provided there. Installation should take 15-30 minutes.

The code uses the probabilistic programming language BLANG. Prerequisites are Conda, Python and Snakemake. The code has been tested on standalone machines running MacOS version 10.14 Python version 3.9.1, and on a server running CentOS Linux version 6.7 and Python version 3.8.3.

A sample set of datasets are downloaded along with the code, into subdirectory humi_pipeline/examples. These contain data from three replicate transplants carried out from PDX line C2271. Instructions are provided to run a batch of three individual fitness inference runs (one for each dataset), along with a grouped fitness inference run using data from all three. The pipeline will take a few hours to run. Results are created in a destination directory specified by the user, including the following files of particular interest:    - tables/estimates/frequentist
     Delta model fitness estimates and confidence intervals for each sgRNA 
   - tables/estimates/bayes      Bayesian model fitness estimates and credible intervals for each sgRNA 
  -  trace/unpacked/<dataset name>/samples      value of each Bayesian model parameter at each Markov chain Monte Carlo (MCMC) sample, which can be used to examine the shape of parameter posterior distributions. For example, the file conditionalWinsorizedMeans.csv contains the post-winsorization fitness estimate of each sgRNA in each MCMC sample. The set of parameters estimated depend on the distribution model specified (e.g. mix-nb).

  -  plots/poset   -  poset/experiment      Partially ordered set (poset) Hasse diagrams connecting a minimal set of sgRNA pairs with non-overlapping credible intervals, and the corresponding directed graph .dot files

For further information or questions on the code, please contact Dr Andrew Roth (aroth@bccrc.ca) or Dr Alexandre Bouchard-Cote (bouchard@stat.ubc.ca).
