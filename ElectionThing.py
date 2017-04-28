from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

PAT = 'EAAarLkMVMy4BALcfghCBksMQuo5lqLMIsogY1OJEHxVDJZAdIR0KkKWqfdCEbbRIv7IeFrsTTEAFfNRo3y0vgFmZA7wCkcYsZAQSEwlBL6V5VZAexpR4LO4IB1hZAhaoDYejvT5hLjCeZCaiye8qCa5vNrOOGuSyAuWE5ZCZB5VMfwZDZD'
VerifyToken = '0454'

IntroductoryMessage = ''' The 2017 Kenyan National Elections are taking place in August.
I am a tool for you to acquire more information on voting and the vying candidates.
I have a top-level menu which you can access at any time by pressing the menu icon (\u2630)  at the bottom to choose the option that you want.
Go ahead, try it.
\U0001F642
'''
VoterRegistration = '''Thank you for using Uchaguzi!
However due to logistical circumstances, the option of finding out your registration status is not available right now.
Please check again in a little while as we go about incorporating it.
'''
VoterRequirements = '''
The national elections are on Tuesday, August 8th.
You will need to have registered as a voter and carry your national identification, or passport to vote.
Please come out in support for our best future leaders.
'''
CandidateMoreInfo = '''
Which candidate do you want to know more about?

(Send me his or her name.)

'''

ApologyMessage = '''
Sorry, I didn't get that.
Would you mind repeating it?
'''

BaseUrl = 'http://myaspirantmyleader.co.ke/'
candidates = []
Counties = ['kiambu', 'kisumu', 'mombasa', 'nairobi', 'nakuru']
OtherCounties = ''' Thank you for using Uchaguzi.
However, this is our first beta and us such we can only provide information for Kiambu, Kisumu, Mombasa, Nairobi, or Nakuru.
Please use any of those five counties for now, as we go about adding information support for all other counties!
\U0001F642
'''

@app.route('/', methods=['GET'])
def verification():
  if request.args.get('hub.verify_token', '') == VerifyToken:
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def GetMessages():
  messages = request.get_json()
  if messages['object'] == 'page':
    for message in messages['entry']:
        for msg in message['messaging']:
            SenderID = msg['sender']['id']
            if msg.get('message'):
                MessageText = msg['message']['text']
                if 'president' in MessageText.lower():
                    names = Candidates()
                    TEXT = 'The presidential candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                elif 'governor' in MessageText.lower():
                    CountyOptions(SenderID)
                elif  MessageText.lower() == 'moses':
                    y = 'Moses Masika Wetangula'
                    a = CandidateInfo(y)
                    SendMessage(SenderID, a)
                elif MessageText.lower() == 'uhuru':
                    y = 'Uhuru Muigai Kenyatta'
                elif MessageText.lower() == 'kiambu':
                    names = Search(MessageText, 'governor')
                    ST = 'The candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, ST)
                elif MessageText.lower() == 'n':
                    pass
                elif MessageText.lower() == 'kisumu':
                    pass
                elif MessageText.lower() == 'nakuru':
                    pass
                elif MessageText.lower() == 'mombasa':
                    pass
                else:
                    SendMessage(SenderID, ApologyMessage)


            if msg.get('postback'):
                PostbackText = msg['postback']['payload']
                if PostbackText == 'Get Started':
                    SendMessage(SenderID, IntroductoryMessage)
                elif PostbackText == 'presidential':
                    names = Candidates()
                    TEXT = 'The presidential candidates are: \n' + str(names[0:])
                    SendMessage(SenderID, TEXT)
                while PostbackText == 'gubernatorial':
                    print('governors')
                    CountyOptions(SenderID)
                    if msg.get('message'):
                        print('Gotten Text')
                        m = msg['message']['quick_reply']['payload']
                        if m.lower() == 'nairobi':
                            SendMessage(SenderID, 'KKK')
                   
                '''elif PostbackText == 'senate' :
                    TEXT2 = 'From what county?'
                    SendMessage(SenderID, TEXT2)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'womrep' :
                    TEXT2 = 'From what county?'
                    SendMessage(SenderID, TEXT2)
                    TEXT2 = 'The candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'parliamentary' :
                    TEXT2 = 'What county?'
                    SendMessage(SenderID, TEXT2)
                    TEXT2 = 'The' + PostbackText + 'candidates are'
                    SendMessage(SenderID, TEXT2)
                elif PostbackText == 'VoterReg':
                    SendMessage(SenderID, VoterRegistration)
                elif PostbackText == 'VoterReq':
                    SendMessage(SenderID, VoterRequirements)
                else:
                    SendMessage(SenderID, ApologyMessage)'''




  return 'ok', 200

   

