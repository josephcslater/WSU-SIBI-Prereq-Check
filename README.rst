WSU-SIBI-Prereq-Check
=====================

You need to:
------------

1. Install the `github app <https://desktop.github.com/>`__.

   -  You don’t need to make an account (anymore)

2. `Clone this
   repository <x-github-client://openRepo/https://github.com/josephcslater/WSU-SIBI-Prereq-Check>`_
   (Just click on `this link <x-github-client://openRepo/https://github.com/josephcslater/WSU-SIBI-Prereq-Check>`_)

   -  When it asks you where to put it, put it in your documents folder,
      or a reasonable subfolder **that you will remember**.

3. `Install Python <https://www.anaconda.com/download/>`__

   -  You should see a big green button under *Python 3.6 version*.
      Click it and agree to all of it.

4. Please edit the ``prerequisites.xlsx`` file.

   -  Each column header is the name of the course, each row below is a
      required prerequisite. If prerequisites can be satisfied multiple
      ways, add more columns for the course (as per the example… which
      is a fictitious example).
   -  Each column represents a different way to satisfy the prerequisites.
   -  You should likely name it EE_prerequisites.xlsx or such. Whatever
      you name it, leave it where it is. No changing after I visit to
      set up.

   For example, the Excel file contains the following:

   +---------+---------+--------+
   | ME2120  | ME2120  | ME3120 |
   +=========+=========+========+
   | EGR1010 | MTH1234 | ME2120 |
   +---------+---------+--------+
   | ME1040  |         |        |
   +---------+---------+--------+

   This means that there are two ways to satisfy the prerequisites for
   ME2120 (**no space allowed**): Either MTH234 or (ME1040 and EGR1010).
   There is one way to satisfy the prerequisites for ME3120: ME2120.
5. Create a transfer spreadsheet

   -  This is useful for

      -  Temporary acknowledgment of prerequisite fulfillment prior to
         transfer credits being posted
      -  Graduate students who don’t have undergraduate courses
         transferred and evaluated formally.

   -  An example is given as ``Student_prerequisite_data_Example.xlsx``
   -  This spreadsheet allows you to note that you’ve agreed that a
      course requirement has been completed **for the sake of satisfying
      prerequisites**.
   -  This is useful when considering transfer students whose
      transcripts have yet to post so that you avoid false warnings.
   -  **You don’t have to use it, but you must provide the empty one
      (where you may add to it later)**.

This won’t complete the process, I will have to:
------------------------------------------------

-  Install the package that you downloaded
-  Run the notebook and configure to your settings
-  Demonstrate how to use it.

However, doing all of the above will mean that we won’t have to wait
while I do the above things for you (or worse, we don’t have the files
ready and I have to come back later.).
