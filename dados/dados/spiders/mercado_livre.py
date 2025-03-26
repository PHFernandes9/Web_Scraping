import scrapy

class MercadoLivreSpider(Scrapy.Spyder):
	name="mercadolivre"
	allowed_domain = ["lista.mercadolivre.com.br"]
	start_urls = ["https://lista.mercadolivre.com.br/video-games#D[A:Video%20games]"]
	
	def pare(self,response):
		pass 
		
		