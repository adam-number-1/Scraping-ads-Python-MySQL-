from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
from datetime import date
import sqlalchemy

# function, which updates the rent in the active ads
def update_rent(ad_link):
    page = requests.get(ad_link)
    page_content = BS(page.content,"html.parser")
    new_rent = (int([x.get_text() for x in page_content.find("table" , class_="PriceTable_priceTable__voQsR priceTable").find_all("tr")][0][16:-3].replace("\xa0","")))
    return new_rent


# list of regions I observe. 
url_list = []
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R429461&osm_value=Hole%C5%A1ovice%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R20000061612&osm_value=Praha+1%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R429381&osm_value=Sm%C3%ADchov%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R20000063928&osm_value=Praha+2%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R20000063962&osm_value=Praha+3%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R435856&osm_value=Karl%C3%ADn%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R428842&osm_value=Vr%C5%A1ovice%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R434063&osm_value=Nusle%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")
url_list.append("https://www.bezrealitky.cz/vyhledat?offerType=PRONAJEM&estateType=BYT&order=TIMEORDER_DESC&regionOsmId=R428823&osm_value=Vy%C5%A1ehrad%2C+Praha%2C+okres+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha%2C+Praha%2C+%C4%8Cesko&roommate=false&page=")


# in the "links" list will be all of the links scrapped from the region pages above
links = []

# iterating through all the regions
for region in url_list:
    page_no = 1

    # every region page has unknown number of catalog pages. I need to iterate through the catalog pages until no links are scraped
    while True:
        temp_links= []
        # for each catalog page, I will take the whole content
        page = requests.get(region + str(page_no))
        page_content = BS(page.content,"html.parser")

        # each catalog page has <article> contaier, which serves as a property card, which contains link to the ad etc.
        # i need to take from the content all these <article> containers
        prop_cards = page_content.find_all("article", class_="PropertyCard_propertyCard__qPQRK propertyCard PropertyCard_propertyCard--landscape__7grmL")
        #then I need to get the ad links from each of this <article> containers
        for i in prop_cards:
            temp_links.append(temp_links.append(i.find("a", href=True)["href"]))

        # if the list of links from the catalog subpage is empty, it means I already have all the links from that region and it is time to move on
        if len(temp_links)==0:
            break
        
        # probably somewhere in the code of the site the containers have more <a> elements, which don´t include the "href", and these give me "None" links
        # I need to get rid of those
        for link in [x for x in temp_links if x != None]:
            links.append(link)
        page_no +=1

# this is just a DF from the links list, so I can in convenient way put into csv
new_links_df = pd.DataFrame({"LINK" : links})

# connection to DB
engine = sqlalchemy.create_engine("mysql://adamsczrental_db:Hyp83AEeTA@uvdb56.active24.cz:3306/adamsczrental_db")

# loading links scraped from the site during previous session and the already processed ads
previous_links = pd.read_sql("previous_session", con = engine)
processed_ads = pd.read_sql("processed_ads", con = engine)

# finding the difference between links from current session and previous one - new unique unprocessed links (or ads)
links = (new_links_df.loc[~new_links_df["LINK"].isin(previous_links["LINK"])]["LINK"]).tolist()

# then I will take all the new live links and will find property information
# create a dictionary to make a DF of the new links links
# I will create the columns in this order: (index), LINK, LISTED BEFORE, DELISTED BEFORE, DESCRIPTION, DISTRICT, STREET
# LAYOUT, SIZE, RENT, FLOOR, BUILDING TYPE, BALCONY, TERRACE, FURNISHED, ELEVATOR, POSITION, NEWBUILT
new_links_dict = {}

# create the unique ID and LLINK lists
new_links_dict["ID"] = list(range(1,len(links)+1))
new_links_dict["LINK"] = links

# create the LISTED_BEFORE - this is easy, because it is whatever date this script is run
new_links_dict["LISTED_BEFORE"] = [date.today()] * len(links)

# create the DELISTED_AFTER - THESE ADS WERE JUST FOUD, SO it will be as NaT
new_links_dict["DELISTED_BEFORE"]  = [pd.NaT] * len(links)

# other lists of default values
new_links_dict["DESCRIPTION"] = ["N-A"] * len(links)
new_links_dict["DISTRICT"] = ["N-A"] * len(links)
new_links_dict["STREET"] = ["N-A"] * len(links)
new_links_dict["LAYOUT"] = ["N-A"] * len(links)
new_links_dict["SIZE"] = [0] * len(links)
new_links_dict["RENT"] = [0] * len(links)
new_links_dict["FLOOR"] = ["N-A"] * len(links)
new_links_dict["BUILDING_TYPE"] = ["N-A"] * len(links)
new_links_dict["BALCONY"] = ["N-A"] * len(links)
new_links_dict["TERRACE"] = ["N-A"] * len(links)
new_links_dict["FURNISHED"] = ["N-A"] * len(links)
new_links_dict["ELEVATOR"] = ["N-A"] * len(links)
new_links_dict["POSITION"] = ["N-A"] * len(links)
new_links_dict["NEWBUILT"] = ["N-A"] * len(links)

