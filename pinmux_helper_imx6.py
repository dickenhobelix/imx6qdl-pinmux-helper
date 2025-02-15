#!/usr/bin/env python3

import sys

"""
https://www.kernel.org/doc/Documentation/devicetree/bindings/pinctrl/fsl%2Cimx6q-pinctrl.txt
"""

PAD_CTL_HYS = 1 << 16
PAD_CTL_PUS_100K_DOWN = 0 << 14
PAD_CTL_PUS_47K_UP = 1 << 14
PAD_CTL_PUS_100K_UP = 2 << 14
PAD_CTL_PUS_22K_UP = 3 << 14
PAD_CTL_PUE = 1 << 13
PAD_CTL_PKE = 1 << 12
PAD_CTL_ODE = 1 << 11
PAD_CTL_SPEED_LOW = 1 << 6
PAD_CTL_SPEED_MED = 2 << 6
PAD_CTL_SPEED_HIGH = 3 << 6
PAD_CTL_DSE_DISABLE = 0 << 3
PAD_CTL_DSE_240ohm = 1 << 3
PAD_CTL_DSE_120ohm = 2 << 3
PAD_CTL_DSE_80ohm = 3 << 3
PAD_CTL_DSE_60ohm = 4 << 3
PAD_CTL_DSE_48ohm = 5 << 3
PAD_CTL_DSE_40ohm = 6 << 3
PAD_CTL_DSE_34ohm = 7 << 3
PAD_CTL_SRE_FAST = 1 << 0
PAD_CTL_SRE_SLOW = 0 << 0


class pin_drive_characteristics:
    def __init__(self, raw_value):
        raw_value = int(raw_value, base=0)

        if raw_value == 0x80000000:
            self.default = True
        else:
            self.default = False
            if 0 != (raw_value & (1 << 16)):
                self.hys = "True (Schmitt Trigger Input)"
            else:
                self.hys = "False (CMOS Input)"
            pus = (raw_value >> 14) & 3
            if pus == 0:
                self.pus = "100k down"
            elif pus == 1:
                self.pus = "47k up"
            elif pus == 2:
                self.pus = "100k up"
            elif pus == 3:
                self.pus = "22k up"
            else:
                self.pus = "undefined"
            if 0 != (raw_value & (1 << 13)):
                self.pue = "True (Pull Enabled)"
            else:
                self.pue = "False (Keeper Enabled)"
            if 0 != (raw_value & (1 << 12)):
                self.pke = "Pull/Keeper enabled"
            else:
                self.pke = "Pull/Keeper disabled"
            if 0 != (raw_value & (1 << 11)):
                self.ode = "True (Open Drain Enabled)"
            else:
                self.ode = "False (Open Drain Disabled)"
            speed = (raw_value >> 6) & 3
            if speed == 0:
                self.speed = "low (50 MHz)"
            elif speed == 1:
                self.speed = "medium (100, 150 MHz)"
            elif speed == 2:
                self.speed = "medium (100, 150 MHz)"
            elif speed == 3:
                self.speed = "high (100, 150, 200 MHz)"
            else:
                self.speed = "undefined"
            dse = (raw_value >> 3) & 7
            if dse == 0:
                self.dse = "disable"
            elif dse == 1:
                self.dse = "260 Ohm (150 Ohm @ 3.3V, 260 Ohm @ 1.8V)"
            elif dse == 2:
                self.dse = "130 Ohm (75 Ohm @ 3.3V, 130 Ohm @ 1.8V)"
            elif dse == 3:
                self.dse = "90 Ohm (50 Ohm @ 3.3V, 90 Ohm @ 1.8V)"
            elif dse == 4:
                self.dse = "60 Ohm (37 Ohm @ 3.3V, 60 Ohm @ 1.8V)"
            elif dse == 5:
                self.dse = "50 Ohm (30 Ohm @ 3.3V, 50 Ohm @ 1.8V)"
            elif dse == 6:
                self.dse = "40 Ohm (25 Ohm @ 3.3V, 40 Ohm @ 1.8V)"
            elif dse == 7:
                self.dse = "33 Ohm (20 Ohm @ 3.3V, 33 Ohm @ 1.8V)"
            else:
                self.dse = "undefined"
            if raw_value & (1 << 0):
                self.sre = "fast"
            else:
                self.sre = "slow"
            self.sion = (raw_value & (1 << 30)) != 0

    def __repr__(self) -> str:
        if self.default:
            return "Default settings (bit 31 set - do not change default pinmux)"
        else:
            ret = ""
            ret += f"HYS: {self.hys}\n"
            ret += f"PUS: {self.pus}\n"
            ret += f"PUE: {self.pue}\n"
            ret += f"PKE: {self.pke}\n"
            ret += f"ODE: {self.ode}\n"
            ret += f"Speed: {self.speed}\n"
            ret += f"DSE: {self.dse}\n"
            ret += f"SRE: {self.sre}\n"
            ret += f"SION: {self.sion}"
            return ret


