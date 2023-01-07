import consul


def post_consul_config():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    c = consul.Consul(host=os.getenv('CONSUL_HOST'))
    c.kv.put('KEYCLOAK_API', os.getenv('KEYCLOAK_API'))
    c.kv.put('KEYCLOAK_REALM', os.getenv('KEYCLOAK_REALM'))
    c.kv.put('KEYCLOAK_CLIENT_ID', os.getenv('KEYCLOAK_CLIENT_ID'))
    c.kv.put('KEYCLOAK_ADMIN_USER', os.getenv('KEYCLOAK_ADMIN_USER'))
    c.kv.put('KEYCLOAK_ADMIN_SECRET', os.getenv('KEYCLOAK_ADMIN_SECRET'))
    c.kv.put('KEYCLOAK_REDIRECT_URL', os.getenv('KEYCLOAK_REDIRECT_URL'))
    c.kv.put('KEYCLOAK_SSL_VERIFY', os.getenv('KEYCLOAK_SSL_VERIFY'))
    c.kv.put('KEYCLOAK_CLIENT_SECRET_KEY', os.getenv('KEYCLOAK_CLIENT_SECRET_KEY'))
