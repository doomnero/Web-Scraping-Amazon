from bs4 import BeautifulSoup
import re
import random
import datetime
from urllib.request import urlopen, Request
import pandas as pd

user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.58',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0'
]
while True:
    try:
        way = input('Iniciando pesquisa de livros na amazon!\nFavor inserir caminho para a pasta onde se encontra o arquivo base: ')
        book = pd.read_excel(f'{way}\AMAZON_BASE_PESQUISA_AUTOMATICA.xlsx')
        print('Arquivo lido, iniciando pesquisa, favor aguardar mensagem de término para fechar o programa.')
        break
    except:
        print('Erro ao encontrar arquivo.')
list_df = book.values.tolist()
str_book = str(list_df)
eliminating_characters = re.sub("\,|\'|\[|\]","",str_book)
def stringToList(string):
    listRes = list(string.split(" "))
    return listRes
list_book = stringToList(eliminating_characters)

isbn_list = list_book

excel_dict = {}

for isbn in isbn_list:
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    search_page = f'https://www.amazon.com.br/s?k={isbn}&i=stripbooks&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=HTEQ0539KZZL&sprefix={isbn}%2Cstripbooks%2C807&ref=nb_sb_noss'
    fake_user_agent_search_page = urlopen(Request(search_page, headers=headers))
    search_page_soup = BeautifulSoup(fake_user_agent_search_page, 'html5lib')
    seeing_if_page_exists = search_page_soup.find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    if seeing_if_page_exists == None:
        price = 'Não tem na Amazon'
        excel_dict[f'{isbn}'] = price
    else:
        page = search_page_soup.find_all(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal', href=True)
        for a in page:
            href_link_str_with_ads = str(a['href'])
            href_link_list_with_ads = stringToList(href_link_str_with_ads)
            href_link_with_ads = href_link_list_with_ads[0]
            ad = '/gp/slredirect/picassoRedirect.html/'
            if ad in href_link_with_ads:
                pass
            else:
                href_link = []
                href_link.append(href_link_with_ads)
        amazon_link = 'https://www.amazon.com.br' + str(href_link[0])
        fake_user_agent_book_page = urlopen(Request(amazon_link, headers=headers))
        book_page_soup = BeautifulSoup(fake_user_agent_book_page, 'html5lib')
        seeing_if_its_new = book_page_soup.find(class_='olp-new olp-link')
        if seeing_if_its_new == None:
            seeing_if_used_is_none = book_page_soup.find(class_='olp-used olp-link')
            if seeing_if_used_is_none == None:
                price = 'Não tem preço na Amazon'
                excel_dict[f'{isbn}'] = price
            else:
                getting_price = list(book_page_soup.find(class_='olp-used olp-link').text)
                eliminating_empty_spaces = getting_price[:-7]
                getting_numerals = eliminating_empty_spaces[-7:]
                dirty_price = ''.join(getting_numerals)
                final_price = re.sub('[^0-9]', '', dirty_price)
                final_price_without_spaces = final_price.lstrip()
                hash = final_price_without_spaces[:-2] + ',' + final_price_without_spaces[-2:]
                price = f'Somente usado: {hash.lstrip()}'
                excel_dict[f'{isbn}'] = price
        else:
            getting_price = list(book_page_soup.find(class_='olp-new olp-link').text)
            eliminating_empty_spaces = getting_price[:-7]
            getting_numerals = eliminating_empty_spaces[-7:]
            dirty_price = ''.join(getting_numerals)
            final_price = re.sub('[^0-9]', '', dirty_price)
            final_price_without_spaces = final_price.lstrip()
            hash = final_price_without_spaces[:-2] + ',' + final_price_without_spaces[-2:]
            price = hash
            excel_dict[f'{isbn}'] = price

df = pd.DataFrame(data=excel_dict, index=[0])
df = (df.T)
while True:
    try:
        excel_local = input('Favor inserir caminho para a pasta onde o arquivo será gerado: ')
        date_now = datetime.datetime.now()
        str_date_now = str(date_now)
        clean_date_now = re.sub("\:","-",str_date_now)
        super_clean_str_date_now = re.sub("\ ","_",clean_date_now)
        final_date_now = super_clean_str_date_now[:-10]
        df.to_excel(f'{excel_local}\PRECOS_AMAZON_{final_date_now}.xlsx')
        break
    except:
        print('Erro ao encontrar pasta.')

input('====================================================================\nTérmino da pesquisa! Aperte qualquer tecla para fechar o programa: ')
