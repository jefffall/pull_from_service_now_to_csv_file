#================================================================================
# SNOW ticket processing 2nd program to run pull json from disk and process to csv
#================================================================================
import json
import datetime
import time
import calendar
import re
 
 
def apply_fixes(line):
 
    try:
        line = str(line)
        line = line.replace('\\r',' ',200)
        line = line.replace('\\n',' | ',200)
        line = line.encode().decode('ascii', 'replace').replace(u'\ufffd', '_')
        line = line.replace("'","\"",2000)
        mydict = json.loads(line)
    except:
        parts = line.split('"description"')
        parts[0] = parts[0][:-2] + "}"
        try:
            mydict = json.loads(parts[0])
        except:
            #try:
            moreparts = parts[0].split('short_description')
            moreparts[0] = moreparts[0][:-3] + "}"
            print (moreparts[0])
            bad_json = moreparts[0]
            
            improved_json  = re.sub(r'"\s*$', '",', bad_json, flags=re.MULTILINE)
            #print(improved_json)
        
            # good_json = re.sub(r'(?<!")(?P<word>[\w-]+)\b(?!")', '"\g<word>"',
            #   improved_json)
            # good_json = re.sub(r'(?<[\{\s])(?P<word>[\w-]+)(?=[:\s])', '"\g<word>"',
            #   improved_json)
            # good_json = re.sub(r'([\{\[\s])(?P<word>[\w-]+)([:,\]\s])', '\1"\g<word>"\3',
            #   improved_json)
            good_json = re.sub(r'(?<=[\{\[\s])(?P<word>[\w-]+)(?=[:,\]\s])', '"\g<word>"', improved_json)
            
            print (good_json)
            try:
                mydict = json.loads(good_json)
            except:
                mydict = {}
                mydict['opened_at'] = "?"
                mydict['priority'] = "?"
                mydict['queue'] = "?"
                mydict['number'] = "?"
                mydict['sys_created_by'] = "?"
                mydict['epoch'] = "?"
                mydict['assigned_to'] = "?"
                mydict['sys_updated_on'] = "?"
                mydict['sys_updated_by'] = "?"
                mydict['automation'] = "BAD JSON from Ticket"
                mydict['tool'] = "BAD JSON"
                mydict['case'] = "BAD JSON from Ticket"
                mydict['description'] = "BAD JSON from Ticket"
    return mydict          
 
def date_to_epoch(date_time):
    parts = date_time.split(" ")
    mydate = str(parts[0])
    mytime = str(parts[1])
    
    mydates = mydate.split("-")
    mytimes = mytime.split(":")
    
    myyear = mydates[0]
    myday = mydates[2]
    mymonth = mydates[1]
    
    myhour = mytimes[0]
    myminute = mytimes[1]
    mysecond = mytimes[2]
    '''
    YEAR, Month, Day, Hr, Minute, Sec
    '''
    epoch_time=datetime.datetime(int(myyear), int(mymonth), int(myday), int(myhour), int(myminute), int(mysecond)).timestamp()
    return int(epoch_time)
 
 
def get_epoch(mylist):
    return mylist.get('epoch')
 
 
 
def process_automation(case):
   
    automation_action = ""
    automation = False
    if "dallas" in case:
        automation_action = "DALLAS "
        automation = True
    if "password" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "PASSWORD "
        automation = True
    if "access" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "ACCESS "
        automation = True
    if "openvpn" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "OPENVPN "
        automation = True
    if "oci" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "OCI "
        automation = True
    if "unlock" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "UNLOCK ACCOUNT "
        automation = True
    if "imzcloud" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "CLOUD "
        automation = True
    if "sone_keyword" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "SOME KEYAORD "
        automation = True
    if "itim" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "SERVER "
        automation = True
    if "3.x" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "PORTAL "
        automation = True
    if "reset" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "RESET "
        automation = True
    if "server" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "SERVER "
        automation = True
    if "create" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "CREATE "
        automation = True
    if "sudo" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "SUDO "
        automation = True
    if "users" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "USERS "
        automation = True
    if "modify" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "MODIFY "
        automation = True
    if "profile" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "PROFILE "
        automation = True
    if "onboarding" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "ONBOARDING "
        automation = True
    if "employee" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "EMPLOYEE "
        automation = True
    if "delete" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "DELETE "
        automation = True
    if "user" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "USER "
        automation = True
    if "connect" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "CONNECT "
        automation = True
    if "vpn" in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "VPN "
        automation = True
    if "vulnerability " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "VULNERABILITY "
        automation = True
    if "aws " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "AWS "
        automation = True
    if "issue " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "ISSUE "
        automation = True
    if "remove " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "REMOVE "
        automation = True
    if "client " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "CLIENT "
        automation = True
    if "login " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "LOGIN "
        automation = True
    if "system " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "SYSTEM "
        automation = True
    if "server " in case:
        if automation == True:
            automation_action = automation_action + " + "
        automation_action = automation_action + "SERVER "
        automation = True
 
    if automation == False:
        automation_action = ""
        
    return automation_action
 
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def assign_resolution_tool(issue):
    if "USECASE1" in issue or "usecase1" in issue:
        return "https://url1.com"
    if "USECASE2" in issue or "usecase2" in issue:
        return "https://url2.comn"
    if "USECASE3" in issue or "usecase3" in issue:
        return "https://url3.com"
    if "USECASE4" in issue or "usecase3" in issue:
        return "https://url4.com"
       
    return ""

 
 