# catch phrases in description text to look for to guess, if the real estate has the attribute or not
elevator_phrases = ["nový výtah" , "s výtahem", "je výtah", ", výtah", ",výtah", "novým proskleným výtahem", "novým výtahem", "disponuje výtahem", "dostupný centrálním výtahem"]
no_elevator_phrases = ["není výtah", "bez výtahu" , "není zde výtah", "není tu výtah", "není výtah", "nenachází výtah", "nenachází se zde výtah"]

# create the DESCRIPTION - this is first of the columns, where I need to get each ads content and find the information in it
for link_index in range(len(links)):
    page = requests.get(links[link_index])
    page_content = BS(page.content,"html.parser")

    description_text = "".join([x.get_text() for x in page_content.find("div", class_="box mb-8").find_all("p")])
    new_links_dict["DESCRIPTION"][link_index] = description_text 
    

    # create the DISTRICT
    street_district = (page_content.find("span", class_="PropertyAttributes_propertyAttributesItem__kscom").find("a", href=True).get_text()).split(" - ")
    new_links_dict["DISTRICT"][link_index] = street_district[1]

    # create STREET
    if street_district[0] != " Praha":
        new_links_dict["STREET"][link_index] = street_district[0].split(", ")[0]

    # rent attribute   
    new_links_dict["RENT"][link_index] = (int([x.get_text() for x in page_content.find("table" , class_="PriceTable_priceTable__voQsR priceTable").find_all("tr")][0][16:-3].replace("\xa0","")))
    

# other attributes - there is a table I am scraping and I need to iterate through each of its rows
    for par_table in (page_content.find_all("div", class_="ParamsTable_paramsTableGroup__IIJ_u")):
        for row in [x.get_text() for x in par_table.find_all("tr")]:
        
            if "Dispozice" in row:
                new_links_dict["LAYOUT"][link_index] = row[9:]
                
            if "Podlaží" in row:
                new_links_dict["FLOOR"][link_index] = row[7:]   
                
            if "Typ budovy" in row:
                new_links_dict["BUILDING_TYPE"][link_index] = row[10:] 
                
            if "Plocha" in row:
                new_links_dict["SIZE"][link_index] = int(row[6:-3]) 

            if "Vybaveno" in row:
                new_links_dict["FURNISHED"][link_index] = row[8:] 
                
            if "Výtah" in row or any([phrase in description_text.lower() for phrase in elevator_phrases]):
                new_links_dict["ELEVATOR"][link_index] = "Yes" 
                
            elif any([phrase in description_text.lower() for phrase in no_elevator_phrases]):
                new_links_dict["ELEVATOR"][link_index] = "No"
               
            if "novostav" in description_text.lower():
                new_links_dict["NEWBUILT"][link_index] = "Yes"
                
            if any([phrase in description_text.lower() for phrase in ["balkón", "balkon", "lodž"]]) or any([phrase in row for phrase in ["Balkón", "Lodžie"]]):
                new_links_dict["BALCONY"][link_index] = "Yes"
                
            if "teras" in description_text.lower() or "Terasa" in row:
                new_links_dict["TERRACE"][link_index] = "Yes"
            if "přízem" in description_text.lower():
                new_links_dict["POSITION"][link_index] = "Groundfloor"
            elif "půdn" in description_text.lower():
                new_links_dict["POSITION"][link_index] = "Attic"

new_ads_df = pd.DataFrame(new_links_dict)

# this is checking, if some ad wasn´t found in the latest search and changes DELISTED_BEFORE date to today
processed_ads.loc[(~processed_ads["LINK"].isin(new_links_df["LINK"])  & processed_ads["DELISTED_BEFORE"].isnull()), "DELISTED_BEFORE"] = date.today()

# updating the rent of the live ads
processed_ads.loc[processed_ads["DELISTED_BEFORE"].isnull(), "RENT"] = processed_ads.loc[processed_ads["DELISTED_BEFORE"].isnull(), "LINK"].apply(update_rent)

# concating the new ads together with the already processed ads while giving the new ads ID incremented from the tail of processed ads
new_ads_df["ID"] = processed_ads.iloc[-1]["ID"] + new_ads_df["ID"]

new_processed_ads = pd.concat([processed_ads,new_ads_df], axis=0)

# loading the new processed ads DF and new links DF as a table to my database
new_processed_ads.to_sql("processed_ads", con = engine, index=False, if_exists="replace", dtype = {"DELISTED_BEFORE":sqlalchemy.Date(),"LISTED_BEFORE":sqlalchemy.Date()})
new_links_df.to_sql("previous_session", con = engine, if_exists= "replace", index = False)
engine.dispose()