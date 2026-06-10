from django.shortcuts import render, redirect
from django.contrib import messages
from .keepalived import generate_keepalived_config
from .forms import HAConfigForm
from .models import HAConfig

def get_keepalived_config_text(config):
    if not config:
        return ""
    return f"""# =========================================================================
# KEEPALIVED MASTER CONFIGURATION (Save on Master Node)
# =========================================================================
vrrp_instance VI_1 {{
    state MASTER
    interface {config.interface}
    virtual_router_id 51
    priority {config.master_priority}
    advert_int 1

    authentication {{
        auth_type PASS
        auth_pass 1234
    }}

    unicast_src_ip {config.master_ip}
    unicast_peers {{
        {config.slave_ip}
    }}

    virtual_ipaddress {{
        {config.virtual_ip}
    }}
}}

# =========================================================================
# KEEPALIVED SLAVE CONFIGURATION (Save on Slave Node)
# =========================================================================
vrrp_instance VI_1 {{
    state BACKUP
    interface {config.interface}
    virtual_router_id 51
    priority {config.slave_priority}
    advert_int 1

    authentication {{
        auth_type PASS
        auth_pass 1234
    }}

    unicast_src_ip {config.slave_ip}
    unicast_peers {{
        {config.master_ip}
    }}

    virtual_ipaddress {{
        {config.virtual_ip}
    }}
}}"""


import os

def ha_config(request):
    config_instance = HAConfig.objects.last()
    config_filepath = os.path.abspath("/tmp/keepalived.conf")
    
    if request.method == 'POST':
        form = HAConfigForm(request.POST, instance=config_instance)
        if form.is_valid():
            obj = form.save()
            generate_keepalived_config(obj)
            messages.success(request, f'Keepalived HA Configuration saved and generated successfully at: {config_filepath}')
            return redirect('ha_config')
    else:
        form = HAConfigForm(instance=config_instance)
        
    config_text = get_keepalived_config_text(config_instance)
    
    return render(request, 'ha/config.html', {
        'form': form,
        'config': config_instance,
        'config_text': config_text,
        'config_filepath': config_filepath
    })

