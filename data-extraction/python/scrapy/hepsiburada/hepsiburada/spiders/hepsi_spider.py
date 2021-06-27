import scrapy
from hepsiburada.items import HepsiburadaItem
from urllib.parse import urlparse, parse_qs

class HepsiSpider(scrapy.Spider):
    name = "hepsiburada"
    
    def start_requests(self):
        urls = []

        hepsi_list = [
            'https://www.hepsiburada.com/cep-telefonlari-c-371965',
            'https://www.hepsiburada.com/samsung-apple-xiaomi-huawei-opporealme-honor-garmin-amazfit-fossil-lenovo-oppo-asus-diesel-sony-casio-emporioarmani/akilli-saatler-c-60003676',
            'https://www.hepsiburada.com/tablet-c-3008012',
            'https://www.hepsiburada.com/oyuncu-masaustu-bilgisayarlari-c-95582',
            'https://www.hepsiburada.com/oyuncu-laptoplari-c-95583',
            'https://www.hepsiburada.com/ekran-kartlari-c-204',
            'https://www.hepsiburada.com/islemciler-c-46',
            'https://www.hepsiburada.com/playstation-5-konsol-c-80757006',
            'https://www.hepsiburada.com/robot-supurge-c-80160033',
            'https://www.hepsiburada.com/apple-samsung-huawei-beats-bose-sennheiser-audiotechnica-klipsch-razer-corsair-harman-yamaha/bluetooth-kulakliklar-c-16218?filtreler=kullanimtipi:Kulaki%E2%82%ACC3%E2%82%ACA7i',
            'https://www.hepsiburada.com/sennheiser-apple-yamaha-bose-razer-jbl-akg-beats-jabra-audiotechnica-sony-meizu-edifier-philips/bluetooth-kulakliklar-c-16218?filtreler=muzik:Var;kullanimtipi:Kulak%E2%82%ACC3%E2%82%ACBCst%E2%82%ACC3%E2%82%ACBC&siralama=artanfiyat',
            'https://www.hepsiburada.com/soundbar-c-60008218',
            'https://www.hepsiburada.com/ev-sinema-sistemleri-c-60007251',
            'https://www.hepsiburada.com/ev-tipi-subwoofer-c-60007247',
            'https://www.hepsiburada.com/monitorler-c-57',
            'https://www.hepsiburada.com/jbl-harmankardon3-sony-anker-lg-samsung-tronsmart-bose-jabra-yamaha/bluetooth-hoparlorler-c-60004557',
            'https://www.hepsiburada.com/xiaomi-google-apple-nvidia-lg-anker/media-player-c-80271010',
            'https://www.hepsiburada.com/lazer-yazicilar-c-6',
            'https://www.hepsiburada.com/murekkep-puskurtmeli-yazicilar-c-4',
            'https://www.hepsiburada.com/ses-goruntu-sistemleri-c-17201',
            'https://www.hepsiburada.com/playstation-4-konsollari-c-60003892',
            'https://www.hepsiburada.com/xbox-series-x-konsol-c-80766001'
        ]
        total_page = 50
        for hepsi in hepsi_list:
            for i in range(1, total_page):
                urls.append(
                    f"{hepsi}?sayfa={i}"
                )
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for product in response.xpath('//ul[@class="productListContainer-wrapper productListContainer-grid-vertical-1"]/li/div'):
            yield HepsiburadaItem(
                name=product.xpath('.//h3/text()').extract_first(),
                price=product.xpath('.//div[@data-test-id="price-current-price"]/text()').extract_first(),
                url=product.xpath('./a/@href').extract_first(),
                id=product.xpath('./a/@href').extract_first().split('-')[-1]
            )

