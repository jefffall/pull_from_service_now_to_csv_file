#==============
# First program to run
#==============

'''
This program pulls tickets from predefined queues enumerated below from SNOW Service NOW and put the JSON into a text file.
'''
 
import requests
import json
 
# Add your show queues below
snow_queues = ["QUEUE1", "QUEUE2"]
 
# Each user has a unique hash in SNOW         
def pull_assigned_to_user(url):
    if "3ac138cbdb8df30001869476db961333" in url:
        return "someuser@yourcompany.com"
   
    elif "d48694091b108dd0204965f0b24bc444" in url:
        return "user2@yourcompany.com"
    else:
        print ("This user is not cached: ",url)
        user = 'snow_login'
        pwd = 'snow_password'
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )
        
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()
        
        myresponse = response.content.decode('utf-8')
        mydict = json.loads(myresponse)
        print ("Please add this user to the static cache -> ",mydict['result']['user_name'])
        exit(0)
 
def remove_excess_double_quotes(line):
    collect = ""
    linelen = len(line)
    for x in range(0,linelen):
        if line[x] == '"':
            if line[x+1] == "," or line[x+1] == "}" or  line[x+1] == '"' or line[x+1] == ':' or line[x+1] == ': ' or line[x-1] == "{" or (line[x-1] == " " and line[x-2] == ",") or (line[x-1] == " " and line[x-2] == ":"):
                collect = collect + (line[x])
            else:
                pass
        else:
            collect = collect + (line[x])
    return collect
 
def fix_double_quotes_in_descriptions(line):
    '''
    # this is the problem string: Full Access"",
    # this is permitted: ': "",'
    '''
    line = str(line)
    new_string = ""
    mylen = len(line)
    for x in range(0,mylen):
        if line[x] == '"' and line[x+1] == '"':
            if line[x-2] == ":" and line[x-1] == " ":
                new_string = new_string + line[x]
            else:
                x = x + 1
        else:
            new_string = new_string + line[x]
    try:
        mydict = json.loads(new_string)
    except:
        print ("Original line:")
        print (line)
        print ("ERROR LINE is below:")
        print(new_string)
        mydict = False
    return mydict
 
def get_snow_queue(queue):
    url = 'https://yourcompany.service-now.com/api/now/table/sn_customerservice_case?&sysparm_order=sys_created_on &sysparm_order_direction=desc&sysparm_query=sys_created_onONLast%20hour@javascript:gs.hoursAgoStart(336)@javascript:gs.hoursAgoEnd(0)&assignment_group='+str(queue)
 
    user = 'snow_user'
    pwd = 'snow_password'
        
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
        
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )
        
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit(0)
    # Decode the JSON response into a dictionary and use the data
    json_data = response.json()
    
    # assign queue`
    for line in json_data['result']:
        line['queue']= queue
    return json_data
     
def fix_noise_in_line(line):
    line = str(line)
   
    line = line.replace("'","\"",1000)
    
    line = str(line).replace("u_","").strip()
    line = line.replace("'","\"")
    line = line.replace("\\","",200)
    line = line.replace("u200b","",200)
    line = line.replace('AddOnly Error: {','", "')
    line = line.replace(' } { ','", "')
    try:
        line = json.loads(line)
    except:
        try:
            line = remove_excess_double_quotes(line)
        except:
            try:
                myresult = fix_double_quotes_in_descriptions(line)
                if myresult != False:
                    line = myresult
                else:
                    print ("Fix double quotes in description failed")
                    exit (0)
            except:
                print ("fix_double_quotes_in_descriptions failed")
    return line
   
 
def scan_tickets_for_user_links(json_data):
    for line in json_data['result']:
        mytemp = line['assigned_to']
        #print (str(type(mytemp)))
        if str(type(mytemp)) == "<class 'dict'>":
            #print (mytemp['link'])
            user_name = pull_assigned_to_user(mytemp['link'])
            #print (user_name)
            line['assigned_to'] = user_name
        else:
            line['assigned_to'] = 'not assigned...'
            
'''
#################################################################################################
MAIN
#################################################################################################
'''
            
myfp = open('/Users/yourloginid/tickets_json.txt', 'w')  
                     
ticket_count = 0  
         
for queue in snow_queues:
    print ("Processing Queue: ",queue)
    print(" ")
    json_result = get_snow_queue(queue)
    
    scan_tickets_for_user_links(json_result)
 
    
    per_queue_ticket_count = 0
    print ("------ top --------")
    for line in json_result['result']:
        per_queue_ticket_count = per_queue_ticket_count + 1
        ticket_count = ticket_count + 1
        print("QUEUE: ",queue,"Ticket: ",per_queue_ticket_count)
        line = fix_noise_in_line(line)
        #print (str(line)) # <<------ !!!!
        myfp.write(str(line)+"\n")
    print(" ")         
myfp.close()
 
print ("Done processing all known SNOW ticket queues...")
print (" ")
print ("Now run 'read from disk' program to process JSON entries gathered for ", ticket_count," tickets")
