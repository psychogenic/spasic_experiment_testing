'''
'''
import time
import machine
from spasic.experiment.experiment_result import ExpResult
from spasic.experiment.experiment_parameters import ExperimentParameters


def wait(n: int = 1) -> None:
    time.sleep_ms(n)
    pass


def addr_set(tt, uio_in: int, bf: bool = None, skip_commit: bool = False) -> int:
    if bf is None:
        uio_in ^= 0x1 # invert
    elif bf:
        uio_in |= 0x1 # A1
    else:
        uio_in &= ~0x1 # A0
    if not skip_commit:
        tt.uio_in.value = uio_in
        wait()
    return uio_in


def clock_on(tt) -> None:
    tt.pins.pin_rp_projclk.on()


def clock_off(tt) -> None:
    tt.pins.pin_rp_projclk.off()


def clock_cycle(tt, count: int = 1) -> None:
    while count > 0:
        if tt.pins.pin_rp_projclk():
           clock_off(tt)
           wait()
        clock_on(tt)
        wait()
        count -= 1


def populate_response(ba: bytearray, count: int, r: int, c: int, good_count: int, last: int) -> None:
    ba[0:4] = count.to_bytes(4, 'little')
    ba[4:6] = r.to_bytes(2, 'little')
    ba[6:8] = c.to_bytes(2, 'little')
    ba[8:12] = good_count.to_bytes(4, 'little')
    ba[12:13] = last.to_bytes(1, 'little')
    #print(f'RESULT = {ba}')
    return count


def entrypoint(params:ExperimentParameters, response:ExpResult):
    # Response structure will be:
    #  FIXME
    response.result = bytearray(10)

    # Read parameters
    p_mode   = int.from_bytes(params.argument_bytes[0:1], 'little') & 0xff
    p_bits   = int.from_bytes(params.argument_bytes[1:3], 'little') & 0xffff
    p_a      = int.from_bytes(params.argument_bytes[3:4], 'little') & 0xff
    p_b      = int.from_bytes(params.argument_bytes[4:5], 'little') & 0xff
    p_expect = int.from_bytes(params.argument_bytes[5:7], 'little') & 0xffff
    p_loop   = int.from_bytes(params.argument_bytes[7:10], 'little') & 0xffffff
    #print(f'mode={p_mode:02x} bits={p_bits:04x} a={p_a:02x} b={p_b:02x} expect={p_expect:04x} loop={p_loop:06x}')

    # get the TT DemoBoard object from params passed in
    tt = params.tt 

    # Select a design, this isn't used but potentially could alter temperature
    # through power draw
    tt.clock_project_stop()

    tt.pins.safe_bidir()
    tt.mode = 1 # ttboard.mode.RPMode.ASIC_RP_CONTROL

    tt.rst_n(False)
    tt.clk(False)
    tt.ui_in.value = 0 # ui_in = 8'b0
    tt.uio_in.value = 0  # uio_in = 8'b0
    tt.uio_oe_pico = 0 # safe_bidir()
    time.sleep_ms(1)

    DESIGN_ID = 616
    tt.shuttle.reset_and_clock_mux(DESIGN_ID)
    time.sleep_ms(1)
    tt.clock_project_once()
    tt.clock_project_once()
    tt.uio_oe_pico = 0b11001001
    clock_on(tt)
    tt.rst_n(True)

    r = 0
    c = 0
    count = 0
    good_count = 0

    uio_in = 0
    maxloop = p_loop
    if p_mode == 0 and p_bits == 0 and p_a == 0 and p_b == 0 and p_loop == 0:
        maxloop = 1 # default (all data zero, do 1 iteration)
        p_bits = 0x08 # MUL/UNS=0 and REG=0x08
    #print(f'entrypoint INIT loop={maxloop}')

    # project should be synced by default
    clock_cycle(tt)
    clock_cycle(tt)

    while params.keep_running and maxloop > 0:
        #print(f'entrypoint LOOP loop={maxloop}')
        if maxloop > 0:
            maxloop -= 1

        b_set   = p_bits & 0xff
        b_reset = (~(p_bits >> 8)) & 0xff # inverted
        #uio_in = tt.uio_in.value
        uio_in |= b_set
        uio_in &= b_reset
        uio_in = addr_set(tt, uio_in, False) # bit0=0 A0
        #print(f'set={b_set:02x} reset={b_reset:02x} uio_in={uio_in:02x} ')

        tt.ui_in.value = p_a
        clock_off(tt)
        clock_on(tt)

        tt.ui_in.value = p_b
        uio_in = addr_set(tt, uio_in, True) # bit0=1 A1
        clock_off(tt)
        clock_on(tt)

        r_b = tt.uo_out.value
        c_b = tt.uio_out.value
        #print(f'r_b={r_b} c_b={c_b} uio_in={tt.uio_in.value}={uio_in:02x}')

        uio_in = addr_set(tt, uio_in, False) # bit0=0 A0

        r_a = tt.uo_out.value
        c_a = tt.uio_out.value
        #print(f'r_a={r_a} c_a={c_a} uio_in={tt.uio_in.value}={uio_in:02x}')

        r = (int(r_a) & 0xff) | ((int(r_b) << 8) & 0xff00)
        c = (int(c_a) & 0xff) | ((int(c_b) << 8) & 0xff00)

        count += 1
        if r == p_expect:
            good_count += 1
            m = 'PASS'
        else:
            m = 'FAIL'

        #print(f'{m}: r={r:04x} expect={p_expect:04x}')

        #print(f'ANSWER r={r:04x} c={c:04x} {good_count}/{count}')
        populate_response(response.result, count, r, c, good_count, 0)


    populate_response(response.result, count, r, c, good_count, 1)
    #print(f'entrypoint EXIT loop={maxloop}')
