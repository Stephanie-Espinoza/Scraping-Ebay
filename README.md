# Scraping-Ebay

The ebay-dl.py program extracts the name, price, shipping cost, free returns, items sold, and product status of an item on ebay and puts the information together in a JSON or CSV file. 

To run the ebay-dl.py program you should include a search term at the end in quotation marks and if you want to search through a specific number of pages, include that as well. The example below is what I included in my terminal when running the program for 'erasable pens', 'camera', and 'notebook'. This will look different for everybody based on your directory, your search term, and the number of pages you are running through. 

```
$ /usr/local/bin/python3 /Users/stephanie/Desktop/CSCI040/ebay-dl.py 'erasable pens' 
```
```
$ /usr/local/bin/python3 /Users/stephanie/Desktop/CSCI040/ebay-dl.py 'camera' 
```
```
$ /usr/local/bin/python3 /Users/stephanie/Desktop/CSCI040/ebay-dl.py 'notebook'
```

If you want to only run the program through one page you could include the following in your command:
```
$ /usr/local/bin/python3 /Users/stephanie/Desktop/CSCI040/ebay-dl.py 'notebook' --num_pages=1
```

If you want to put the data into a CSV file, add --csv at the end of your command. For example:

```
$ /usr/local/bin/python3 /Users/stephanie/Desktop/CSCI040/ebay-dl.py 'erasable pens' --num_pages=1 --csv
```


This is a [project](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03) for CSCI040 at Claremont McKenna College. 
