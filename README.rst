WSU-SIBI-Prereq-Check
=====================

You need to:
------------

1. Install the `github app <https://desktop.github.com/>`__.

   -  You don’t need to make an account (anymore). **Please don't**. (regular github users are fine- but adding an account for those who aren't will just create more confusion)

3. `Install Python <https://www.anaconda.com/download/>`__

   -  You should see a big green button under *Python 3.6 version*.
      Click it and agree to all of it.

3. Decide where you want this. I suggest inside your documents folder, make a folder named ``prerequisite_checks``. Inside that folder, make a folder called ``SIBI_Reports`` (no spaces).

4. Please create the ``prerequisites.xlsx`` file- put it inside ``prerequisite_checks``.

   -  Each column header is the name of the  course, each row below is a
      required prerequisite. If prerequisites can be satisfied multiple
      ways, add more columns for the course (as per the example… which
      is a fictitious example).
   -  Each column represents a different way to satisfy the prerequisites.
   -  You should likely name it EE_prerequisites.xlsx or such. Whatever
      you name it, leave it where it is. No changing after I visit to
      set up.

   For example, the Excel file ``prerequisites.xlsx`` contains the following:

   +---------+---------+--------+----------+
   | ME2120  | ME2120  | ME3120 | ME4321   |
   +=========+=========+========+==========+
   | EGR1010 | MTH1234 | ME2120 | ME3210-C |
   +---------+---------+--------+----------+
   | ME1040  |         |        |          |
   +---------+---------+--------+----------+

   This means that:

      -  there are two ways to satisfy the prerequisites for ME2120 (**no space allowed**):
        -  Either MTH234
        -  or (ME1040 and EGR1010).
      -  there is one way to satisfy the prerequisites for ME3120: ME2120.
      -  there is one way to satisfy the prerequisites for ME4321: a C grade or higher in ME3210
      


5. Create a transfer spreadsheet

   -  This is useful for

      -  Temporary acknowledgment of prerequisite fulfillment prior to
         transfer credits being posted
      -  Graduate students who don’t have undergraduate courses
         transferred and evaluated formally.

   -  An example is given as `Student_prerequisite_data_Example.xlsx <https://github.com/josephcslater/WSU-SIBI-Prereq-Check/blob/master/Student_prerequisite_data_Example.xlsx>`_ (click on the link to download it).
   -  Put the file inside ``prerequisite_checks``.
   -  This spreadsheet allows you to note that you’ve agreed that a
      course requirement has been completed **for the sake of satisfying
      prerequisites**.
   -  This is useful when considering transfer students whose
      transcripts have yet to post so that you avoid false warnings.
   -  **You don’t have to use it, but you must provide the empty one
      (where you may add to it later)**.

Usage
-----

Once this is all set up **by me**, you:

-  Put your **raw unedited**[1] SIBI reports inside ``SIBI_Reports`` (I know, right?)

  -  Method 1:

    -  Select ``Anaconda Prompt`` from your Windows menu.

  -  Method 2:

    -  Double click on the file named ``Check_Prerequisites.py``.

-  Watch the text go by until it tells you that it's done.

-  Close the window and enjoy your refined results.

This won’t complete the process, I will have to:
------------------------------------------------

-  Install the WSU-SIBI package
   -  Run the ``Anaconda Prompt`` (now on your windows start menu, in the ``Anaconda3`` folder)
   -  ``execute pip install -e .`` in the root directory for the prerequisite package.
-  Run the Jupyter notebook and configure to your settings
-  Save the script and notebook to a better location.
-  Edit the ``ipython`` lines out of the script file.
-  Edit ``activate.bat`` in the folder (Sometimes located elsewhere- run anaconda prompt and it will briefly show at the top of the window)

   ``C:\Users\(username)\AppData\Local\Continuum\anaconda3\Scripts``
   and add the line
   
   ``python (pathto)Check_Prerequisites.py``.
-  Demonstrate how to use it.

However, doing all of the above will mean that we won’t have to wait
while I do the above things for you (or worse, we don’t have the files
ready and I have to come back later.).

[1] You know who you are... don't!

.. _`this link`: x-github-client://openRepo/https://github.com/josephcslater/WSU-SIBI-Prereq-Check