def SendMessage(RecipientID, Text):
    print(('Sending message to {0}').format(RecipientID))

    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient': {
        'id': RecipientID
    },
    'message' : {
        'text': Text
    }
    })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages/?access_token=' + PAT,  headers=headers, data=data)
    if r.status_code != 200:
        print(r.text)

def CountyOptions(RecipientID):
    print(('Sending county options to {0}').format(RecipientID))
    CountyText = 'From what county? Choose one below.'
    headers = {
    'Content-Type' : 'application/json'
    }
    data = json.dumps({
        'recipient' : {
        'id' : RecipientID
        },
        'message': {
            'text' : CountyText,
            'quick_replies' : [
            {
                'content_type' : 'text',
                'title' : 'Kiambu County',
                'payload' : 'kiambu'
            },
            {
                'content_type' : 'text',
                'title': 'Kisumu County',
                'payload': 'kisumu'
            },
            {
                'content_type' : 'text',
                'title': 'Mombasa County',
                'payload': 'mombasa'
            },
            {
                'content_type' : 'text',
                'title': 'Nairobi County',
                'payload': 'nairobi'
            },
            {
                'content_type' : 'text',
                'title': 'Nakuru County',
                'payload': 'nakuru'
            }
            ]
        }
        })
    r = requests.post('https://graph.facebook.com/v2.9/me/messages?access_token=' + PAT, headers = headers, data = data)
    '''messages = request.get_json()
    if messages['object'] == 'page':
        for message in messages['entry']:
            for msg in message['messaging']:
                SenderID = msg['sender']['id']
                if msg.get('message'):
                    m = msg['message']['quick_replies']['payload']
                    if m.lower() == 'nairobi':
                        SendMessage(SenderID, 'KKK')'''
    if r != 200:
        print(r.status_code)



def Name(name):
    name = name.split()
    name = '-'.join(name)
    return name.lower()

def Candidates():
    Url = BaseUrl + 'members/presidential-candidates/'
    RQT = requests.get(Url)
    DATA = RQT.text
    SD = BeautifulSoup(DATA, 'html.parser')
    for match in SD.find_all('div', class_ = 'col-md-3 col-sm-6 col-xs-12'):
        NT = match.find('h3')
        name = NT and ''.join(NT.stripped_strings)
        PT = match.find('span')
        party = PT and ''.join(PT.stripped_strings)
        fmt = '{0} - {1}.'.format(name, party)
        candidates.append(fmt)
    candidate = '\n'.join([str(cand) for cand in candidates])
    return candidate
        

def CandidateInfo(name):
    print('Getting info')
    z = Name(name)
    Url = BaseUrl + 'member/' + z + '/'
    RQT2 = requests.get(Url)
    DATA2 = RQT2.text
    SD2 = BeautifulSoup(DATA2, 'html.parser')
    for match in SD2.find_all('div', class_='member-content'):
        info_tag = match.find('p')
        info = info_tag and ' '.join(info_tag.stripped_strings)
        return info

def Search(CountyName, Level):
    CountyName = CountyName.title() + '+County'
    parameters = {
    "upme_search[county]" : CountyName,
    "upme-search"  :  "Search+&+Filter"
    }
    search = BaseUrl  + 'candidates/' + Level + '-candidates/'
    ToSearch = requests.post(search, params=parameters)
    y = ToSearch.status_code
    if y == 200:
        TS = ToSearch.text
        TS = BeautifulSoup(TS, 'html.parser')
        for match in TS.find_all('div', class_= 'upme-team-design-three upme-team-design'):
            for tags in match.find('div', class_ = 'upme-author-name'):
                name_tag = tags.find('a')
                name = name_tag.string
                return name


if __name__ == '__main__':
  app.run(debug = True)


#counties - Nairobi, Kiambu, Nakury, Mombasa, Kisumu

g_nairobi = ['Evans Kidero - CORD-ODM', 'Mike Mbuvi Sonko - Jubilee', 'Peter Kenneth - JUBILEE', 'Miguna Miguna - ODM ']

