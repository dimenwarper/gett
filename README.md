gett
====

Install instructions
-----

* Download/clone from github: `git clone https://github.com/dimenwarper/gett.git`
* Setup an environment variable `GETT_HOME` that points to the directory where gett lives: `export GETT_HOME:/path/to/gett/`
* Put `GETT_HOME/bin/` in your `PATH`: `export PATH=$PATH:$GETT_HOME/bin`
* Change directory to `GETT_HOME` and do: `python setup.py install`
* To run gene network inference algorithms that depend on the JGL package (e.g. clip), you need to install gett's version of JGL. To do this, change directory to `GETT_HOME/external` and do `R CMD INSTALL JGL`.
* Do a test run by running the get command: `gett`

How to run
----

The genotype, expression, and trait toolkit

Main usage is through the gett executable, e.g. as follows

`gett datasets/magnet/full_exp_cases.txt datasets/magnet/full_exp_controls.txt --correctcovariates datasets/magnet/all_sample_covariates.txt datasets/magnet/all_sample_covariates.txt --zscores --selectbyvariance 0.2 --clip --savesteps --outdir /my/outdir/`


The line above will take two trait matrices (rows are traits with first field being trait name e.g. gene names and gene expression values and columns are samples [with a header]) contained in full_exp_cases.txt and full_exp_controls.txt and will correct the values for the covariates using robust linear regression (default) included in all_sample_covariates.txt (in the same format as trait matrices) and will then take only the top 20% traits with most variance and then normalize trait-wise using z-scores. After that, the CLIP analysis will be run (with the --clip flag, you can run other analyses with e.g. --jgl [for the joint graphical lasso, see link http://arxiv.org/pdf/1111.0324v4.pdf], --pcor, --cor, etc.). The --savesteps flag will save intermediary files (e.g. one file for the covariance-corrected, then normalized, etc.). Every result will be saved in the the /my/outdir directory due to the --outdir argument.
The above yields two files, one with the community memberships and one with the edges in the network (and weights).

After that, you can use the following script to get the network statistics:

`python $GETT_HOME/scripts/network_statistics.py full_exp_cases.txt output/full_exp_cases.txt.communities output/full_exp_cases.txt.edges`

This will generate network statistics files in current directory in a file called summary.txt. Do the same thing for all your trait matrices.
You can then compare statistic summary files with 

`python $GETT_HOME/scripts/score_summary_files.py summary_cases.txt summary_controls.txt outdir/`

Which will use lc and gc to score the traits and produce a final score file in outdir/


Format of input files
------

Almost all files are tab-delimited.
* For trait matrices, you have to have a header file with your sample names (tab-delimited), and then one row for each trait, that starts with your trait name (e.g. gene symbol for expression traits), and their values per samples (as in header), also tab-delim.
* Covariate matrices have the same format as trait matrices.
