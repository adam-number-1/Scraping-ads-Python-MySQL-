# Scraping-ads-Python-MySQL-
This is a project, where I scrape rental ads from a for-rent-by-owner site using the Beautiful soup library in Python. The script is looking for specific information in the ad like where it is, what is the size, floor number etc. Then it loads the data on a MySQL server using the SQLalchemy connector.

There is also a MySQL script, which takes the data on the server and creates several views out of them. The views are later on visualized on my website, you can see the result here in the link below:

https://adam-s.cz/rent-en

For the visualization, I just used free wordpress SQL plugin, which connects to my database and visualizes whatever queries I put into it.

https://wordpress.org/plugins/sql-chart-builder/

The script is supposed to run frequently, once a day seems to be the ideal frequency. Initially, the script needs to be run mannually by the user, but changes will be made in order to ideally deploy the script on some platform, where it will be executed regularly.
