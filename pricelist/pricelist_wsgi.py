import re
prodName=0
listprice=1
ourprice=2
prodDesc=3
prodPic=4
def get_entry(raw, template):
    cols = raw.split(',')
    if len(cols) != 5:
        return ""
    resp=re.sub(r'<prod_name/>',cols[prodName].strip(),template)
    resp=re.sub(r'<list_price/>',cols[listprice].strip(),resp)
    resp=re.sub(r'<our_price/>',cols[ourprice].strip(),resp)
    resp=re.sub(r'<prod_desc/>',cols[prodDesc].strip(),resp)
    resp=re.sub(r'<prod_pic/>',cols[prodPic].strip(),resp)
    return '\n' + resp

def get_content():
    content = ""
    #return the list of display cells to the caller.
    with open('/var/www/pricelist/data/cell.txt','r') as f:
        cell_template=f.read()
    with open('/var/www/pricelist/data/pricelist.csv','r') as f:
        for line in f:
            entry = line.strip()
            if entry[0] == '#':
                continue
            content = content +  get_entry(entry,cell_template)

    return content

def application(environ, start_response):
    sPath = environ['PATH_INFO']
    sFull = environ['SCRIPT_NAME']
    # uncomment the following line to print hello to httpd/error_log
    # print("Hello") 
    # It does detect an image request...
    if '.png' in sPath or '.ico' in sPath:
        print(sPath[1:]) 
        data = open(f'/var/www/pricelist/data/{sPath[1:]}', 'rb').read()
        start_response('200 OK', [('Content-Type', 'image/png'),
                                 ('content-length', str(len(data)))])
        return [data]
    status = '200 OK'
    with open('/var/www/pricelist/data/template.txt','r') as f:
        html_text = f.read()
    cell_txt = get_content()
    html_text=re.sub(r'<context/>',cell_txt,html_text)
    html=html_text.encode("utf-8")
    response_header = [('Content-type','text/html')]
    start_response(status,response_header)
    return [html]