def write_ticket(fpout, line):
    tool_url = ""
    try:
        parts = line['opened_at'].split(" ")
        fpout.write(str(parts[0])+",")
        fpout.write(str(parts[1])+",")
    except:
        #continue
        print("exception: opened_at")
        fpout.write("Bad JSON"+",")
    try:
        ist_time = int(line['epoch']) + 19800
        fpout.write(epoch_time_to_am_pm(ist_time)+",")
    except:
        pass
    try:
        est_time =  int(line['epoch']) - 18000
        fpout.write(epoch_time_to_am_pm(est_time)+",")
    except:
        pass
    try:
        pst_time = int(line['epoch']) - 28800
        fpout.write(epoch_time_to_am_pm(pst_time)+",")
    except:
        pass
   
    try:
        fpout.write(line['priority']+',')
    except:
        #continue
        print("exception: priority")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(line['queue']+',')
    except:
        #continue
        print("exception: queue")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(line['number']+',')
    except:
        #continue
        print("exception: number")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(line['sys_created_by']+',')
    except:
        #continue
        print("exception: sys_created_by")
        fpout.write("Bad JSON"+",")
    try:
        current_epoch_time = int(calendar.timegm(time.gmtime()))
        current_epoch_time = current_epoch_time + 28800 # convert to GMT from PST
        delta = current_epoch_time - int(line['epoch'])
        days_open = str(round(float(delta) / float(86400), 1))
        fpout.write(str(days_open)+',')
    except:
        #continue
        print("exception: days_open")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(line['assigned_to']+',')
    except:
        #continue
        print("assigned_to")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(line['sys_updated_on']+',')
    except:
        #continue
        print("exception: sys_updated_on")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(line['sys_updated_by']+',')
    except:
        #continue
        print("exception: sys_updated_by")
        fpout.write("Bad JSON"+",")
    try: 
        # resolved
        if line['resolved_by'] == '':
            fpout.write(" "+",")
        else:
            fpout.write("YES"+",")
    except:
        print("exception: resolved_by")
        fpout.write("Bad JSON"+",")  
    try:
        automation_action_case  = process_automation(line['case'].casefold())
        automation_action_description = process_automation(line['description'].casefold())
        automation_actions = automation_action_case + automation_action_description
        tool_url = assign_resolution_tool(automation_actions)
        automation_actions =' '.join(unique_list(automation_actions.split()))
        fpout.write(automation_actions+",")
    except:
        print("exception: automation_error")
        fpout.write("Automation Error,")
    try:
        mylink = ""
        if tool_url != "":
            #mylink = '"=HYPERLINK(""'+tool_url+'"",""'+"Click -> Some Tool"+'"")"'
            mylink = tool_url
        tool = mylink
        fpout.write(tool+",")
    except:
        print("exception: tool_error")
        fpout.write("TOOL Error,")
    try:
        fpout.write(str(line['case']).strip().replace("\n"," ").replace('\r',' ',1000).replace(","," ").replace('\u200b', '')+",")
    except:
        print("exception: case")
        fpout.write("Bad JSON"+",")
    try:
        fpout.write(str(line['description']).strip().replace("\n"," ").replace('\r',' ',1000).replace(","," - ").replace('\u200b', ''))
    except:
        print("exception: description")
        fpout.write("Bad JSON"+",")
    fpout.write("\n")
    
    fpout.flush()
 
def print_tickets(mylist):
    for line in mylist:
    
        ticket_count = ticket_count + 1
        print ("Ticket #", ticket_count)
        try:
            print ("NUMBER: ",line['number'])
            print ("OPENED DATE:", line['opened_at'])
            print ("PRIORITY: ",line['priority'])
            print ("CASE: ",line['case'])
            print (line['description'])
            print ('---------------------------------------')
        except:
            print ("Error in JSON")
            exit(0)
            
            
def epoch_time_to_am_pm(epoch):
    datetime_time = datetime.datetime.fromtimestamp(epoch)
    pm = "AM"
    parts = str(datetime_time).split(" ")
    hms = parts[1].split(":")
    hours = int(hms[0])
    minutes = str(hms[1])
    seconds = str(hms[2])
    if hours > 12:
        pm = "PM"
        hour = str(hours - 12)
    else:
        hour = str(hours)
    return hour+":"+minutes+":"+seconds+" "+pm
      
     
'''
================================================================================================================
|    Main begins here                                                                                          |
================================================================================================================
'''
 
myfp = open('/Users/yourloginid/tickets_json.txt','r')
 
mylist = []
 
for line in myfp:
    print (line)
    result = apply_fixes(line)
    mylist.append(result)
    
 
''' 
mylist = []
for line in myfp:
    mylist.append(json.loads(line))
'''    
 
ticket_count = 0
 
for line in mylist:
    line.update({'epoch' : 0})
    
    
for line in mylist:
    try:
        line.update({'epoch' : date_to_epoch(line['opened_at'])})
        #print (date_to_epoch(line['opened_at']))
    except:
        continue
        print ("exception: line.update({'epoch' : 0})")
        line.update({'epoch' : 0 })
 
mylist.sort(key=get_epoch, reverse=True)
 
print (ticket_count,"Tickets found.")
 
fpout = open('/Users/yourloginidl/Downloads/new_tickets.csv','w')
 
ticket_count = 0
 
fpout.write("GMT Date,GMT Time,IST,EST,PST,Priority,Queue,Ticket #,Created by,Days open,Assigned to,GMT Updated On,Updated by,Resolved,Automation Routing,Resolution URL,Case,Description\n")
fpout.flush()
 
for line in mylist:
        if line['resolved_by'] == '': # Not resolved
            ticket_count = ticket_count + 1
            print ("Writing ticket #",ticket_count,"to csv file...")
            write_ticket(fpout, line)
     
print ("wrote /Users/yourloginid/Downloads/new_tickets.csv at ", ticket_count, "lines")   
    
fpout.close()
 
