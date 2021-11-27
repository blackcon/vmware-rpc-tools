# vmware-rpc-tools
### 1. vmware rpc sniffer
 - Languate: `Python`
 - Module: `FRIDA` (python library for hooking)
 - Target: Vmware Workstation 15
 - Description
   - In vmware, host and guest communicate using rpc.
   - This tool(rpc-sniffer.py) was made for easy viewing of data between communication.
   - The core of the tool is to output the corresponding argument by hooking a specific function of the target process.
 - Logic
   - `Analyze the vmware-vmx.exe` binary to check the offset of the `execRPCFunc`.
   - Using Frida, attach to the target process and get the base address.
   - Hook at the location the execRPCFunc (base_address + offset)
   - Outputs the argument value passed to the function.
