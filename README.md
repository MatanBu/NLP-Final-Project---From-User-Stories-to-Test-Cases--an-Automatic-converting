FINAL-PROJECT
=
From User Stories to Test cases - an Automatic converting
-


The project team choose to research and develop a tool for analyzing and automatically customizing user stories for test cases using natural language processing technologies (NLP).

In the current state of the industry, the test cases and scripts themselves are written manually, drawing on the customer requirements derived from user stories. 
This manual process is exhausting and takes up 40-70% of the test cycle time (Joglekar, 2014), and many times the client changes his requirements during the work and therefore re-writes the test cases according to the new requirements. 
Another problem is writing test cases that do not meet the requirements, due to a lack of familiarity with the system or inexperience. 
Any writing and modification of the test cases requires manual updating of the test scripts.

In order to deal with the problems mentioned above, we will endeavor to automatically adjust the test cases, as required, to shorten the working time on the test cases and, as a result, shorten the re-writing time in the event of changing the requirements of the client. In addition, automating test case adaptation to user stories will obviate the need for early review of the system and minimize errors caused by it.

The automation process include the text processing of the user story and then the adjustment of test cases from the repository. The text processing will be performed by Natural Language Processing Tools (NLP) and to streamline the process user stories will be written in a predefined format.

The purpose of this work is to develop a tool for converting user stories into test cases by using natural language processing (NLP) as well as to fully understand the process that begins with receiving user stories and ending with test cases and tests, and finally embedding the solution in the system that will perform the entire process efficiently and optimally.


Summary
=
The system is part of the process of writing test scripts automatically. The ultimate goal is to make the test case writing process automatic.

The main goal of the current system is to address test scripts that exist from previous projects, to shorten the time allocated for writing test scripts and to reduce manpower in this activity. The system extensively searches the databases where test scripts are stored and pulls out the most appropriate ones when needed.

Another requirement is the use of standard quality metrics Precision, Recall, Accuracy to enable quantitative measurement and comparison of the different results.

The system will be implemented at Amdocs and adjusted to the business values ​​and the companies with which the company works; The system will sit inside the Amdocs internal network and will not have external access. The system will also be implemented on an existing infrastructure and will be written on the enterprise computers that contain Windows 10 The system will also write in Python, in the Eclipse development environment.

The system is done as part of a final project. Platforms that Amdocs works with or are provided by the college will be used, or open source platforms. Resources are needed such as a database for work, a position from Amdocs for ongoing work, as well as meetings with the designated professionals at Amdocs for knowledge of the systems and future support.


Tools
=
![alt text](https://imgur.com/uJ3TaV4.png)

o	Eclipse Oxygen

o	Python 3.6

o	Spacy

o	NLTK

o	scikit-learn

o	PyQt5

o	sciPy

o	TextBlob


The procces
=
![alt text](https://imgur.com/y3u0Yvj.png)

Results visualization
=

Single user-story matching
-
Displaying the match results between the selected user story and the test cases loaded from the data repository The presentation will be in the form of a table centering the data as well as in a graph configuration that allows you to see the relationship between the matches and the different test cases, as illustrated.

![alt text](https://imgur.com/vWxmNaK.png)


Entire database matching
-
For run of the entire database, we will display a graph that shows the relationships between the user stories and all test cases. The graph allows you to see the distribution of test cases for the different user stories.

![alt text](https://imgur.com/5sxIQ91.png)


LDA comparison
-
For a comparison using the Topic modeling (LDA) method, an output file is created which displays the distribution of the text words for the various topics in an intuitive graph which allows the data to be clearly displayed to the user.

![alt text](https://imgur.com/cptrpTZ.png)
