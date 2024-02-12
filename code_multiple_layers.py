print("Hello World!")
print("Starting")

import board
################## FOR DISPLAY IMPORT ##################
import displayio
import adafruit_displayio_ssd1306
import busio
import terminalio
from adafruit_display_text import label
import time
import gc
################ FOR DISPLAY IMPORT END ################


from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
# from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData

keyboard = KMKKeyboard()


################### QMK REF #############################
# https://github.com/qmk/qmk_firmware/blob/master/keyboards/1upkeyboards/pi50/info.json
# https://github.com/qmk/qmk_firmware/blob/master/keyboards/1upkeyboards/pi50/keymaps/default/keymap.c
# "matrix_pins": {
#         "rows": ["GP20", "GP15", "GP19", "GP14", "GP18", "GP13", "GP17", "GP12", "GP16", "GP21"],
#         "cols": ["GP1",  "GP2",  "GP3",  "GP4",  "GP5",  "GP6",  "GP9"]
#     },

################### LAYERS #############################
keyboard.extensions.append(Layers())
keyboard.modules.append(Layers())

################### ENCODER #############################
ENCODER = EncoderHandler()
keyboard.extensions.append(MediaKeys())
ENCODER.pins = ((board.GP8,board.GP7, None),) # SUPPORT MULT & NONE IS ON THE CLICK POSITION
ENCODER.map = [
    ((KC.VOLD, KC.VOLU),),
    # ADD MORE ENCODER LAYERS 
]

keyboard.extensions.append(ENCODER)
################### RGB ################################
rgb = RGB(pixel_pin=board.GP0, num_pixels=59)#rgb_order=(1,0,2) not required
keyboard.extensions.append(rgb)


################### KEYMAP & LAYERS #############################
#TODO: LOOK AT http://kmkfw.io/docs/scanners TO FIX THIS
keyboard.col_pins = (board.GP1,board.GP2,board.GP3,board.GP4,board.GP5,board.GP6,board.GP9)
keyboard.row_pins = (board.GP20,board.GP15,board.GP19,board.GP14,board.GP18,board.GP13,board.GP17,board.GP12,board.GP16,board.GP21)
keyboard.diode_orientation = DiodeOrientation.COL2ROW


#LAYER HELPERS http://kmkfw.io/docs/layers
ENC_CLK = KC.TG(3)# ENCODER CLICK / TOGGLE LAYER
TRN = KC.TRANSPARENT;
RAISE = KC.MO(1) #MOMENTARY SWITCH LAYER
LOWER = KC.MO(2)
SLEEP = KC.RGB_TOG
CAPSLOCK = KC.CAPSLOCK
RAISE42_1 = KC.MO(4)
TAB_MISC = KC.LT(5, KC.TAB, prefer_hold=True, tap_interrupted=False, tap_time=250)

