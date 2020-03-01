import curses
from smbus import SMBus

addr = 9 # bus address
bus = SMBus(1) # indicates /dev/i2c-1

def StringtoBytes(val):
	retVal = []
	for c in val:
		retVal.append(ord(c))
	return retVal

# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord(' '):
            break
        elif char == curses.KEY_DOWN:
            data = int(0)
        elif char == curses.KEY_UP:
            data = int(30)
        screen.addstr(0, 0, str(data))
        bus.write_i2c_block_data(addr, 0x00, [data]*8)
finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
