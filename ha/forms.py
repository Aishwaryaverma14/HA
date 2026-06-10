from django import forms
from .models import HAConfig
import socket
import os

def get_network_interfaces():
    interfaces = []
    try:
        interfaces = [name for _, name in socket.if_nameindex()]
    except (AttributeError, OSError):
        pass

    if not interfaces:
        if os.path.exists('/sys/class/net'):
            try:
                interfaces = os.listdir('/sys/class/net')
            except OSError:
                pass

    if not interfaces:
        interfaces = ['eth0', 'eth1', 'wlan0', 'lo']
    return interfaces

class HAConfigForm(forms.ModelForm):
    class Meta:
        model = HAConfig
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        interfaces = get_network_interfaces()
        choices = [(name, name) for name in interfaces]
        
        current_value = self.instance.interface if self.instance and hasattr(self.instance, 'interface') else None
        if current_value and current_value not in interfaces:
            choices.insert(0, (current_value, current_value))
            
        self.fields['interface'].widget = forms.Select(choices=choices)

        for field_name, field in self.fields.items():
            if field_name == 'interface':
                field.widget.attrs.update({
                    'class': 'form-select shadow-sm border-secondary-subtle focus-ring focus-ring-primary',
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control shadow-sm border-secondary-subtle focus-ring focus-ring-primary',
                    'placeholder': f'Enter {field.label.lower()}'
                })