MYLAYERS  =  [
    [  #LAYER 0 : BASE                                                                                                                
         [ KC.ESCAPE,  KC.N1,    KC.N2,    KC.N3,    KC.N4,   KC.N5,    KC.N6,    KC.N7,   KC.N8,   KC.N9,  KC.N0,    KC.BSPACE ],
         [ KC.TAB,     KC.Q,     KC.W,     KC.E,     KC.R,    KC.T,     KC.Y,     KC.U,    KC.I,    KC.O,   KC.P,     KC.BSLASH ],
         [ CAPSLOCK ,  KC.A,     KC.S,     KC.D,     KC.F,    KC.G,     KC.H,     KC.J,    KC.K,    KC.L,   KC.SCLN,  KC.ENTER  ],
         [ KC.LSHIFT,  KC.Z,     KC.X,     KC.C,     KC.V,    KC.B,     KC.N,     KC.M,    KC.COMMA,KC.DOT, KC.SLASH, KC.RSHIFT ],
         [ KC.LCTRL,   KC.LALT,  KC.LGUI,  SLEEP,   LOWER,    KC.SPACE, KC.SPACE, RAISE , KC.LEFT, KC.DOWN,KC.UP,    KC.RIGHT ],
    ],
    [  #LAYER 1 : FUNCTIONS
         [ KC.F1,KC.F2,KC.F3,KC.F4,KC.F5,KC.F6,KC.F7,KC.F8,KC.F9,KC.F10,KC.F11,KC.F12 ],
         [ KC.GRAVE, TRN, TRN, TRN, KC.RESET, TRN, TRN, TRN, KC.PAUSE, KC.N1, KC.N2, KC.SCROLLLOCK ],
         [ KC.RGB_HUD,  KC.RGB_HUI,  KC.RGB_AND, KC.RGB_ANI, TRN, TRN, TRN, TRN, KC.MINUS , KC.EQUAL,  KC.QUOTE, TRN ],
         [ KC.RGB_SAD,  KC.RGB_SAI,  TRN,  KC.RGB_MODE_PLAIN, KC.RGB_MODE_KNIGHT, TRN, TRN, TRN,  KC.LBRACKET, KC.RBRACKET, TRN, KC.RSHIFT ],
         [ KC.RGB_VAD,  KC.RGB_VAI,  TRN,  KC.RGB_MODE_BREATHE_RAINBOW, KC.RGB_MODE_PLAIN, TRN, TRN, TRN, TRN, TRN, TRN, TRN],
    ],
     [  #LAYER 2 : NUMBERS                                                                                                                
         [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.NUMLOCK, KC.KP_EQUAL,  KC.KP_SLASH,  KC.KP_ASTERISK],
         [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_7,       KC.KP_8,      KC.KP_9,  KC.KP_MINUS ],
         [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_4,       KC.KP_5,      KC.KP_6,  KC.KP_PLUS ],
         [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_1,       KC.KP_2,      KC.KP_3,  KC.KP_ENTER],
         [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_0,   KC.NO,  KC.KP_DOT,  KC.NO ],
    ],
    # ONLY 42 Keys (CORN, PIANTOR):
    [  #LAYER 3 AKA 0: BASE                                                                                                                
         [ KC.ESCAPE,  SLEEP,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,    KC.NO,     KC.NO,  KC.NO,    KC.NO ],
         [ TAB_MISC,   KC.Q,     KC.W,     KC.E,     KC.R,     KC.T,     KC.Y,     KC.U,     KC.I,      KC.O,   KC.P,     KC.BSPACE ],
         [ KC.LSHIFT,  KC.A,     KC.S,     KC.D,     KC.F,     KC.G,     KC.H,     KC.J,     KC.K,      KC.L,   KC.SCLN,  KC.QUOTE ],
         [ KC.LCTRL,   KC.Z,     KC.X,     KC.C,     KC.V,     KC.B,     KC.N,     KC.M,     KC.COMMA,  KC.DOT, KC.SLASH, KC.RSHIFT ],
         [ KC.NO,      KC.NO,    KC.NO,    KC.LGUI,  RAISE42_1,KC.ENTER, KC.SPACE, RAISE42_1,KC.ESCAPE, KC.NO,  KC.NO,    KC.NO ],
    ],
    [  #LAYER 4 AKA 1: CHARACTERS
         [ KC.ESCAPE,  SLEEP,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.NO,     KC.NO,   KC.NO,    KC.NO ],
         [ TAB_MISC,   KC.EXLM,  KC.AT,    KC.HASH,  KC.DLR,  KC.PERC,  KC.CIRC,  KC.AMPR, KC.ASTR,   KC.LPRN, KC.RPRN,  KC.BSLS ],
         [ KC.LSHIFT,  KC.N5,    KC.N4,    KC.N3,    KC.N2,   KC.N1,    KC.PPLS,  KC.EQL,  KC.GRV,    KC.LCBR, KC.RCBR,  KC.PIPE ],
         [ KC.LCTRL,   KC.N9,    KC.N8,    KC.N7,    KC.N6,   KC.N0,    KC.PMNS,  KC.UNDS, KC.TILD,   KC.LBRC, KC.RBRC,  KC.LALT ],
         [ KC.NO,      KC.NO,    KC.NO,    KC.LGUI,  TRN,     KC.ENTER, KC.SPACE, TRN,     KC.ESCAPE, KC.NO,   KC.NO,    KC.NO ],

    ],
    [  #LAYER 5  AKA 2: MISCELLANEOUS                                                                                                             
         [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.NO,  KC.NO, KC.NO,   KC.NO ],
         [ TRN,    KC.F1,    KC.F2,    KC.F3,    KC.F4,   KC.F5,    KC.F6,    KC.F7,   KC.F8,  KC.F9, KC.F10,  KC.F11],
         [ TRN,    KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.LEFT, KC.DOWN,KC.UP, KC.RIGHT,KC.F12],
         [ TRN,    KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.NO,  KC.NO, KC.NO,   KC.NO ],
         [ KC.NO,  KC.NO,    KC.NO,    TRN,      KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.NO,  KC.NO, KC.NO,   KC.NO ],
    ],
]


def permanenSwitchDefaultLayer (LYS, newDefault):
    LYS[newDefault],LYS[0] = LYS[0],LYS[newDefault]
    
#THIS IS ONLY TO BUILD THE KEYMAP SINCE THE COLS ARE OFF LOOK AT THE TODO
def buildKeymap (LYS):
    permanenSwitchDefaultLayer(LYS,3) #Only switch the default layer
    km = []
    for L in LYS:
        km.append([   #KC.NO ARE IGNORE. THE COLUMNS ARE OFF BUT NEED ALL 7 COL PINS AND 10 ROWS !
                L[0][0], L[0][2], L[0][4],  L[0][6], L[0][8],   L[0][10],   ENC_CLK,  L[0][1], L[0][3], L[0][5], L[0][7], L[0][9], L[0][11], KC.NO,
                L[1][0], L[1][2], L[1][4],  L[1][6], L[1][8],   L[1][10],   KC.NO,    L[1][1], L[1][3], L[1][5], L[1][7], L[1][9], L[1][11], KC.NO,
                L[2][0], L[2][2], L[2][4],  L[2][6], L[2][8],   L[2][10],   KC.NO,    L[2][1], L[2][3], L[2][5], L[2][7], L[2][9], L[2][11], KC.NO,
                L[3][0], L[3][2], L[3][4],  L[3][6], L[3][8],   L[3][10],   KC.NO,    L[3][1], L[3][3], L[3][5], L[3][7], L[3][9], L[3][11], KC.NO,
                L[4][0], L[4][2], L[4][4],  L[4][6], L[4][8],   L[4][10],   KC.NO,    L[4][1], L[4][3], L[4][5], L[4][7], L[4][9], L[4][11], KC.NO,
            ]) 
    return km





keyboard.keymap = buildKeymap(MYLAYERS)
#SHOULD BE:
# keyboard.keymap = [
#     [                                                                                                              KC.A,  #ENCODER CLICK    
#         KC.ESCAPE,  KC.N1,    KC.N2,    KC.N3,    KC.N4,   KC.N5,    KC.N6,    KC.N7,   KC.N8,   KC.N9,  KC.N0,    KC.BSPACE,
#         KC.TAB,     KC.Q,     KC.W,     KC.E,     KC.R,    KC.T,     KC.Y,     KC.U,    KC.I,    KC.O,   KC.P,     KC.BSLASH,
#         KC.CAPSLOCK,KC.A,     KC.S,     KC.D,     KC.F,    KC.G,     KC.H,     KC.J,    KC.K,    KC.L,   KC.SCLN,  KC.ENTER,
#         KC.LSHIFT,  KC.Z,     KC.X,     KC.C,     KC.V,    KC.B,     KC.N,     KC.M,    KC.COMMA,KC.DOT, KC.SLASH, KC.RSHIFT,
#         KC.A,       KC.A,     KC.A,     KC.A,     KC.A,    KC.SPACE, KC.SPACE, KC.A,    KC.LEFT, KC.DOWN,KC.UP,    KC.RIGHT,
#     ]
# ]

# MYLAYERS  =  [
#     [  #LAYER 0 : BASE                                                                                                                
#          [ KC.ESCAPE,  KC.N1,    KC.N2,    KC.N3,    KC.N4,   KC.N5,    KC.N6,    KC.N7,   KC.N8,   KC.N9,  KC.N0,    KC.BSPACE ],
#          [ KC.TAB,     KC.Q,     KC.W,     KC.E,     KC.R,    KC.T,     KC.Y,     KC.U,    KC.I,    KC.O,   KC.P,     KC.BSLASH ],
#          [ CAPSLOCK ,  KC.A,     KC.S,     KC.D,     KC.F,    KC.G,     KC.H,     KC.J,    KC.K,    KC.L,   KC.SCLN,  KC.ENTER  ],
#          [ KC.LSHIFT,  KC.Z,     KC.X,     KC.C,     KC.V,    KC.B,     KC.N,     KC.M,    KC.COMMA,KC.DOT, KC.SLASH, KC.RSHIFT ],
#          [ KC.LCTRL,   KC.LALT,  KC.LGUI,  SLEEP,   LOWER,    KC.SPACE, KC.SPACE, RAISE , KC.LEFT, KC.DOWN,KC.UP,    KC.RIGHT ],
#     ],
#     [  #LAYER 2 : FUNCTIONS
#          [ KC.F1,KC.F2,KC.F3,KC.F4,KC.F5,KC.F6,KC.F7,KC.F8,KC.F9,KC.F10,KC.F11,KC.F12 ],
#          [ KC.GRAVE, TRN, TRN, TRN, KC.RESET, TRN, TRN, TRN, KC.PAUSE, KC.N1, KC.N2, KC.SCROLLLOCK ],
#          [ KC.RGB_HUD,  KC.RGB_HUI,  KC.RGB_AND, KC.RGB_ANI, TRN, TRN, TRN, TRN, KC.MINUS , KC.EQUAL,  KC.QUOTE, TRN ],
#          [ KC.RGB_SAD,  KC.RGB_SAI,  TRN,  KC.RGB_MODE_PLAIN, KC.RGB_MODE_KNIGHT, TRN, TRN, TRN,  KC.LBRACKET, KC.RBRACKET, TRN, KC.RSHIFT ],
#          [ KC.RGB_VAD,  KC.RGB_VAI,  TRN,  KC.RGB_MODE_BREATHE_RAINBOW, KC.RGB_MODE_PLAIN, TRN, TRN, TRN, TRN, TRN, TRN, TRN],
#     ],
#      [  #LAYER 2 : NUMBERS                                                                                                                
#          [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.NUMLOCK, KC.KP_EQUAL,  KC.KP_SLASH,  KC.KP_ASTERISK],
#          [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_7,       KC.KP_8,      KC.KP_9,  KC.KP_MINUS ],
#          [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_4,       KC.KP_5,      KC.KP_6,  KC.KP_PLUS ],
#          [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_1,       KC.KP_2,      KC.KP_3,  KC.KP_ENTER],
#          [ KC.NO,  KC.NO,    KC.NO,    KC.NO,    KC.NO,   KC.NO,    KC.NO,    KC.NO,   KC.KP_0,   KC.NO,  KC.KP_DOT,  KC.NO ],
#     ],
#     # ADD HERE
# ]


################### DISPLAY #############################
##### Needs to be rewired for kmk/circuitpython usage https://github.com/KMKfw/kmk_firmware/blob/master/kmk/extensions/peg_oled_display.py
# oled_ext = Oled(
#     OledData(
#         corner_one={0:OledReactionType.STATIC,1:["layer"]},
#         corner_two={0:OledReactionType.LAYER,1:["1","2"]},
#         corner_three={0:OledReactionType.LAYER,1:["base","raise"]},
#         corner_four={0:OledReactionType.LAYER,1:["qwerty","nums"]}
#         ),
#         toDisplay=OledDisplayMode.TXT,flip=False,i2c = busio.I2C(scl=board.GP11, sda=board.GP10))

# oled_display_data=OledData(image={0:OledReactionType.LAYER,1:["1.bmp","2.bmp","1.bmp","2.bmp"]})

# oled_ext = Oled(oled_display_data,toDisplay=OledDisplayMode.IMG,flip=False)
# keyboard.extensions.append(oled_ext)

######### ALSO DISPLAY##############

displayio.release_displays()
i2c = busio.I2C(scl=board.GP11, sda=board.GP10)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32, rotation=180)
display.brightness = 8/10

def MyOledDisplay(layerNum,layerName,layerDesc):
    splash = displayio.Group()
    splash.append(label.Label(terminalio.FONT,text="LAYER",color=0xFFFFFF,x=0,y=10,))
    splash.append(label.Label(terminalio.FONT,text=layerNum,color=0xFFFFFF,x=64,y=10,))
    splash.append(label.Label(terminalio.FONT,text=layerName,color=0xFFFFFF,x=0,y=25,))
    splash.append(label.Label(terminalio.FONT,text=layerDesc,color=0xFFFFFF,x=64,y=25,))
    display.show(splash)
    gc.collect()

#INIT
def initOled():
    MyOledDisplay("1","BASE","QUERTY")
    #TODO: Add cool image on start
initOled()


def baseOledText(key, keyboard, *args):
    MyOledDisplay("1","BASE","QUERTY")

def raiseOledText(key, keyboard, *args):
    MyOledDisplay("2","RAISE","FUNCTIONS")
    
def lowerOledText(key, keyboard, *args):
    MyOledDisplay("0","LOWER","NUMBERS")

def onOffOledDisplay(key, keyboard, *args):
    if(display.is_awake):
        display.sleep()
    else:
        display.wake() 

RAISE.after_press_handler(raiseOledText)
RAISE.after_release_handler(baseOledText)
LOWER.after_press_handler(lowerOledText)
LOWER.after_release_handler(baseOledText)
SLEEP.after_release_handler(onOffOledDisplay)

######### ADDITIONAL ACTIONS ##############
# TODO: Capslock Led on when activated  http://kmkfw.io/docs/lock_status , http://kmkfw.io/docs/peg_rgb_matrix

if __name__ == '__main__':
    keyboard.go()
