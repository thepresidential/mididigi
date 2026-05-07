import mido
import keyboard
import time

from mido.backends.rtmidi import Output

mido.set_backend('mido.backends.rtmidi')

control_binds = ["filter", "low", "mid", "high"]

control_ccs = [[11, 12], [13, 14], [15, 16], [17, 18]]

class InputManager:
    def __init__(self, outport : Output, verbose = False):
        self.outport = outport
        self.verbose = verbose

    def send_cc(self, cc_number, val):
        msg = mido.Message('control_change', control=cc_number, value=val)
        self.outport.send(msg)

        if self.verbose:
            print("CC value:", val)

# load inputs and outputs and check if matching drivers exist
inputs = mido.get_input_names()
outputs = mido.get_output_names()

print("Found MIDI controller outputs ", *outputs, sep="/")

idx = int(input("Choose the index of the output to use: "))

# if i can't find it just get out atp.
if idx < len(outputs):
    print(f"Initializing MIDI outport {outputs[idx]}")

    # open virtual MIDI output (match name of your loopMIDI port)
    outport = mido.open_output(outputs[idx])

    val1 = 64
    val2 = 64

    min_val = 0
    max_val = 127

    current_control = 1 # default to low [bass swiiiitch]
    current_control_cc_pair = control_ccs[current_control]

    print(f"Initializing InputManager with initial values for CC14 and 15 as {val1}")
    input_manager = InputManager(outport)
    input_manager.send_cc(14, val1)
    input_manager.send_cc(15, val2)

    print("Starting main loop.")

    verbose = True if input("Verbose? (Y/n): ").lower() == "y" else False

    print(f"Currently controlling knobs for {current_control} using pairs {current_control_cc_pair}")

    while True:
        changed = False
        changed_cc = False

        if keyboard.is_pressed('1'): # filter
            current_control = 0
            changed_cc = True
        elif keyboard.is_pressed('2'): # lows
            current_control = 1
            changed_cc = True
        elif keyboard.is_pressed('3'): # mids
            current_control = 2
            changed_cc = True
        elif keyboard.is_pressed('4'): # highs
            current_control = 3
            changed_cc = True

        if changed_cc:
            current_control_cc_pair = control_ccs[current_control]
            print(f"Currently controlling knobs for {current_control} using pairs {current_control_cc_pair}")

        # CC Deck 1, CC Deck 2
        CCD1, CCD2 = current_control_cc_pair[0], current_control_cc_pair[1]

        # floor controls - switch the max and min vals to 32 and 96
        # this is so you don't overshoot while trying to bass switch.
        if keyboard.is_pressed('c'):
            min_val = 32 if min_val == 0 else 0
            max_val = 96 if max_val == 127 else 127

        # knob 1
        if keyboard.is_pressed('x'):
            val1 = min(max_val, val1 + 1)
            input_manager.send_cc(CCD1, val1)
            changed = True

        if keyboard.is_pressed('z'):
            val1 = max(min_val, val1 - 1)
            input_manager.send_cc(CCD1, val1)
            changed = True

        # knob 2 (runs at same time!)
        if keyboard.is_pressed('m'):
            val2 = min(max_val, val2 + 1)
            input_manager.send_cc(CCD2, val2)
            changed = True

        if keyboard.is_pressed('n'):
            val2 = max(min_val, val2 - 1)
            input_manager.send_cc(CCD2, val2)
            changed = True

        if changed:
            time.sleep(0.01)