
# coding: utf-8

# In[9]:

import requests
import datetime


# In[4]:

'''def send_mail_through_python(url_list,to_who):
    import smtplib
    import socket
    subject = 'Protential places you might be interested with '
    to_user = str(to_who)
    body_content = ''
    for i in url_list:
        body_content = body_content + ''.join(i) + '\n'
        type(body_content)
        print(body_content)  # combine all the url's together (string)
    try:
        smtpserver = smtplib.SMTP('smtp.gmail.com', 587)  # bulid smtp connection
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        print('connect to smtp sccuessfully')
        try:
            user = 'yoyoman0411@gmail.com'  # smtp login connection
            password = 'my_password'
            smtpserver.login(user, password)
            print('login sccuessfully')
            try:
                header = 'To: ' + to_user + '\n' + 'From: ' + user + '\n' + 'Subject: ' + subject + '\n'
                msg = header + '\n' + body_content
                smtpserver.sendmail(user, to_user, msg)
                print(msg)
                print('mail sent sccuessfully')
            except NameError:
                print('mail sent failed')
                

        except NameError:
            print('login failed')
    except NameError:
        print('connection failed')
'''


# In[10]:

def send_mail_through_python(url_list,sent_to):
    import smtplib
    import socket
    from email.mime.text import MIMEText
    from email.header import Header

    subject = 'Protential places you might be interested with '
    to_user = sent_to
    body_content = ''
    for i in url_list:
        body_content = body_content + ''.join(i) + '\n'

        print(type(body_content))  # combine all the url's together (string)
    try:
        smtpserver = smtplib.SMTP('smtp.gmail.com', 587)  # bulid smtp connection
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        print('connect to smtp sccuessfully')
        try:
            user = ''  # smtp login connection
            password = ''
            smtpserver.login(user, password)
            print('login sccuessfully')
            try:
                #header = 'To: ' + to_user + '\n' + 'From: ' + user + '\n' + 'Subject: ' + subject + '\n'
                #msg = header + '\n' + body_content
                msg =  body_content
                message = MIMEText(msg, 'html', 'utf-8')

                message['From'] = Header('yoyoman0411@gmail.com', 'utf-8')
                message['To'] =  Header('Hello world', 'utf-8')
                message['Subject'] = Header(subject, 'utf-8')

                smtpserver.sendmail(user, to_user, message.as_string())
                #print(msg)
                print('mail sent sccuessfully')
            except smtplib.SMTPException:
                print('mail sent failed')

        except smtplib.SMTPException:
            print('login failed')
    except smtplib.SMTPException:
        print('connection failed')


# In[4]:

T1 = datetime.datetime.now()
T1 = T1.strftime('%Y-%m-%d %H:%M')
print('the programe start at: '+T1)
cookies = {'user_index_role':'1',
            ' user_browse_recent':'a%3A2%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225183189%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%225126695%22%3B%7D%7D',
            ' ba_cid':'a%3A5%3A%7Bs%3A6%3A%22ba_cid%22%3Bs%3A32%3A%2208b1f847afa44cfb0d1027f3a07add15%22%3Bs%3A7%3A%22page_ex%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-5126695.html%22%3Bs%3A4%3A%22page%22%3Bs%3A48%3A%22https%3A%2F%2Frent.591.com.tw%2Frent-detail-5183189.html%22%3Bs%3A7%3A%22time_ex%22%3Bi%3A1494404773%3Bs%3A4%3A%22time%22%3Bi%3A1494472950%3B%7D',
            ' __auc':'ff8dc3cc15bf1772f195b7fc9b2',
            ' __utma':'82835026.646763773.1494404076.1494482768.1494482768.1',
            ' __utmz':'82835026.1494482768.1.1.utmcsr',
            'localhost:8888|utmccn=(referral)utmcmd':'referral|utmcct=/notebooks/Desktop/Untitled.ipynb',
            ' PHPSESSID':'03500fd74394e4e87cbc54f9a4afbe91',
            ' c10f3143a018a0513ebe1e8d27b5391c':'1',
            ' urlJumpIp':'3',
            ' urlJumpIpByTxt':'=%E6%96%B0%E5%8C%97%E5%B8%82',
            ' _gat':'1',
            ' new_rent_list_kind_test':'0',
            ' 591_new_session':'eyJpdiI6InlKYVE4NzFaeVM5MFRtQlJVU01YOVE9PSIsInZhbHVlIjoiY1wveHhESHRFZEh6UHVlNERHVmhpcmp1Qld1QVo4TGl4TXJ6TVo0OHd2SG1pWnczcjRqa2YwVm5VYXRXWFdIU1JuY3Y4b2hGcG8wUHZ1MGxOem5GXC9YQT09IiwibWFjIjoiODQwM2IxNzBhY2ZlZGY3ZjJlOWZkNzgxM2FhYzkxODY4ODk5YjliZWZjNGE0MmQxMzBkNzcxYzE0M2RkMmI4OSJ9',
            ' _gat_tw591':'1',
            ' _ga':'GA1.3.646763773.1494404076',
            ' _gid':'GA1.3.1996421294.1494579436',
            ' _ga':'GA1.4.646763773.1494404076',
            ' _gid':'GA1.4.65532783.1494579436',
            ' _dc_gtm_UA-97423186-1':'1'
              }
