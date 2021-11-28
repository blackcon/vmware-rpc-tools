from ctypes import *
from ctypes.wintypes import DWORD, LPCSTR
from keystone import *

VirtualProtect = windll.kernel32.VirtualProtect
VirtualAlloc = windll.kernel32.VirtualAlloc
VirtualFree = windll.kernel32.VirtualFree
RtlMoveMemory = windll.kernel32.RtlMoveMemory

def Backdoor():
    ks = Ks( KS_ARCH_X86, KS_MODE_32 )

    encoding, cnt = ks.asm(
        b'mov eax,564D5868h;'
        b'mov ecx, 01;' # 01. GET Processor speed (MHz)
                        # backdoor's command(ref. open-vmtools)
        b'mov edx, 5658h;'
        b'in eax, dx;'
        b'ret'
    )
    asm = "".join( map( chr, encoding ) )
    return asm

def main():
    PAGE_EXECUTE_READWRITE = 0x40
    _code = Backdoor()
    ASM = bytearray(_code)

    # Allocation memory for shellcode
    ptr = VirtualAlloc( c_int(0),
                        c_int( len(ASM) ),
                        c_int( 0x3000 ),
                        c_int( PAGE_EXECUTE_READWRITE ))

    # Change permition of memory
    old = c_long(1)
    VirtualProtect( c_int(ptr),
                    c_int(len(ASM)),
                    PAGE_EXECUTE_READWRITE,
                    byref(old) )
    
    # move memory from ASM to buf
    buf = (c_char*len(ASM)).from_buffer(ASM)
    RtlMoveMemory( c_int(ptr),
                   buf,
                   c_int(len(ASM)) )

    # Execute BackdoorCommand
    execBdoor = cast( ptr, CFUNCTYPE(c_void_p) )
    ret = execBdoor()
    print "[+] return: {0}".format( hex(ret) )
    VirtualFree(ptr)
    
    
if __name__ == "__main__":
    main()
