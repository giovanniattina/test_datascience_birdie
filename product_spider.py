import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/',
        'https://www.magazineluiza.com.br/lavadora-de-roupas-lava-e-seca/eletrodomesticos/s/ed/ela1/'
    ]

    def parse(self, response):
        
        
        for product in response.css('li.product'):
            
            #We only have the information about the vendor inside the product page
            #so too just save the products that magazine luiza sell, the crawler has to acess the product page
            # and extract informations about the product
            product_page = product.css('::attr(href)').extract_first()
            if product_page is not None:
                yield response.follow(product_page, callback=self.parse_product_page)   

            
        # go to the next product page
        next_page = response.css('div.center > a.forward::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product_page(self, response):

        
        info = response.css('div.header-product::attr(data-product)').extract_first()
        if info: #check if got the correct info, because there are some products out of stock and don't have the correct info about them 
            info = json.loads(info)

            if info['seller'] == 'magazineluiza':
                #in the fullTitle data I understood as:  "{title} - {model}", so split the data to ge the two infos
                title, model = info['fullTitle'].split(" - ")
		#the product categories I just found it in the url, then to extract the category, split by / and save the penultimate string
                category = info['urlSubcategories'].split("/")[-2]
                yield {
                    'SKU': info["sku"],
                    'Titulo': title.strip(" "),
                    'Marca': response.css('a.header-product__text-interation > span::text').extract_first(),
                    'Modelo': model.strip(" "),
                    'Preco': info['bestPriceTemplate'],
                    'Categoria': category
                }
