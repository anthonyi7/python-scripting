from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# Disable SSL warnings for lab environments
context = ssl._create_unverified_context()

def sizeof_fmt(num, suffix="B"):
    for unit in ['','K','M','G','T','P']:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0

def get_datastore_health(datastore):
    summary = datastore.summary

    health = {
        "Name": summary.name,
        "Type": summary.type,
        "Accessible": summary.accessible,
        "Capacity": sizeof_fmt(summary.capacity),
        "Free Space": sizeof_fmt(summary.freeSpace),
        "Uncommitted": sizeof_fmt(summary.uncommitted) if summary.uncommitted else "N/A",
        "Maintenance Mode": getattr(summary, 'maintenanceMode', "N/A"),
        "Multiple Host Mount": getattr(summary, 'multipleHostAccess', "N/A"),
        "Overall Status": getattr(datastore, 'overallStatus', "unknown")
    }

    # vSAN / heartbeat info if available
    if hasattr(summary, 'redundancyStatus'):
        health["vSAN Redundancy"] = summary.redundancyStatus

    return health

def main():
    si = SmartConnect(
        host="vcenter.anthony.com",
        user="administrator@vsphere.local",
        pwd="VMware123!",
        sslContext=context
    )
    content = si.RetrieveContent()

    datastores = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.Datastore], True
    ).view

    print("\n=== DATASTORE HEALTH REPORT ===\n")

    for ds in datastores:
        health = get_datastore_health(ds)
        for key, val in health.items():
            print(f"{key:20}: {val}")
        print("-" * 60)

    Disconnect(si)

if __name__ == "__main__":
    main()