g_evans_info = '''Evans Odhiambo Kidero is a Kenyan politician and current Governor of Nairobi County. 
He served as CEO of Mumias Sugar Company for 8 years, resigning in 2012 to join elective politics. 
Kidero was elected as the first governor of Nairobi County in the Nairobi gubernatorial elections of 2013 on an ODM ticket. 
Dr. Kidero is married to Susan Mboya, daughter of the late Kenyan politician, Tom Mboya, and together they have 3 children.'''

g_mike_info = '''Mbuvi Gidion Kioko Mike Sonko  commonly known as Mike Sonko is a Kenyan politician who currently serves as Senator of Nairobi. 
Sonko is the immediate former Member of Parliament for Makadara Constituency, Kenya, a position he was elected to on September 20, 2010 in a by-election. 
Born in Mombasa ,Mbuvi became the First Senator of Nairobi.True to his word, his Makadara constituency has recorded a significant surge in employment brought about by establishment and growth of small businesses. 
His style of leadership has been described as different because unlike other leaders, Mike Sonko walks around dressed in jeans and a t-shirt which has earned him titles like, mtu wa watu (A man of the people).
'''

g_peter_info = '''Peter Kenneth (born 27 November 1965) is a Kenyan politician. He hails from Kirwara Sub-location of Gatanga Constituency in Murang'a County, Kenya.Peter Kenneth was first elected a Member of Parliament for Gatanga Constituency in December 2002 on a National rainbow coalition ticket.] He held this seat up to 2013 general elections where he vied for presidency. His constituency was voted the best managed in Kenya, during his tenure.2008 to date: Assistant Minister, Ministry of State for Planning, National Development and Vision 2030.Dec 2005 – 2007: Assistant Minister, Ministry of Finance.Nov 2003 – 2005: Assistant Minister, Ministry of Cooperative Development and Marketing.
4.Miguna Miguna
Miguna Miguna (born in Kisumu District) is a Kenyan author and columnist. He is also a barrister and solicitor in Canada, and an advocate of the High Court of Kenya. Miguna served as a senior adviser to former Prime Minister Raila Odinga from 2009 to 2011.
'''
g_mombasa = ['Ali Joho - ODM(NASA)', 'Suleiman Shahbal - Jubilee Alliance', 'Hezron Awiti - WIPER(NASA)']

g_ali_info = '''Hassan Joho is a Kenyan politician affiliated to the Orange Democratic Movement and was elected to represent the Kisauni Constituency in the National Assembly of Kenya during the Kenyan parliamentary election, 2007. On 4 March 2013, during the general election, Joho was elected as the first governor of Mombasa County. Joho joined active politics in the year 2004, and became the Kisauni party chairman for the Liberal Democratic Party between 2006-2007. It was not until 2007 General Election, when he was overwhelmingly elected as the Kisauni parliamentary member through ODM in 2007. He was elected as Member of Parliament for Kisauni constituency and the Assistant Minister for Transport. On 4 March 2013 he was elected as Governor of Mombasa.
According to The Economist, "He is close to Raila Odinga, Kenya’s main opposition leader, and is said to be financing Mr Odinga’s Orange Democratic Movement party."
'''
g_suleiman_info = '''Suleiman Shahbal was Managing Partner of GulfCap Investments Ltd until 2012 .He is Chief Executive and Director of Gulf African Bank and Bank Clerk of Citibank .Suleiman Shahbal is Secondary School Student of Nairobi School, Kenya He  is Founder & Executive Director of Trifoil Petroleu Ltd He is also Deputy General Manager of Bank of Muscat, UAE He has been Member of Wiper democratic Movement Kenya representing Mombasa since 2013-01 Suleiman Shahbal was Aspirant Governor of REPUBLIC OF KENYA representing Mombasa until 2013-03-04 Suleiman Shahbal has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-13 TICAL PARTY-JUBILEE'''
g_hezron_info = '''Hezron Awiti was elected for the first time in Parliament in 2013 as the MP for Nyali Constituency in Mombasa County. He was elected on a Wiper Democratic Movement Party ticket in the CORD Coalition. He was blocked from running on ODM ticket after won the ODM ticket but was not denied the ticket because some people thought he stood no chance against a coastal candidate on other tickets. He won the seat with a convincing majority despite the fact that majority of the voters there were not Luo.Hezron Awiti has declared that he will challenge Mombasa Governor Hassan Joho for the gubernatorial seat in 2017 on a Wiper ticket.
'''
g_kisumu = ['Jack Ragumba - ODM(NASA)', "Peter Anyang' Nyong'o  - ODM(NASA)", 'Christopher Odieki - ODM(NASA)']




