import json
import urllib3
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from prettytable import PrettyTable
from datetime import datetime
import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

issueLinkDictHigh = {}
issueLinkDictMedium = {}
issueLinkDictLow = {}

newDict={}
urllib3.disable_warnings()
tabular_table = None
totalBugs = 0
FTVAgeM = 0
FTVAgeMM = 0
FTVAgeMMM = 0
RokuAgeM = 0
RokuAgeMM = 0
RokuAgeMMM = 0
LAgeM = 0
LAgeMM = 0
LAgeMMM = 0
FTVTriaged = 0
FTVUnTriaged = 0
RokuTriaged = 0
LTriaged = 0
RokuUnTriaged = 0
LUnTriaged = 0


linkURL = "https://maxis-service-prod-pdx.amazon.com/issues?q=status:Open%20AND%20createDate:[2022-12-31T18:30:00.000Z%20TO%202023-12-30T18:30:00.000Z]%20AND%20tags:%22GDQ_QS_Detected_IMDb%20TV%22"
issuesURL = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)&sort=score+desc&selectedDocument=67343495-24cd-4aff-a105-69faded4563f"

def prepareTable():
    html_body_header = '<font face="Calibri">Hi All, <br> '
    html_body_header = html_body_header + '<br><font face="Calibri">Please find the 2023 open bug report for each component. Requesting corresponding POCs to take action on the bugs in their queue.<br> <br>'
    html_body=html_body_header+'<style type="text/css">\n\
                        .tg  {border-collapse:collapse;border-spacing:0;}\n\
                        .tg td{font-family:Calibri;font-size:14px;padding:3px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}\n\
                        .tg th{font-family:Calibri;font-size:14px;font-weight:normal;padding:3px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}\n\
                        .tg .tg-vkco{font-weight:bold;font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;background-color:#f59614;vertical-align:top\n\
                        .tg .tg-kl7f{font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;vertical-align:top}\n\
                        .tg .tg-mer2{font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;text-align:right;vertical-align:top}\n\
                        .tg .tg-4n4u{font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;background-color:#82378c;color:#cbcefb;vertical-align:top}\n\
                        .tg .tg-8i5d{font-weight:bold;font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;background-color:#f59614;text-align:right;vertical-align:top}\n\
                        .tg .tg-s1pv{font-weight:bold;font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;background-color:#82378c;color:#cbcefb;vertical-align:top}\n\
                        .tg .tg-status{font-size:11px;font-family:Arial, Helvetica, sans-serif !important;;text-align:right;vertical-align:top;color:#cbcefb;}\n\
                        </style>'

    totalLink = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)&sort=score+desc&selectedDocument=67343495-24cd-4aff-a105-69faded4563f"
    html_body=html_body+'<table class="tg">'+'\n'+'<tr>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">No of Open Bugs'+'</th>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri"><a href='+totalLink+'>'+str(totalBugs)+'</a></th>'
    html_body= html_body+ '\n' +'<td colspan="3" bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">Aging'+'</td>'
    html_body= html_body+ '\n' +'<td rowspan="2" bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">Triaged'+'</td>'
    html_body= html_body+ '\n' +'<td rowspan="2" bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">Untriaged'+'</td>'

    html_body=html_body+'\n'+'</tr>'

    html_body=html_body+'\n'+'<tr>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0"><B><font face="Calibri">Component'+'</th>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0"><B><font face="Calibri">Open Bugs'+'</th>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0"><B><font face="Calibri"><30 days'+'</th>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0"><B><font face="Calibri">30-60 days'+'</th>'
    html_body= html_body+ '\n' +'<th bgcolor="#90B8E0"><B><font face="Calibri">>60 days'+'</th>'

    html_body=html_body+'\n'+'</tr>'

    for key,value in newDict.items():
        html_body=html_body+'\n'+'<tr>'
        if key == "FTV":
            FTVIssueLink = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)+tags%3A(FTV)&sort=score+desc&selectedDocument=67343495-24cd-4aff-a105-69faded4563f"
            FTVUnT_Link = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)+tags%3A(FTV)+-tags%3A(Triaged)&sort=score+desc&selectedDocument=e9702efb-f5f2-4d87-b882-557e488c6c9b"

