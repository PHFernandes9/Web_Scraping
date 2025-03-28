import scrapy

class MercadoLivreSpider(scrapy.Spyder):
	name="mercadolivre"
	allowed_domain = ["lista.mercadolivre.com.br"]
	start_urls = ["https://lista.mercadolivre.com.br/games/video-games/#menu=categories"]
	
	def pare(self,response):
		pass 
		
		