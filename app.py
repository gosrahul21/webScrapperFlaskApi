from flask import request,Flask,render_template,request,jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/',methods=['GET']) #route to display the home page
@cross_origin()
def homePage():
    return render_template('index.html')


@app.route('/review',methods=['POST'])
@cross_origin()
def review():
    searchString = request.json['search'].replace(" ","")
    imdb_url = "https://www.imdb.com/find?q="+searchString
    
    uclient = uReq(imdb_url)
    fetch_page = uclient.read()
    uclient.close()
    imdb_html = bs(fetch_page,'html.parser')
    search_url = "https://www.imdb.com"+imdb_html.td.a['href']   
    movieName = imdb_html.find_all('td')[1].a.text
    print(movieName)
    uClient = uReq(search_url)
    req_page = uClient.read()
    req_page = bs(req_page,"html.parser")
    frating = req_page.find_all('span',{'class':"AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"})[0].text
    review_links = req_page.find_all('div',{"class":"UserReviewsHeader__Header-k61aee-0 egCnbs"})
    #img links
    try:
        image_links = req_page.find_all('a',{"class":"ipc-button ipc-button--single-padding ipc-button--center-align-content ipc-button--default-height ipc-button--core-baseAlt ipc-button--theme-baseAlt ipc-button--on-onBase ipc-secondary-button Link__MediaLinkButton-yyqs5y-3 bzgyge"})
        image_links = image_links[0]['href']
        img_link_actsite ="https://imdb.com"+image_links
        uClient = uReq(img_link_actsite)
        readData = uClient.read()
        img_html = bs(readData,"html.parser")
        img = img_html.find_all('img')[0]['src']
        #fetch image links
        uClient.close()
    except:
        img="#"


    
    reviews = review_links[0].a['href']
    # print(reviews)
    uclient = uReq("https://www.imdb.com"+reviews)
    reviews_list = uclient.read()
    reviews_html = bs(reviews_list,'html.parser')
    lister_list = reviews_html.find_all('div',{"class":"lister-item mode-detail imdb-user-review collapsable"})
  
    lst = []        
    for reviews in lister_list:
        review = reviews.div.div.find_all('div')

        try:
            rating = review[0].span.span.text
        except:
            rating = ''
        try:
            user = review[1].span.a.text
        except:
            user = ''
        
        try:
            commentHead = reviews.div.div.a.text
        except:
            commentHead=''

        try:
            # commentBody1 = review[2].text
            commentBody = review[3].text
            # if(len(commentBody1)>len(commentBody2)):
            #     commentBody = commentBody1
            # else:
            #     commentBody = commentBody2 
        except:
            commentBody=''
   
        response = {"rating":rating,"user":user,"commentHead":commentHead,"commentBody":commentBody}
        lst.append(response)
   
    return jsonify({"list":lst,"movieName":movieName,"frating":frating,"img":img})
    # return render_template("display.html",lst = lst)




# app.run()

if(__name__=='__main__'):
    app.run(debug=True)
