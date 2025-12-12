import requests

VCENTER = "192.168.1.69"
USER = "administrator@vsphere.local"
PASSWORD = "VMware123!"


requests.packages.urllib3.disable_warnings()

def get_token():
    resp = requests.post(
        f"https://{VCENTER}/rest/com/vmware/cis/session",
        auth=(USER, PASSWORD),
        verify=False
    )
    return resp.json()["value"]

def get_all_vms(token):
    headers = {"vmware-api-session-id":token}

    result = requests.get(
        f"https://{VCENTER}/rest/vcenter/vm",
        headers=headers,
        verify= False
    )
    return result.json()

def get_vm_details(vm_id,token):
    headers = {"vmware-api-session-id":token}
    resp = requests.get(
        f"https://{VCENTER}/rest/vcenter/vm/{vm_id}",
        headers=headers,
        verify = False
    )
    return resp.json()["value"]

def check_tools(vm_list,token):
    print("\n----- VMS Missing Tools -----")
    for vm in vm_list:
        if vm["power_state"] == "POWERED_ON":
            continue
        
        details = get_vm_details(vm["vm"], token)
        tools = details.get("tools",{})
        run_state = tools.get("run_state")
        version_status = tools.get("version_status")

        if run_state != "RUNNING" or version_status != "CURRENT":
            print(f"{vm['name']}  (ID: {vm['vm']}) -- Tools: {run_state}, Version: {version_status}")
            

def main():
    token = get_token()
    print("\nSession token: " + token + "\n\n")
    vms = get_all_vms(token)["value"]
    print("Total VMs found: ", len(vms))
    check_tools(vms,token)

main()
