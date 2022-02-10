import scrapy
import re
from ..items import ScreenplayItem


class genreSpider(scrapy.Spider):
    name = 'genres'
    start_urls = ['https://www.imsdb.com/']
    
    
    def parse(self,response): #Start at genre level
        genresName = response.css("a[href*='genre']::text").extract()
        genresLink = response.css("a[href*='genre']::attr(href)").extract()
        #genre = response.xpath("//a[contains(@href,'/genre')]")
        for gName, gLink in zip(genresName, genresLink):
            yield scrapy.Request(response.urljoin(gLink), callback = self.parseFilms, 
                                 meta = {'Genre':gName})
    
    def parseFilms(self, response):
        gName = response.meta['Genre']
        moviesName = response.css("p a::text").extract()
        moviesList = response.css("p a::attr(href)").extract() 
        for mName, mLink in zip(moviesName, moviesList):
            genreSpider.nFilm = mName
            yield scrapy.Request(response.urljoin(mLink), callback = self.navScript,
                                 meta = {'Genre':gName, 'Film': mName})

    def navScript(self, response):
        gName = response.meta['Genre']
        mName = response.meta['Film']
        scriptLink = response.css("a[href*='/scripts/']::attr(href)").get() 
        yield scrapy.Request(response.urljoin(scriptLink), callback = self.parseScript,
                             meta = {'Genre':gName, 'Film': mName})

    
    def parseScript(self, response):
        items = ScreenplayItem()
        gName = response.meta['Genre']
        mName = response.meta['Film']
        script = response.css("pre::text").extract() 
        
        countList = []
        profanityList = [r"[Ff]uck", r"[Dd]amn", r"[Ss]hit\b", r"[Bb]itch", r"(\b|[Dd]umb)[Aa]ss(\b|h)"]
        for p in profanityList:
            countList.append(re.subn(p, '', str(script))[1])
        
        items['Genre'] = gName
        items['Film'] = mName
        items['F'] = countList[0]
        items['D'] = countList[1]
        items['S'] = countList[2]
        items['B'] = countList[3]
        items['A'] = countList[4]
        
        yield items