import os

def generate_keepalived_config(config):
    content = f"""# =========================================================================
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
}}
"""

    filepath = "/tmp/keepalived.conf"
    # Ensure directory exists (e.g., C:\tmp on Windows, /tmp on Linux)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        f.write(content)

