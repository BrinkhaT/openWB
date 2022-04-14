#!/usr/bin/python3
import os
import sys, traceback
import time
from typing import List
try: # make script callable from command line and LRS
    from bezug_rct2 import rct_lib
except:
    import rct_lib

# Entry point with parameter check
def main(argv: List[str]):
    start_time =  time.time()
    rct = rct_lib.RCT(argv)

    if rct.connect_to_server() == True:
        try:
            MyTab = []
            pv1watt  = rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].p_dc')
            pv2watt  = rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].p_dc')
            pv3watt  = rct.add_by_name(MyTab, 'io_board.s0_external_power')
            dA       = rct.add_by_name(MyTab, 'energy.e_dc_day[0]')
            dB       = rct.add_by_name(MyTab, 'energy.e_dc_day[1]')
            dE       = rct.add_by_name(MyTab, 'energy.e_ext_day')
            mA       = rct.add_by_name(MyTab, 'energy.e_dc_month[0]')
            mB       = rct.add_by_name(MyTab, 'energy.e_dc_month[1]')
            mE       = rct.add_by_name(MyTab, 'energy.e_ext_month')
            yA       = rct.add_by_name(MyTab, 'energy.e_dc_year[0]')
            yB       = rct.add_by_name(MyTab, 'energy.e_dc_year[1]')
            yE       = rct.add_by_name(MyTab, 'energy.e_ext_year')
            pv1total = rct.add_by_name(MyTab, 'energy.e_dc_total[0]')
            pv2total = rct.add_by_name(MyTab, 'energy.e_dc_total[1]')
            pv3total = rct.add_by_name(MyTab, 'energy.e_ext_total')

            # read all parameters
            response = rct.read(MyTab)
            rct.close()

            # postprocess values
            pv1watt  = int(pv1watt.value)
            pv2watt  = int(pv2watt.value)
            pv3watt  = int(pv3watt.value)
            dA       = int(dA.value)
            dB       = int(dB.value)
            dE       = int(dE.value)
            mA       = int(mA.value)
            mB       = int(mB.value)
            mE       = int(mE.value)
            yA       = int(yA.value)
            yB       = int(yB.value)
            yE       = int(yE.value)
            pv1total = int(pv1total.value)
            pv2total = int(pv2total.value)
            pv3total = int(pv3total.value)

            # aktuell
            rct.write_ramdisk('pv1wattString1', int(pv1watt), 'pv1watt')
            rct.write_ramdisk('pv1wattString2', int(pv2watt), 'pv2watt')
            pvwatt = ((pv1watt+pv2watt+pv3watt) * -1)
            rct.write_ramdisk('pvwatt', int(pvwatt), 'negative Summe von pv1watt + pv2watt + pv3watt')

            # daily
            daily_pvkwhk = (dA + dB + dE) / 1000.0   # -> KW
            rct.write_ramdisk('daily_pvkwhk', daily_pvkwhk, 'daily_pvkwhk')

            # monthly
            monthly_pvkwhk = (mA + mB + mE) / 1000.0   # -> KW
            rct.write_ramdisk('monthly_pvkwhk', monthly_pvkwhk, 'monthly_pvkwhk')

            # yearly
            yearly_pvkwhk = (yA + yB + yE) / 1000.0   # -> KW
            rct.write_ramdisk('yearly_pvkwhk', yearly_pvkwhk, 'yearly_pvkwhk')

            # total
            pvkwh = (pv1total + pv2total + pv3total)
            rct.write_ramdisk('pvkwh', pvkwh, 'Summe von pv1total pv1total pv1total')

            # debug output of processing time and all response elements
            rct.dbglog("Overall processing time: {:.3f} seconds".format(time.time() - start_time))
            rct.dbglog(response.format_list())
        except:
            print("-"*100)
            traceback.print_exc(file=sys.stdout)
            rct.close()

    rct = None


if __name__ == "__main__":
    main(sys.argv[1:])