import remi.gui as gui
from remi import start, App
from TunableLaserInterface import ECL_Client


class TunableLaserGUI(App):
    def __init__(self, *args):
        super(TunableLaserGUI, self).__init__(*args)
    def main(self, name='world'):
        self.laser = mylaser
        self.wavelength = 1550
        self.pow = 10
        self.state = 0
        self.name = "Laser 1"
        
        title = gui.VBox(width=800, height=300, layout_orientation = gui.Widget.LAYOUT_VERTICAL, margin='0px auto')
        wid3 = gui.VBox(width=800, height=400, layout_orientation = gui.Widget.LAYOUT_VERTICAL, margin='0px auto') #overall widgets
        wid3b = gui.HBox(width=800, height=300, layout_orientation = gui.Widget.LAYOUT_HORIZONTAL, margin='0px auto') #overall widgets
        wid2 = gui.HBox(width=800, height=300, layout_orientation = gui.Widget.LAYOUT_HORIZONTAL, margin='0px auto') #overall widgets
        wid1 = gui.HBox(width=800, height=200, layout_orientation = gui.Widget.LAYOUT_HORIZONTAL, margin='0px auto') #overall widgets
        wid = gui.HBox(width=800, height=200, layout_orientation = gui.Widget.LAYOUT_VERTICAL, margin='0px auto') #overall widgets
        
    
        titlelbl = gui.Label(self.name, width = '80%', height = '50%')
        titlelbl.style['font-size'] = '40px'
        titlelbl.style['text-align'] = 'center'

        self.onlbl = gui.Label('Laser is off.', style={'text-align': 'center'})
        bt = gui.Button('OFF', width=100, height=30) #on/off button
        bt.style['margin'] = 'auto 10px'
        bt.set_on_click_listener(self.on_button_pressed)
        #bt.style['margin'] = 'auto 50px'

        wavlbl = gui.Label('Select a wavelength between 1529 nm and 1570 nm.', width = '100%', margin ='10px auto', style={'text-align': 'center'})
        wavlbl.style['text-align'] = 'center'
        self.inputWav = gui.TextInput(width=200, height=20)   
        self.inputWav.set_on_change_listener(self.setWavGUI)     

        applyWav = gui.Button('APPLY WAV', width=100, height=30)
        applyWav.set_on_click_listener(self.on_applyWav_pressed)

        powlbl = gui.Label('Select a power between 0 db and 15 db.', width = '100%', margin ='10px auto')
        powlbl.style['text-align'] = 'center'
        self.inputPow = gui.TextInput(width=200, height=20)
        self.inputPow.set_on_change_listener(self.setPowGUI)

        applyPow = gui.Button('APPLY POW', width=100, height=30)
        applyPow.set_on_click_listener(self.on_applyPow_pressed)

        '''self.table = gui.Table.new_from_list([('Laser Property', 'Value'),
                                   ('Wavelength', self.wavelength),
                                   ('Power', self.pow)], width=200, height=100, margin='0px')'''
        update = gui.Button('Update Laser', width=120, height=30)
        update.set_on_click_listener(self.updateFields)

        title.append(titlelbl)
        wid3b.append(self.onlbl)
        wid2.append(bt) #on/off container
        wid2.append(update)
        wid1.append(wavlbl) #label container
        wid1.append(powlbl)
        wid.append(self.inputWav)
        wid.append(applyWav) #set wavelength and power container
        wid.append(self.inputPow)
        wid.append(applyPow)

        wid3.append(title)
        wid3.append(wid3b)
        wid3.append(wid2) #root container
        wid3.append(wid1)
        wid3.append(wid)

        return wid3
        
        
    '''def updateTable(self, content, fill_title = False):
        self.table[0][0] = 'Laser Property'
        self.table[0][1] = 'Value'
        self.table[1][0] = 'Wavelength'
        self.table[1][1] = self.wavelength
        self.table[2][0] = 'Power'
        self.table[2][0] = self.pow'''

    def updateFields(self, widget):
        print(str(self.laser.GetWav()))
        print(str(self.laser.GetPower()))
        self.inputWav.set_text("{0:.4f}".format((self.laser.GetWav())))
        self.inputPow.set_text("{0:.4f}".format((self.laser.GetPower())))
        
    def on_button_pressed(self, widget):
        if(self.state == 0):
            self.state = 1
            widget.set_text('ON')
            self.onlbl.set_text("Laser is on.")
            self.laser.On()
        else:
            self.state = 0
            widget.set_text('OFF')
            self.onlbl.set_text("Laser is off.")
            self.laser.Off()            
    
    def setWavGUI(self, widget, value):
        self.wavelength = float(widget.get_text())
        self.validateWav()
    
    def setPowGUI(self, widget, value):
        self.pow = float(widget.get_text())
        self.validatePow()

    def validateWav(self):
        if (self.wavelength < 1528 or self.wavelength > 1570):
            self.wavelength = 1550.0000
        else:
            print('')
    def validatePow(self):
        if (self.pow < 0 or self.pow > 15):
            self.pow = 10.0000

    def on_applyWav_pressed(self, widget):
        #self.open_confirmation(widget)
        self.laser.SetWav(self.wavelength)
    
    def on_applyPow_pressed(self, widget):
        #self.open_confirmation(widget)
        self.laser.SetPower(self.pow)

    def open_confirmation(self, widget):
        self.dialog = gui.GenericDialog(title='Confirmation Page', message='Are you sure?')
        self.dialog.set_size(300,300)   
        self.dialog.set_on_confirm_dialog_listener(self.dialog.confirm_dialog)
        self.dialog.set_on_cancel_dialog_listener(self.main())
        #self.set_root_widget(self.dialog)
        self.dialog.show(self)
        print(self.wavelength)
   
if __name__ == "__main__":
    mylaser = ECL_Client()
    start(TunableLaserGUI, debug=True)