g_jack_info ='''Jack Nyanungo Ranguma, also known as JR, is a Kenyan politician and was the first Governor of Kisumu County, Kenya. He was elected on 6 March 2013. Jack Ranguma has a Master of Science (International Accounting and Management Information Systems) from the University of Illinois at Urbana-Champaign. Prior to entering politics Jack Ranguma had worked as an accountant for close to 30 years. In 1979, Jack Ranguma was appointed Audit Manager in charge of a large quasi-government n audit portfolio by BDO International. he was promoted to Partner in charge of audit services in 1989, and served as Partner and Head of Financial and Management Consultancy Services between 1991-2001. in 2002 he was appointed Commissioner of Income Tax, and later Commissioner of Domestic Taxes, Kenya Revenue Authority. In 2008 he became Senior Policy Advisor, Tax Justice Network Africa, a pan-African organization.
'''
g_anyang_info = '''Peter Anyang' Nyong'o (born 10 October 1945) is a Kenyan politician. He is the Secretary General of the Orange Democratic Movement and was the acting party leader from March 11 until late May when Raila Odinga was in the United States and was elected to the National Assembly of Kenya in the December 2007 parliamentary election, representing the Kisumu Rural Constituency. He was the Minister for Medical Services and previously the Minister for Planning & National Development. He is currently serving as the Senator for Kisumu County.
'''

g_chris_info = '''Born in the Kisumu slums in 1983 went to a mixed public school to enjoy the Kenyan education system in a journey that culminated in his graduation in 2009 with a Bachelor of Architecture at the Jomo Kenyatta University of Agriculture and Technology. During his campus life he engaged student leadership and youth political movements and also in work study programs to support the siblings and joined business with like minded friends who were fellow students to start business and became pioneer agents for Safaricom mpesa business.
'''


g_nakuru = ['Kinuthia Mbugua - Jubilee Alliance', 'Lee Kinyanjui - Jubilee Alliance', 'James Kiarie Mungai - Jubilee Alliance']

g_kinuthia_info = '''Kinuthia Mbugua , is the first and current governor of Nakuru County in Kenya. He has had an illustrious career in the Civil Service in 1978 as a District Officer and served extensively throughout the countryrising to become a District Commisssioner in Nakuru.
'''
g_lee_info = '''Lee Maiyani Kinyanjui is a Kenyan politician.He belongs to the Party of National Unity and was elected to represent the Nakuru Town Constituency in the National Assembly of Kenya since the Kenyan parliamentary election, 2007. He is a 35-year-old graduate of Kenyatta university where he graduated in literature and later pursued a master's degree in business administration at the Nairobi university. He was  the assistant minister for roads.
'''

g_james_info = '''James Kiarie Mungai was born in 1st January 1960 he is a Kenyan politician and the senator for Nakuru county. He is a member of The National Alliance and a coalition member of Jubilee Alliance. 997 – 2013 : Managing Director, May Feeds(K) Limited.1979 -1987 : Sales Representative, Stellascope Trading Company LimitedSenior Cashier, Unga Limited
AREAS OF INTEREST: Industrial, Finance And Commerce Agriculture And Tourism.'''

g_kiambu = ['William Kabogo - Jubilee Alliance', 'Ferdinand Waititu - Jubilee Alliance', 'Bedan Mbugua - Safina Party of Kenya']


g_william_info = '''William Kabogo Gitau was born on 4th April 1961. He is a Kenyan politician and currently the governor for Kiambu county.He is a member of The National Alliance. He was highly rated among the Members of 10th Parliament for being one of the most inquisitive and one who sought ministerial statements at the behest of his constituents. In 2002, William Kabogo joined politics as a young man and won the Juja parliamentary seat. Since, he has been known to have initiated numerous development projects, including provision of tapped water, installation of electricity, and road construction works as well as, proper management of the bursary fund, construction of health centers and schools. In 2007, he defended his position for the Juja Parliamentary seat, which he controversially lost to George Thuo in a disputed election
'''

