import os, requests
module_dir=os.path.dirname(__file__)

def remove_forward_slashes(picture_url):
	new_picture_url = ''
	for c in picture_url:
		if c!="\\":
			new_picture_url=new_picture_url+c
	return new_picture_url

def create_sms_array(phone_number):
    file=os.path.join(module_dir, 'textlists/SMS_Gateways.txt')
    with open(file, 'r', errors='ignore', encoding='utf-8') as f:
        array=f.readlines()
    array=[x.strip() for x in array]
    sms_list = []
    for x in range(len(array)):
        sms_list.append(phone_number+'@'+array[x])
    return sms_list

def get_pic_urls():
    file=os.path.join(module_dir, 'textlists/ZooPics.txt')
    with open(file, 'r', errors='ignore', encoding='utf-8') as f:
        urls = f.readlines()
    urls=[x.strip() for x in urls]
    while '' in urls:
        urls.remove('')
    return urls

def get_facts():
    file=os.path.join(module_dir, 'textlists/ZooFacts.txt')
    with open(file, 'r', errors='ignore', encoding='utf-8') as f:
        facts = f.readlines()
    facts=[x.strip() for x in facts]
    while '' in facts:
        facts.remove('')
    return facts

def get_attributions():
    file=os.path.join(module_dir, 'textlists/ZooAttributions.txt')
    with open(file, 'r', errors='ignore', encoding='utf-8') as f:
        att = f.readlines()
    att=[x.strip() for x in att]
    while '' in att:
        att.remove('')
    att.sort()
    for i in range(len(att)):
        if i==0:
            continue
        else:
            if i>=len(att):
                break
            if att[i]==att[i-1]:
                del att[i]
    return att

#    with open(file, 'r', errors='ignore', encoding='utf-8') as f: