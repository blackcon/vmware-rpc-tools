# vmware-rpc-tools
### 1. vmware rpc sniffer
 - Languate: `Python 3.7.2`
 - Module: `FRIDA` (python library for hooking)
 - Target
   - Vmware Workstation 15
   - Runing tool on `host` enviroment
 - Description
   - In vmware, host and guest communicate using rpc.
   - This tool(rpc-sniffer.py) was made for easy viewing of data between communication.
   - The core of the tool is to output the corresponding argument by hooking a specific function of the target process.
 - Logic
   - `Analyze the vmware-vmx.exe` binary to check the offset of the `execRPCFunc`.
   - Using Frida, attach to the target process and get the base address.
   - Hook at the location the execRPCFunc (base_address + offset)
   - Outputs the argument value passed to the function.
 - Result
   ![Result Sniff](https://github.com/blackcon/vmware-rpc-tools/blob/main/images/1.%20result%20sniff.png?raw=true)


### 2. vmware rpci fuzzer (`draft version`)
 - Languate: `Python 2.7.17`
 - Module
   - `keystone` (asm tools)
   - `ctypes`
 - Target
   - Vmware Workstation 15
   - Runing tool on `guest` enviroment
 - Concenpt
   - Randomly generates various commands.([CommandList](https://github.com/vmware/open-vm-tools/blob/master/open-vm-tools/lib/include/backdoor_def.h))
   - Request the created chunks in random order.
 - Reference
   - https://sites.google.com/site/chitchatvmback/backdoor
  - Result
   ![Result Backdoor](https://github.com/blackcon/vmware-rpc-tools/blob/main/images/2.%20result%20backdoor.png?raw=true)
