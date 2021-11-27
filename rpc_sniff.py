import frida, sys

frida_script = '''
var vmware_vmx = Module.findBaseAddress("vmware-vmx.exe");

// var execRPCfunc = vmware_vmx.add(0xA3A5C); // for vmx_20190515
var execRPCfunc = vmware_vmx.add( 0x778E0 );   // for vmx_15.1_20200218

console.log("vmware-vmx : " + vmware_vmx.toString(16));
console.log("rpc parser : " + execRPCfunc.toString(16));

Interceptor.attach(execRPCfunc, 
    {
        onEnter: function(args) {
            // read from r8 to r8+r9
            var func = this.context.rbx.toString(16)
            var offset = (this.context.rbx.toInt32()-vmware_vmx.toInt32()).toString(16)

            var buffer = this.context.r8;
            var length = this.context.r9.toInt32();
            var data = Memory.readByteArray(buffer, length);
            console.log("==========================================================================="); 

            console.log("Function Addr: "+func+"\toffset: "+offset);  
            console.log("Request length: " + length);
            console.log("Packet: ");
            console.log(data);

            console.log( JSON.stringify(this.context) );
            console.log("===========================================================================");
        },

        onLeave: function(retval) {
        },        
    });
'''

def on_message( message, data ):
    print( "[{0}] => {1}".format( message, data ) )

def main():
    process = "vmware-vmx.exe"
    session = frida.attach( process )

    script = session.create_script( frida_script )

    script.on( "message", on_message )
    script.load()
    print("=======================================")
    print("[!] Ctrl+D on UNIX, Ctrl+Z on Windows/cmd.exe to detach from instrumented program.\n\n")
    sys.stdin.read()
    session.detach()
if __name__ == "__main__":
    main()