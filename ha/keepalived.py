def generate_keepalived_config(config):
    content = f"""
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

    virtual_ipaddress {{
        {config.virtual_ip}
    }}
}}
"""

    with open("/tmp/keepalived.conf", "w") as f:
        f.write(content)