url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&section=38,34&rentprice=3&area=10,20&other=tragoods,cook,balcony_1'
content = requests.get(url,cookies=cookies)
format_content = content.json()
totoal_raw = format_content['records']  #get how many result in totals
firstRow=0
print(totoal_raw)
format_content = dict()
format_content2 = list()

while int(firstRow) <= int(totoal_raw):
    url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=3&section=38,34&rentprice=3&area=10,20&other=tragoods,cook,balcony_1'+'&'+'firstRow='+str(firstRow)+'&'+'totalRows='+str(totoal_raw)
    content = requests.get(url,cookies=cookies)
    print(content.url)
    format_content=content.json()
    format_content2.append(format_content['data']['data'])
    firstRow+=30
    


# In[11]:

format_content2


# In[12]:

counter_47 = 1
for i in format_content2:
    for j in i:
        print(counter_47)
        print(j['address'])
        
        counter_47+=1
        
        
list_for_email = list()
list_for_email_2 = list()
list_for_email_3 = list()
list_for_email_4 = list()
count = 1
import mysql.connector
from sqlalchemy import create_engine
cnx = mysql.connector.connect(user='root', password='rootKen0411',
                              host='127.0.0.1',
                              database='591_rent_project')

cursor = cnx.cursor()
for i in format_content2:
    for j in i:
        print(count)
        print('Item {}:\n'.format(count))
        houseid = j['houseid']
        price = j['price']
        ltime = j['ltime']
        section_name = j['section_name']
        street_name = j['street_name']
        print(j['houseid'])
        print(j['price'])
        print(j['ltime'])
        print(j['section_name'])
        print(j['street_name'])
        print('----------------\n')
        count+=1
        
        try:
            
            add_value_syntax = ("INSERT INTO rent_condition"
                                  "(Ltime, Price, id) "
                                  "VALUES (%s, %s, %s)")

            data_employee = (ltime, price, houseid)

            cursor.execute(add_value_syntax, data_employee)
            cnx.commit()
            list_for_email.append(houseid)
            list_for_email_2.append(ltime)
            list_for_email_3.append(section_name)
            list_for_email_4.append(street_name)
            
        except: 
            print('Insert data failed or already exist in the database!!')

cnx.close()


# In[36]:

count = 0
detail_base_url = 'https://rent.591.com.tw/rent-detail-'
tail = '.html '
final_list=list()
for i in list_for_email:
        print(count)
        id_house = list_for_email[count]
        timepost_house = list_for_email_2[count]
        distinct_name = list_for_email_3[count]
        street_name = list_for_email_4[count]
        msg_url = detail_base_url + str(id_house) + tail +'<br>'+ timepost_house+'<br>'+distinct_name+'<br>'+ street_name+'<br><br>'
        final_list.append(msg_url)
        count += 1
        print(msg_url)
print(final_list)
        
      


# In[21]:

'''detail_base_url = 'https://rent.591.com.tw/rent-detail-'
tail = '.html<br>'

final_list =list()
count = 1
for i in list_for_email:
    convert_string = i
    for j in  list_for_email_2:
        convert_string_2 = j
        for k in list_for_email_3:
            convert_string_3 = k
            for l in list_for_email_4:
                convert_string_4 = l
                
                msg_url = detail_base_url + str(convert_string) + tail +convert_string_2+'<br>'+convert_string_3+'<br>'+convert_string_4+'<br><br>'
                final_list.append(msg_url)
                
    #print(msg_url)
    count+=1
    
print(final_list)'''


# In[38]:

if final_list == []:
    print('There is no need to send the mail at this point')
else:
    #send_mail_through_python(final_list,'ken77889@yahoo.com.tw')
    send_mail_through_python(final_list,'gajdos.alexandra@gmail.com')
    
    


# In[ ]:




# In[ ]:




# In[ ]:



