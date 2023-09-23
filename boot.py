import board

from kmk.bootcfg import bootcfg

bootcfg(
    sense=board.GP6,  # column
    source=board.GP16, # row
    midi=False,
    mouse=False,
    storage=False,
    usb_id=('1UPKeyboards', 'PI50'),
)

# SCL=board.GP11
# SDA=board.GP10
 # SCL=board.SCL
 # SDA=board.SDA