g_ferdinard_info = '''Ferdinard Waititu (born January 1, 1962 in Kibera, Nairobi) was the Kabete Member of Parliament since 2015 and the immediate former Member of Parliament for Embakasi Constituency and assistant minister for Water Services and Irrigation in the government of Kenya. He is a former deputy mayor and Councillor of Nairobi. He is described as a "fiery politician" and has been arrested on several occasions, including for "hate speech" directed against ethnic Maasai and for protesting the demolition of shanty houses in his district. In September 2012 he was suspended from his government post over charges of hate speech and inciting violence.
'''
g_bedan_info = '''Bedan Mbugua is Director of Royal Media Services. He was Aspirant Governor of REPUBLIC OF KENYA representing Kiambu between 2012 and 2013-03-04 Bedan Mbugua has been Member of Safina Party Of Kenya since 2013-02-08
'''

s_nairobi = ['Johnson Sakaja - Jubilee', 'William Wahome - Jubilee', 'Richard Kavemba - Wiper Democratic Movement of Kenya']


s_johnson_info = '''Johnson Sakaja , the National Chairman of TNA is currently the Principal Partner at Arthur Johnson Consultants which offers financial and strategic advisory services to Governmental and Private business entities in Kenya. Sakaja Johnson studied Actuarial Science and is currently pursuing Political Economics where he found his interests lie.He began his foray into national politics through student politics at the University of Nairobi (NASA – as vice chair of the Actuarial Students Association and later in SONU).He has been involved in National Politics since the 2005 referendum and played a key role in the 2007 re-election of H.E. Mwai Kibaki. Sakaja was also instrumental in the constitution making process being a key consultant to the COE and Parliamentary Select Committee on the Constitution on the issue of Representation and helped formulate the formula for delimitation of electoral boundaries in Kenya.
'''

s_richard_info = '''Richard Mutinda Kavemba has been Member of Wiper democratic Movement of Kenya since 2013-02-15 
Richard Mutinda Kavemba was Aspirant Governor of REPUBLIC OF KENYA representing Nairobi between 2013-02-15 and 2013-03-04 
Richard Mutinda Kavemba has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-16'''

s_william_info = '''Businessman William Wahome has declared his interest to run for Nairobi senator. The businessman-cum-politician becomes one of the aspirants to announce a bid for the JP ticket..Wahome announced his bid at the home of Roysambu parliamentary aspirant Michael Karanja, where the two hosted their grassroots mobilisers.
'''

s_mombasa = ['Yasser Bajaber - FORD Kenya', 'Mohammad Faki - United Democratic Forum (UDF) Party', 'Tendai Mtwana - Independent Party']

s_yasser_info = '''Yasser Ali Sheikh has been Member of Ford Kenya since 2013-02-08 
Yasser Ali Sheikh was Aspirant MP of REPUBLIC OF KENYA representing Nyali between 2013-02-08 and 2013-03-04 
Yasser Ali Sheikh has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-13
'''


s_mohammad_info = '''
Mohamed Faki Mwinyihaji has been Member of United Democratic Forum Party (UDF) since 2013-02-08. 
Mohamed Faki Mwinyihaji has been Coalition Member of Amani (Peace) Coalition since 2013-02-13. 
Mohamed Faki Mwinyihaji was Aspirant MP of REPUBLIC OF KENYA representing Jomvu between 2013-02-08 and 2013-03-04.
'''
s_tendai_info = '''
Tendai Lewa Mtana has been Member of The Independent Party since 2013-02-08 
Tendai Lewa Mtana was Aspirant Governor of REPUBLIC OF KENYA representing Mombasa between 2013-02-08 and 2013-03-04 
Tendai Lewa Mtana has been Coalition Member of Coalition for Reforms & Democracy since 2013-02-13
'''

s_nakuru = ['Susan Kihika - Jubilee',  'Jack Waihenya - Jubilee']
s_susan_info = '''
Susan Kihika, born in 1974, is the daughter of the late Nakuru veteran Politician Dickson Kihika Kimani who earned repute in the 1970s and 1980s. He is the only Kenyan to ever get elected as MP of three different constituencies(Nakuru North, Laikipia West and Molo). By Profession, Susan Kihika holds a Political Science and Government Degree from the University of North Texas in Denton, Texas, USA.She also did a Jurist Doctorate Law Degree from the Southern Methodist University in Dallas, Texas,USA. She was l elected the Vice Chairlady of the County Assemblies Forum, which is composed of all 47 County Assemblies in Kenya with a membership of over 2200 MCAs and 47 County Assembly speakers.Susan Kihika is well known for being involved in community projects and charity work including being involved in women groups projects across the county, advocating for rights and welfare of children particularly those living with disabilities and advancement of girl child education.
'''
s_jack_info = '''
A Nakuru Businessman and Engineer eyeing the Senatorial seat.
'''

s_kisumu = ['Otieno Odongo - ODM(NASA)', 'Milicent Abudho - ODM(NASA)']
s_otieno_info = '''
He was admitted to Maseno National School in 1964 through to 1967 where after O levels he proceeded to Friends School Kamusinga for  A levels in 1969. Thereafter in 1970 he was admitted to University of Nairobi for Civil Engineering Course graduating with Honours in 1973.He has a company: Engineering Consultancy Firm in the name of Otieno Odongo and Partners.
'''
s_milicent_info = '''
Milicent Anyango Abudho was Aspirant Women representative of REPUBLIC OF KENYA representing Kisumu between 2013-02-08 and 2013-03-04 
Milicent Anyango Abudho has been Member of The National Alliance (TNA) since 2013-02-08 
Milicent Anyango Abudho has been Coalition Member of Jubilee Alliance since 2013-02-13
'''

s_kiambu = ['Kimani Wamatanga - Jubilee', 'Karungo Thangwa - Jubilee']

s_kimani_info = '''2012 – 2013: St. Pauls University, Degree in Leadership and Management, 1980 – 1989 : Bombay University 2010 – 2012 :  C.E.O, King Group Limited.,2004 – 2012 : Managing Director, Auto Bass Limited.,2008  – 2012 : Director, Total Assurance,2008  – 2012 : Director, Kings Construction
'''
s_karungo_info = '''
Karungo wa Thang'wa is the Member of County Assembly for Ngewa in Kiambu. Karungo Paul Thangwa was Aspirant Ward Representative of REPUBLIC OF KENYA between 2013-02-08 and 2013-03-04 Karungo Paul Thangwa has been Member of The National Alliance (TNA) since 2013-02-08 Karungo Paul Thangwa has been Coalition Member of Jubilee Alliance since 2013-02-13.Karungo Paul Thangwa has been Ward Representative of REPUBLIC OF KENYA since 2013-03-10
'''

w_nairobi = ['Esther Passaris - CORD-ODM', 'Millicent Omanga - Jubilee', 'Rachel Shebesh', 'Karen Nyamu - Jubilee']
w_esther_info = '''Esther Muthoni Passaris OGW (born 20 October 1964) is a Kenyan social entrepreneur, philanthropist, and politician. A member of the Kenya National Congress, she has run for member of parliament for Embakasi Constituency as well as for women's representative for Nairobi County. She is regarded as one of the most well-known female public figures in Kenyan business and politics.
'''

w_rachel_info = '''Rachel is the UN Champion for disaster risk reduction in Africa, where her main role is to promote synergy between disaster risk reduction and climate change adaptation in Africa, and works closely with African parliamentarians to obtain political commitment to disaster risk reduction policies. Her current Political Position is as the 2013 Nairobi women representative. Rachel seems to mingle well the young people hence her supporters gave her the name Manzi wa Nai.
'''
w_millicent_info = '''
Millicent Omanga is a business woman married to one Dr Francis Nyambiobo with two children. Omanga wants to become the next Nairobi Women Representative.
'''
w_karen_info = '''
Karen Nyamu or “Bae wa Nai” (Nairobi's sweetheart) as she is commonly referred by her supporters is a children and women's lawyer, hence, her slogan Wakili wa Watoto na Wamama. 
'''


w_mombasa = ['Sadaf Deen - ODM(NASA)', 'Mishi Juma - ODM']

w_sadaf_info = '''
Sadaf Deen is currently the youngest aspirant for the Mombasa women rep position in Mombasa. She is 20 years old.'''
w_mishi_info = '''
Mishi actively participated in Likoni political campaigns in 1997 and 2002. She vied for Likoni parliamentary seat in 2007 and lost in party nominations which were marred by irregularities. She would like to see government funded drug rehabilitation centres established in Mombasa.
'''
