
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

from prereqcheck.prereqcheck import *
import prereqcheck.prereq_config as prc


# In[2]:


# This is the name of your prerequisites file, including path.
prereqfilename = '/Users/jslater/Desktop/SIBI_Reports/BIE prereqs all UG_050118.xlsx'
print(prereqfilename)

# This is the name of your prerequisites file, including path.
# It has to exist, but it can be empty (no useful information)
transfer_filename = "/Users/jslater/Documents/OneDrive - Wright State University/Chair-OneDrive/PrereqData/Student_prerequisite_data.xlsx"
print(transfer_filename)

# This next cell sets the location of your reports.
# It will process all of the reports in this directory.
os.chdir('/Users/jslater/Desktop/SIBI_Reports')
print(os.getcwd())


# In[3]:


check_prerequisites(prereqfilename = prereqfilename,
                    transfer_filename = transfer_filename,
                    majordict = majordict)


# Ignore all of this down here. For my reference.

# In[4]:


prereqdict = load_prerequisites(prereqfilename=prereqfilename)
