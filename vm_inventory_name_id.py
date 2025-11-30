import requests

VCENTER = "" #your vcenter IP or FQDN here
USER = "" #your vcenter username here
PASSWORD = "" #your vcenter password here

#disable SSL warnings

requests.packages.urllib3.disable_warnings()

#1 create session to vcenter

session = requests.post(
    f"https://{VCENTER}/rest/com/vmware/cis/session",
    auth=(USER, PASSWORD),
    verify=False
)

print("Raw session response: ", session.text)

#2 parse token

try:
    token = session.json().get("value")
except Exception as e:
    print("Could not parse JSON from session response")
    print("Error: ", e)
    exit(1)

print("Session token: ", token)

#3  send API call to get the VM list

headers = {"vmware-api-session-id": token}

vms = requests.get(
    f"https://{VCENTER}/rest/vcenter/vm",
    headers = headers,
    verify = False
)

print ("\nRaw VM resposne" + vms.text)

#4 parse VM list

try:
    vm_list = vms.json()["value"]
except Exception as e:
    print("Could not parse VM list - API may have failed")
    print("Error: ", e)
    exit(1)

#5 print VM names 

print("\nVM List")
for vm in vm_list:
    print(f"- {vm.get('name')}  (ID: {vm.get('vm')})")
