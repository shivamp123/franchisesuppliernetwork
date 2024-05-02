import re
import pymongo
import requests
from scrapy.http import HtmlResponse

# MongoDB connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb1 = myclient[f"franchi1"]
output_db2 = mydb1["output_db"]

def get_response(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'max-age=0',
        # 'cookie': 'nitroCachedPage=0; _fbp=fb.1.1714096810049.535727242; __hstc=128850451.ab42ec2678f7cfe53d1dcb46b235c500.1714096819411.1714096819411.1714096819411.1; hubspotutk=ab42ec2678f7cfe53d1dcb46b235c500; __hssrc=1; _ga_27MSJXLYFZ=GS1.2.1714096809.1.1.1714098167.0.0.0; _ga=GA1.1.1657998429.1714096809; _ga_4YR50D3B4D=GS1.1.1714129231.2.1.1714129232.0.0.0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    request = requests.get(url, headers=headers)
    response = HtmlResponse(url="xyz", body=request.content)
    return response

# Function to extract data from URLs
def extract_data_from_urls(url_list):
    count = 1
    for url in url_list:
        response1 = get_response(url)
        urls1 = re.findall('<loc>(.*?)</loc>', response1.text)
        for url1 in urls1:
            response2 = get_response(url1)
            datass = response2.xpath('//*[@class="col-lg-12 contentside"]')
            for datas in datass:
                item = {}
                item['file_name'] = url1.split('/')[-2].replace("-", "_")
                item['title'] = datas.xpath('.//*[@class="title"]//text()').extract_first(default="")
                item['details'] = " ".join([iii.strip() for iii in datas.xpath('.//*[@class="post_info"]//text()').extract() if iii.strip()])
                item['des'] = item['title'] + "\n" + item['details'] + "\n" + " ".join([iii.strip() for iii in datas.xpath('.//*[@class="col-sm-12"][2]//text()').extract() if iii.strip()])
                item['url'] = url1
                item['image'] = response2.xpath('//img/@src').extract()
                item['image'].remove("https://franchisesuppliernetwork.com/wp-content/themes/franchise-supplier-network/img/logo-fsn.png")
                item['no'] = count
                item['image_count'] = len(item['image'])
                item['reference_url'] = response2.xpath('//*[@class="col-lg-12 contentside"]//a/@href').extract()
                item['reference_url_count'] = len(item['reference_url'])
                count += 1
                if item['title'] == "":
                    item['des'] = " ".join([iii.strip() for iii in response2.xpath('//*[@class="col-lg-12 contentside"]//text()').extract() if iii.strip()])
                    item['reference_url'] = response2.xpath('//*[@class="col-lg-12 contentside"]//@href').extract()
                    item['reference_url_count'] = len(item['reference_url'])

                    print('Data inserted')
                    output_db2.insert(item)
                else:
                    print('Data inserted')
                    output_db2.insert(item)

# Main code
response = get_response('https://franchisesuppliernetwork.com/sitemap_index.xml')
urls = re.findall('<loc>(.*?)</loc>', response.text)
extract_data_from_urls(urls)
