# bring in the libs we need
import requests
from bs4 import BeautifulSoup
from pprint import pprint

# purley for printing to the terminal
def debug(x):
    print("-"*50)
    pprint(x)
    print("-"*50)

# remove any non-number elements from the strings
# return int
def clean_numbers(n):
    return int(n.replace("%", "").n.replace(",", ""))

# the main function that does the heavy lifting
def get_zipcodes():
    # I got these zipcodes from google
    fh = open("zipcodes.csv", "r")
    zips = fh.read().split("\n")
    fh.close()

    # the csv header
    rows = ["Female Total", "Female Percentage", "Male Total", "Male Percentage", "Zipcode", "Grand Total"]
    for z in zips:
        # THANK GOD the url was consestent and easy to just append the zipcode to it
        # else this would have been a lot harder since the main page on their website
        # is paged and triggered with JS. requests wouldn't have worked.
        url = f"http://worldpopulationreview.com/zips/west-virginia/{z}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # grab the element we want via it's selector. Found this by viewing the source of the page
        data = soup.select(".section-container > div:last-child")
        if data:
            # target the actual elements we want
            target_data = data[2].findChildren()

            # run one of the numbers we found through the clean function
            # if it returns None, we know there was no data, or bad data, so skip it
            if clean_numbers(target_data[2].text):
                rows.append([
                    clean_numbers(target_data[2].text),
                    clean_numbers(target_data[4].text),
                    clean_numbers(target_data[8].text),
                    clean_numbers(target_data[10].text),
                    z,
                    clean_numbers(target_data[2].text) + clean_numbers(target_data[8].text)
                ])

                # this is purley for printing the data to the terminal and not needed
                # but having the live feedback is nice
                json = {
                    "female_total": target_data[2].text.replace(",", ""),
                    "female_percentage": target_data[4].text.replace("%", ""),
                    "male_total": target_data[8].text.replace(",", ""),
                    "male_percentage": target_data[10].text.replace("%", ""),
                    "zipcode": z,
                    "total": int(target_data[2].text.replace(",", "")) + int(target_data[8].text.replace(",", ""))
                }
                debug(json)

    # our file for outputting what we grabbed
    out = open("output2.csv", "a")
    for row in rows:
        # convert the int's back to strings so we can joing them by a comma
        # and written to the output file
        out.write(",".join(map(str,row))+"\n")
    out.close()

# actually start the crawling
# since this is a one off script, I'm not making this a class
# nor making it a module, so just stright calling the function is fine here
get_zipcodes()