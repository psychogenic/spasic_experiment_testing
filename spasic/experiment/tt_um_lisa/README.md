# LISA

This experiment runs a simple LISA test and sends the output down the satellite link.
The processor is fed opcodes via a PIO programmed from Python with up to 64 16-bit
opcodes PUSHed to the PIO FIFOs.  Then the processor is either single-stepped
or breakpoints are set and the core is allowed to run to the breakpoint.  Then additional
opcodes are PUSHed to the FIFO, additional breakpoints, etc.

## Expected results

The experiment should progress as follows:

| Stage                      | Reported bytes                                     |
|----------------------------|----------------------------------------------------|
| LISA Debugger detected     | `0x1  0x0  0x0  0x0  0x0  0x0  0x0  0x0  0x0  0x0` |
| LISA Configuration Success | `0x2  0x0  0x0  0x0  0x0  0x0  0x0  0x0  0x0  0x0` |
| LISA Single Step Success   | `0xf  0x0  0x0  0x0  0x0  0x0  0x0  0x0  0x0  0x0` |
| LISA Opcode Tests Pass     | `0xf  0x0  0x0  0xff 0xff 0xff 0x7f 0x0  0x0  0x0` |
| Final result               | `0xf  0x42 0x28 0xff 0xff 0xff 0x7f 0x24 0x7  0x1` |
                                     ---------                       ^    ^    ^ 
                                   BF16 "42.0"(Calcualted)           |    |    |
                                                                     |    |  Success
                                         ^                           |    |
                                         |                           | Number of 'LISA'
                               Also reports expected                 | strings received from
                               and actual PC if break                | uC UART2 by RP2040
                               failed.  Then  "Success"              |
                               byte will be 0x00             Number of times the 
                                                             127ms timer rolled over