# highIssueLink = ""
##            mediumIssueLink = ""
##            lowIssueLink =""
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+key+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center"><a href='+FTVIssueLink+'>'+str(value['total'])+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(FTVAgeM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(FTVAgeMM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(FTVAgeMMM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(FTVTriaged)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center"><a href='+FTVUnT_Link+'>'+str(FTVUnTriaged)+'</td>'

            html_body = html_body +'\n'+'</tr>'

        if key == "Roku":
            RokuIssueLink = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)+tags%3A(Roku)&sort=score+desc&selectedDocument=67343495-24cd-4aff-a105-69faded4563f"
            RokuUnT_Link = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)+tags%3A(Roku)+-tags%3A(Triaged)&sort=score+desc&selectedDocument=b95834c8-c6f0-4e05-a1ce-2833bfe2b447"
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+key+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center"><a href='+RokuIssueLink+'>'+str(value['total'])+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(RokuAgeM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(RokuAgeMM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(RokuAgeMMM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(RokuTriaged)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center"><a href='+RokuUnT_Link+'>'+str(RokuUnTriaged)+'</td>'


            html_body = html_body +'\n'+'</tr>'

        if key == "Linear channel":
            LinearIssueLink = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)+tags%3A(%22Linear+channel%22)&sort=score+desc&selectedDocument=67343495-24cd-4aff-a105-69faded4563f"
            LinearUnT_Link = "https://sim.amazon.com/issues/search?q=status%3A(Open)+createDate%3A(%5B2022-12-31T18%3A30%3A00.000Z..2023-12-30T18%3A30%3A00.000Z%5D)+tags%3A(%22GDQ_QS_Detected_IMDb+TV%22)+tags%3A(%22Linear+channel%22)+-tags%3A(Triaged)&sort=score+desc&selectedDocument=b95834c8-c6f0-4e05-a1ce-2833bfe2b447"
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+key+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center"><a href='+LinearIssueLink+'>'+str(value['total'])+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(LAgeM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(LAgeMM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(LAgeMMM)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center">'+str(LTriaged)+'</td>'
            html_body = html_body+ '\n' +'<td  class="tg-mer2" style="text-align:center"><a href='+LinearUnT_Link+'>'+str(LUnTriaged)+'</td>'

            html_body = html_body +'\n'+'</tr>'
            html_body = html_body +'\n'+'</tr>' 

    html_body = html_body+'\n'+'</table><br><font face="Calibri">This is an automated email. Do not reply.<br><br>Thanks,<br>Freevee QS'

    return html_body

def sendMail():
    TO = "hdavisvi@amazon.com; klsathis@amazon.com"   #hdavisvi@amazon.com; klsathis@amazon.com; ugiree@amazon.com"icb-cx-qa-sea@amazon.com; rsamarth@amazon.com; yeshask@amazon.com: abhinayy@amazon.co.uk"   #To add multiple email addresses, start with single/double quotes and type each email with a semicolon between each email address, then end the line with quotes
    CC = ""   #"mahayuv@amazon.com; mmatha@amazon.com"

    #fullMailList = [y for x in [TO, CC] for y in x]
    #my_string = ','.join(fullMailList)

    HtmlBody = prepareTable()
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = 'FreeVee Open Bug report'
    MESSAGE['From'] = "FreeVee-Open-bug-reports@amazon.com"
    MESSAGE['To'] = TO
    MESSAGE['CC'] = CC
    MESSAGE.preamble = """
    """
    HTML_BODY = MIMEText(HtmlBody, 'html')
    MESSAGE.attach(HTML_BODY)

    smtpObj = smtplib.SMTP('smtp.amazon.com')
    #smtpObj.sendmail("ICB-open-bug-report@amazon.com", fullMailList.split(","), MESSAGE.as_string())
    #smtpObj.sendmail("ICB-open-bug-report@amazon.com", fullMailList, MESSAGE.as_string())
    #smtpObj.sendmail("ICB-open-bug-report@amazon.com", my_string.split(","), MESSAGE.as_string())
    smtpObj.sendmail("FreeVee-Open-bug-reports@amazon.com", ["klsathis@amazon.com", "hdavisvi@amazon.com", ""], MESSAGE.as_string()) #"klsathis@amazon.com", "hdavisvi@amazon.com", #Add all people from "TO and CC" within double quotes inside square bracket of this line(separated by comma and a space) like this ["icb-cx-qa-sea@amazon.com", "rsamarth@amazon.com", "yeshask@amazon.com", "abhinayy@amazon.co.uk", "rprabaka@amazon.com", "mmatha@amazon.com", "ugiree@amazon.com", "skertha@amazon.com", "harishas@amazon.com"]
    smtpObj.quit()

