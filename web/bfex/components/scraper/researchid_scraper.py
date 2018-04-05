from bfex.components.scraper.scraper import *
from bfex.components.scraper.scraper_type import *


class ResearchIdScraper(Scraper):
    """ This is what will scrape the researchid links """

    def get_scrapps(self):
        """ Get the html content from the website and put it into a scrapp
            It gets title from the first page, keywords and descriptions
            :return: return all the scrapps produced
        """
        scrapps = []
        self.validate_url()
        soup = self.get_content()
        freebies = soup.find_all("tr")
        found = False
        found_d = False
        scrapp = Scrapp()

        # Get the keywords and description
        for section in freebies:
            if (found is True and found_d is True):
                break
            contents = section.find_all("td")
            i = 0
            for content in contents:
                if ("Keywords:" == str(content.string) and not found):
                    # Get just the keywords and strip out other characters
                    keywords = contents[i+1].contents[0].strip()
                    keywords = keywords.replace("\n", "").replace(" ", "")
                    keywords = keywords.replace("\r", "")
                    keywords = keywords.replace("\xa0", "").split(";")
                    scrapp.add_meta("keywords", keywords)
                    found = True
                if ("Description:" in str(content.string) and not found_d):
                    # Get the description and strip out other characters
                    keywords = contents[i+1].string.replace("\xa0", "")
                    scrapp.add_meta("description", keywords)
                    found_d = True
                i += 1
        
        # May append a blank scrape, but first in the list is for freebies
        scrapp.set_source(self.type)
        scrapps.append(scrapp)    
            
        imgs = soup.find_all("img")
        links = []
        for img in imgs:
            if "window.open" in img.attrs.get('onclick', ''):
                link = img.attrs.get('onclick', '')
                link = link.split("(")
                link = link[1]
                link = link[1:-2]
                try:
                    response = requests.get(link)
                    soup = BeautifulSoup(response.text, "html.parser")
                    # texts will include javascript and html and css. I am not sure why this happens
                    texts = soup.find_all(text=True)
                    for text in texts:
                        words = text.split()
                        # we have to remove the small text,
                        # then the html, css and javascript
                        if (len(words) > 100) and (">" not in text) and ("background-" not in text) and ("||" not in text):
                            scrapp_absract = Scrapp()
                            scrapp_absract.add_meta("text", text)
                            scrapp_absract.set_source(ScraperType.RESEARCHIDABSTRACT)
                            scrapps.append(scrapp_absract)
                            print("\n\n", scrapp_absract.meta_data["text"], "\n\n")
                except requests.exceptions.ConnectionError:
                    print("\nThere was a connection error\n")

        titles = soup.find_all("input")

        # Get the titles
        for title in titles:
            try:
                if ("itemTitle" in title.get("name")):
                    scrapp = Scrapp()
                    scrapp.set_title(title.get("value"))
                    scrapp.set_source(self.type)
                    scrapps.append(scrapp)
            except:
                continue
        return scrapps
