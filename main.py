import mido
import keyboard
import time

mido.set_backend('mido.backends.rtmidi')

# load inputs and outputs and check if matching drivers exist
inputs = mido.get_input_names()
outputs = mido.get_output_names()

print("Found MIDI controller outputs ", *outputs, sep="/")

idx = int(input("Choose the index of the output to use: "))

# if i can't find it just get out atp.
if idx < len(outputs):
    # open virtual MIDI output (match name of your loopMIDI port)
    outport = mido.open_output(outputs[idx])

    cc_number = 14
    value = 64  # start in middle

    def send_cc(val):
        msg = mido.Message('control_change', control=cc_number, value=val)
        outport.send(msg)

    while True:
        changed = False

        if keyboard.is_pressed('z'):   # increase knob
            value = min(127, value + 1)
            changed = True

        if keyboard.is_pressed('x'):   # decrease knob
            value = max(0, value - 1)
            changed = True

        if changed:
            send_cc(value)
            print("CC value:", value)
            time.sleep(0.01)  # controls speed (smoothness)