def fetchDetails():
    global issueLinkDict, FTVAgeM, FTVAgeMM, FTVAgeMMM, RokuAgeM, RokuAgeMM, RokuAgeMMM, LAgeM, LAgeMM, LAgeMMM, FTVTriaged, FTVUnTriaged, RokuTriaged, RokuUnTriaged, LTriaged, LUnTriaged
    print(len(issueLinkDict["documents"]))
    for value in issueLinkDict["documents"]:
        try:
            Tags = value ['tags']
            CreateDate = ((value['createDate']).split('T')[0])
            tagNumber = [tg["id"] for tg in Tags]
            Today = (str(datetime.now())).split(' ')[0]
            d2 = datetime.strptime(Today, "%Y-%m-%d")
            d1 = datetime.strptime(CreateDate, "%Y-%m-%d")
            Age = d2 - d1
            Calc = int(Age.days)
            for x in tagNumber:
                if x == "FTV":
                    PODName = "FTV"
                    if Calc < 30:
                        FTVAgeM += 1
                    if Calc > 30 and Calc < 60:
                        FTVAgeMM += 1
                    if Calc > 60:
                        FTVAgeMMM += 1
                elif x == "Roku":
                    PODName = "Roku"
                    if Calc < 30:
                        RokuAgeM += 1
                    if Calc > 30 and Calc < 60:
                        RokuAgeMM += 1
                    if Calc > 60:
                        RokuAgeMM += 1
                elif x == "Linear channel":
                    PODName = "Linear channel"
                    if Calc < 30:
                        LAgeM += 1
                    if Calc > 30 and Calc < 60:
                        LAgeMM += 1
                    if Calc > 60:
                        LAgeMMM += 1
                else:
                    pass
            #print (PODName, value['aliases'][0]["id"])
            #print(CreateDate)
            #print(f'Age is {Age.days} days')

        except:
            reqName = ((value['requesterIdentity']).split(':')[1]).split('@')[0]
            PODName = "OtherTasks"
            print (PODName, value['aliases'][0]["id"])
            CreateDate = ((value['createDate']).split('T')[0])
            Today = (str(datetime.now())).split(' ')[0]
            d2 = datetime.strptime(Today, "%Y-%m-%d")
            d1 = datetime.strptime(CreateDate, "%Y-%m-%d")
            Age = d2 - d1
            print(CreateDate)
            print(f'Age is {Age.days} days')

        Tags = value ['tags']
        tagNumber = [tg["id"] for tg in Tags]
        if 'FTV' in tagNumber:
            if 'Triaged' in tagNumber:
                FTVTriaged += 1
            else:
                FTVUnTriaged += 1
        if 'Roku' in tagNumber:
            if 'Triaged' in tagNumber:
                RokuTriaged += 1
            else:
                RokuUnTriaged += 1
        if 'Linear channel' in tagNumber:
            if 'Triaged' in tagNumber:
                LTriaged += 1
            else:
                LUnTriaged += 1

        try:
            priorityValue = value['extensions']['backlog']['priority']
        except:
            priorityValue = 0.5 # When no priority found, assign it medium value

        if PODName not in newDict.keys():
            newDict[PODName] = {'total':0,'high':0,'medium':0,'low':0}

        if priorityValue < 0.3:
            newDict[PODName]['low'] = newDict.get(PODName).get('low', 0) + 1 if newDict.get(PODName) else 1
        elif (priorityValue > 0.3) and (priorityValue < 0.7):
            newDict[PODName]['medium'] = newDict.get(PODName).get('medium', 0) + 1 if newDict.get(PODName) else 1
        else:
            newDict[PODName]['high'] = newDict.get(PODName).get('high', 0) + 1 if newDict.get(PODName) else 1

        newDict[PODName]['total'] = newDict.get(PODName).get('total', 0) + 1 if newDict.get(PODName) else 1
    print(FTVAgeM, FTVAgeMM, FTVAgeMMM)
    print(RokuAgeM, RokuAgeMM, RokuAgeMMM)
    print(LAgeM, LAgeMM, LAgeMMM)
    print(FTVTriaged, FTVUnTriaged)
    print(RokuTriaged, RokuUnTriaged)
    print(LTriaged, LUnTriaged)

def main():
    global issueLinkDict, totalBugs
    my_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    data = requests.get(linkURL, auth=my_auth, verify=False).text
    issueLinkDict = json.loads(data)
    totalBugs = issueLinkDict["totalNumberFound"]
    token = issueLinkDict["startToken"]
    fetchDetails()

    if totalBugs > 100:
        quotient = totalBugs // 100
        remainder = totalBugs % 100
        if remainder > 0:
            runTime = quotient
            
        else:
            runTime = quotient - 1
        for i in range(runTime):            
            my_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
            linkURLTok = linkURL + '&startToken='+str(token)
            data = requests.get(linkURLTok, auth=my_auth, verify=False).text
            issueLinkDict = json.loads(data)
            totalBugs = issueLinkDict["totalNumberFound"]
            fetchDetails()            

    sendMail()

if __name__=="__main__":
    main()
