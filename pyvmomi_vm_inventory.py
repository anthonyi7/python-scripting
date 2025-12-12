from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

context = ssl._create_unverified_context()

si = SmartConnect(
    host="192.168.10.69",
    user="administrator@vsphere.local",
    pwd="VMware123!",
    sslContext=context
)

content = si.RetrieveContent()


container = content.viewManager.CreateContainerView(
    content.rootFolder,
    [vim.VirtualMachine],  # type of object to search
    True
)

for vm in container.view:
    print(vm.name, vm.runtime.powerState)



# from pyVim.connect import SmartConnect, Disconnect
# # SmartConnect = login wrapper for SOAP API
# # Disconnect = gracefully close session

# from pyVmomi import vim
# # vim object model = all vSphere managed objects (VM, host, datastore…)

# import ssl
# # imported to create a context that ignores SSL certs

# context = ssl._create_unverified_context()
# # prevents SSL errors from vCenter's self-signed certificate

# si = SmartConnect(…)
# # connect to vCenter SOAP endpoint
# # return a ServiceInstance

# content = si.RetrieveContent()
# # get vCenter’s entire inventory

# container = content.viewManager.CreateContainerView(
#     content.rootFolder,           # where to start the search
#     [vim.VirtualMachine],         # what object type to find
#     True                          # recursive search
# )

# for vm in container.view:
#     print(vm.name, vm.runtime.powerState)
# # loop through VM objects and print properties