class mux_description:
    def __init__(self, line):
        line = line.strip()
        try:
            [pad, function] = line.split()[0].split("MX6QDL_PAD_")[1].split("__")
            self.pad = pad
            self.function = function
        except Exception:
            self.pad = "<unknown>"
            self.function = "<unknown>"
        try:
            self.pindrive = pin_drive_characteristics(line.split()[-1])
        except Exception:
            self.pindrive = "<unknown>"

    def __repr__(self) -> str:
        return f"Pad {self.pad} is muxed to function {self.function}\n\nPin Drive Characteristics\n{self.pindrive}"


def generate_pinmux_option(options):
    opt = 0
    options = options.upper()

    if "HYS_SCHMITT" in options:
        opt |= PAD_CTL_HYS
    elif "HYS_CMOS" in options:
        pass
    else:
        raise Exception("no HYS value passed, use -h for valid options")

    if "PUS_100K_DOWN" in options:
        pass
    elif "PUS_47K_UP" in options:
        opt |= PAD_CTL_PUS_47K_UP
    elif "PUS_100K_UP" in options:
        opt |= PAD_CTL_PUS_100K_UP
    elif "PUS_22K_UP" in options:
        opt |= PAD_CTL_PUS_22K_UP
    else:
        raise Exception("no PUS value passed, use -h for valid options")

    if "PUE_KEEP" in options:
        pass
    elif "PUE_PULL" in options:
        opt |= PAD_CTL_PUE
    else:
        raise Exception("no PUE value passed, use -h for valid options")

    if "PKE_ENABLE" in options:
        opt |= PAD_CTL_PKE
    elif "PKE_DISABLE" in options:
        pass
    else:
        raise Exception("no PKE value passed, use -h for valid options")

    if "ODE_ENABLE" in options:
        opt |= PAD_CTL_ODE
    elif "ODE_DISABLE":
        pass
    else:
        raise Exception("no ODE value passed, use -h for valid options")

    if "LOW_SPEED" in options:
        opt |= PAD_CTL_SPEED_LOW
    elif "MED_SPEED" in options:
        opt |= PAD_CTL_SPEED_MED
    elif "HIGH_SPEED" in options:
        opt |= PAD_CTL_SPEED_HIGH
    else:
        raise Exception("no SPEED value passed, use -h for valid options")

    if "DSE_DISABLE" in options or "DSE_HIZ" in options:
        pass
    elif "DSE_240OHM" in options:
        opt |= PAD_CTL_DSE_240ohm
    elif "DSE_120OHM" in options:
        opt |= PAD_CTL_DSE_120ohm
    elif "DSE_80OHM" in options:
        opt |= PAD_CTL_DSE_80ohm
    elif "DSE_60OHM" in options:
        opt |= PAD_CTL_DSE_60ohm
    elif "DSE48OHM" in options:
        opt |= PAD_CTL_DSE_48ohm
    elif "DSE40OHM" in options:
        opt |= PAD_CTL_DSE_40ohm
    elif "DSE34OHM" in options:
        opt |= PAD_CTL_DSE_34ohm
    else:
        raise Exception("no DSE value passed, use -h for valid options")

    if "SRE_SLOW" in options:
        pass
    elif "SRE_FAST" in options:
        opt |= PAD_CTL_SRE_FAST

    if "SION" in options:
        opt |= 1 << 30

    return str(hex(opt))


if __name__ == "__main__":
    try:
        line = ""
        for arg in sys.argv[1:]:
            line += f"{arg} "
        if line.strip() == "":
            raise Exception("empty string")

        if line.startswith("-h"):
            print(f"{sys.argv[0]} - Pinmux helper for imx6")
            print("")
            print(f"Usage: {sys.argv[0]} [OPTION] [LINE, MUX VALUES]")
            print("")
            print(
                "without options: pass entire line from dts to get a cleartext description"
            )
            print("")
            print("Options: ")
            print("-g: generate mux hex value")
            print("    valid values, all must be passed")
            print("       HYS: HYS_SCHMITT or HYS_CMOS (hysteresis)")
            print(
                "       PUS: PUS_100K_DOWN, PUS_47K_UP, PUS_100K_UP or PUS_22K_UP (pullup/pulldown)"
            )
            print("       PUE: PUE_KEEP or PUE_PULL (select either Keeper or Pullup")
            print("       PKE: PKE_ENABLE or PKE_DISABLE (enable Keeper/Pullup)")
            print("       ODE: ODE_ENABLE or ODE_DISABLE (enable OpenDrain)")
            print("       SPEED: LOW_SPEED, MED_SPEED, HIGH_SPEED")
            print(
                "       DSE: DSE_DISABLE, DSE_240OHM, DSE_120OHM, DSE_80OHM, DSE_60OHM, DSE48OHM, DSE40OHM, DSE34OHM (Drive Strength)"
            )
            print("       SRE: SRE_SLOW, SRE_FAST")
            print("       SION: SION (or leave out, is implicitely off)")
            print("-h: display this help")
            exit(0)

        # generate config
        if line.startswith("-g"):
            try:
                print(generate_pinmux_option(line.split("-g")[1].strip()))
                exit(0)
            except Exception as ex:
                print(f"something went wrong: {ex}")
                exit(1)
    except Exception as ex:
        print(ex)
        line = "MX6QDL_PAD_CSI0_DAT6__ECSPI1_MISO       0x100b1"
        print(
            f"no pinmux entry line given as program argument, using example {line} instead"
        )

    try:
        print(mux_description(line))
    except Exception as ex:
        print(ex)
