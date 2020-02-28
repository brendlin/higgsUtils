higgsUtils - An Introduction to the Package
================

Initial setup
==================

To get started, simply check out the package from git, and run the following commands
(or put them in your `.bash_profile` script):

     export PYTHONPATH=$PYTHONPATH:/path/to/higgsUtils/python
     export PYTHONPATH=$PYTHONPATH:/path/to/higgsUtils/genericUtils/python
     export PATH=$PATH:/path/to/HggStarUtils/genericUtils/macros

(This appends the python directories to PYTHONPATH, and makes the genericUtils/macros executable from
any directory.) Now you can run these scripts in any directory:

    cd testarea
    SpuriousSignal.py ...

And that's it - you're ready to go!



**BackgroundReweighting.py** - Description and Instructions
==================

### What is it

This script takes yy AF2, plus data from yj and jj control regions, and finally a text file containing
the relative fractions of yy, yj and jj, in HGam Couplings categories.

It finds linear reweightings to get the AF2 to match yj and to match jj (separately). Then it applies
the reweightings, along with the relative fractions, into a final reweight result. It uses a TF1 to
derive this reweighting.

### How to run it

The syntax is:
```
BackgroundReweighting.py --af2 AF2.root --yj yj.root --jj jj.root --fractions fractions.txt
```
where the fractions.txt file is of the form (ordered by yy, yj, jj, and in %):

```
Baseline               78.7   18.7  2.6
M17_ggH_0J_Cen         79.3   18.8  1.9
M17_ggH_0J_Fwd         75.2   21.3  3.5
M17_ggH_1J_LOW         79.5   18.0  2.6
M17_ggH_1J_MED         83.3   15.5  1.1
M17_ggH_1J_HIGH        87.4   12.2  0.4
...
```

The root files contain TH1s for each category. They are hard-coded for a particular case
(HGam couplings), but if it is useful then this can be made more generic.

**SpuriousSignal.py** - Description and Instructions
==================

### What is it

### How to run it

**ChiSquare.py** - Description and Instructions
==================

### What is it

### How to run it

**FtestStudies.py** - Description and Instructions
==================

### What is it

### How to run it

