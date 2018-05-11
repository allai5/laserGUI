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
           
        self.titlelbl = gui.Label(self.name, width = '80%', height = '50%')
        self.titlelbl.style['font-size'] = '40px'
        self.titlelbl.style['text-align'] = 'center'

        self.onlbl = gui.Label('Laser is off.', style={'text-align': 'center'})
        self.bt = gui.Button('OFF', width=100, height=30) #on/off button
        self.bt.style['margin'] = 'auto 10px'
        self.bt.set_on_click_listener(self.on_button_pressed)

        self.wavlbl = gui.Label('Select a wavelength between 1529 nm and 1570 nm.', width = '100%', margin ='10px auto', style={'text-align': 'center'})
        self.wavlbl.style['text-align'] = 'center'
        self.inputWav = gui.TextInput(width=200, height=20)   
        self.inputWav.set_on_change_listener(self.setWavGUI)     

        self.applyWav = gui.Button('APPLY WAV', width=100, height=30)
        self.applyWav.set_on_click_listener(self.on_applyWav_pressed)

        self.powlbl = gui.Label('Select a power between 0 db and 15 db.', width = '100%', margin ='10px auto')
        self.powlbl.style['text-align'] = 'center'
        self.inputPow = gui.TextInput(width=200, height=20)
        self.inputPow.set_on_change_listener(self.setPowGUI)

        self.applyPow = gui.Button('APPLY POW', width=100, height=30)
        self.applyPow.set_on_click_listener(self.on_applyPow_pressed)

        self.update = gui.Button('Update Laser', width=120, height=30)
        self.update.set_on_click_listener(self.updateFields)

        wid_title = gui.VBox(width=800, height=300, layout_orientation = gui.Widget.LAYOUT_VERTICAL, margin='0px auto')
        wid_root = gui.VBox(width=800, height=400, layout_orientation = gui.Widget.LAYOUT_VERTICAL, margin='0px auto') #overall widgets
        wid_status = gui.HBox(width=800, height=300, layout_orientation = gui.Widget.LAYOUT_HORIZONTAL, margin='0px auto') #overall widgets
        wid_apply = gui.HBox(width=800, height=300, layout_orientation = gui.Widget.LAYOUT_HORIZONTAL, margin='0px auto') #overall widgets
        wid_label = gui.HBox(width=800, height=200, layout_orientation = gui.Widget.LAYOUT_HORIZONTAL, margin='0px auto') #overall widgets
        wid_input = gui.HBox(width=800, height=200, layout_orientation = gui.Widget.LAYOUT_VERTICAL, margin='0px auto') #overall widgets

        wid_title.append(self.titlelbl)
        wid_status.append(self.onlbl)
        wid_apply.append(self.bt) #on/off container
        wid_apply.append(self.update)
        wid_label.append(self.wavlbl) #label container
        wid_label.append(self.powlbl)
        wid_input.append(self.inputWav)
        wid_input.append(self.applyWav) #set wavelength and power container
        wid_input.append(self.inputPow)
        wid_input.append(self.applyPow)

        wid_root.append(wid_title)
        wid_root.append(wid_status)
        wid_root.append(wid_apply) 
        wid_root.append(wid_label)
        wid_root.append(wid_input)

        return wid_root
        
        
    '''def updateTable(self, content, fill_title = False):
        self.table[0][0] = 'Laser Property'
        self.table[0][1] = 'Value'
        self.table[1][0] = 'Wavelength'
        self.table[1][1] = self.wavelength
        self.table[2][0] = 'Power'
        self.table[2][0] = self.pow'''

    def updateFields(self, widget):
        #print(str(self.laser.GetWav()))
        #print(str(self.laser.GetPower()))
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
    
    def setPowGUI(self, widget, value):
        self.pow = float(widget.get_text())

    def validateWav(self):
        if (self.wavelength < 1528 or self.wavelength > 1570):
            self.wavelength = 1550.0000
    def validatePow(self):
        if (self.pow < 0 or self.pow > 15):
            self.pow = 10.0000
    def on_applyWav_pressed(self, widget):
        self.setWavGUI
        self.validateWav()
        self.open_confirmation(widget)
    
    def on_applyPow_pressed(self, widget):
        self.setPowGUI
        self.validatePow()
        self.open_confirmation(widget)

    def open_confirmation(self, widget):
        self.dialog = gui.GenericDialog(title='Confirmation Page', message= 'Are you sure you want to set laser to ' + str(self.wavelength) + ' nm wavelength and ' + str(self.pow) + ' db power?')
        self.dialog.set_size(350,150)   
        #self.set_root_widget(self.dialog)
        self.dialog.set_on_confirm_dialog_listener(self.confirm_dialog(widget))
        #self.dialog.set_on_cancel_dialog_listener(self.maidialogn())
        
        self.dialog.show(self)
        #print(self.wavelength)
   
    def confirm_dialog(self, widget):
        self.laser.SetWav(self.wavelength)
        self.laser.SetPower(self.pow)

if __name__ == "__main__":
    mylaser = ECL_Client()
    start(TunableLaserGUI, debug=True)
