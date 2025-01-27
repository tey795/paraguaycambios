from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# MyD Cambios에서 환율 정보 추출
def get_mydcambios():
    url = 'https://www.mydcambios.com.py/home'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # <li> 태그에서 venta와 compra 추출
    try:
        li_tags = soup.find_all('li')  # 모든 <li> 태그를 가져옴
        venta = li_tags[15].text.strip().replace('"', '') if len(li_tags) > 15 else '정보 없음'
        compra = li_tags[16].text.strip().replace('"', '') if len(li_tags) > 16 else '정보 없음'
    except Exception as e:
        venta, compra = '정보 없음', '정보 없음'

    return venta, compra

# Maxicambios에서 환율 정보 추출
def get_maxicambios():
    url = 'https://www.maxicambios.com.py/#top-page'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # 모든 <p> 태그에서 클래스가 'ng-tns-c4-0'인 태그 찾기
        p_tags = soup.find_all('p', {'class': 'ng-tns-c4-0'})

        # 첫 번째 <p> 태그는 venta, 두 번째는 compra라고 가정
        venta = p_tags[2].text.strip() if len(p_tags) > 2 else '정보 없음'
        compra = p_tags[4].text.strip() if len(p_tags) > 4 else '정보 없음'
    except Exception as e:
        venta, compra = '정보 없음', '정보 없음'

    return venta, compra

# Cambios Chaco에서 환율 정보 추출
def get_cambioschaco():
    url = 'https://www.cambioschaco.com.py/en/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    venta = soup.find('span', {'class': 'purchase'})
    compra = soup.find('span', {'class': 'sale'})
    return venta.text.strip() if venta else '정보 없음', compra.text.strip() if compra else '정보 없음'

# 웹사이트의 루트 경로
@app.route('/')
def index():
    myd_venta, myd_compra = get_mydcambios()
    maxi_venta, maxi_compra = get_maxicambios()
    chaco_venta, chaco_compra = get_cambioschaco()

    return render_template('index.html',
                           myd_venta=myd_venta, myd_compra=myd_compra,
                           maxi_venta=maxi_venta, maxi_compra=maxi_compra,
                           chaco_venta=chaco_venta, chaco_compra=chaco_compra)

if __name__ == '__main__':
    app.run(debug=True)
