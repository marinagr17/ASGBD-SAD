from pymemcache.client import base

# Conexión al servidor Memcached
client = base.Client(('192.168.122.14', 11211))

# Guardar un valor
client.set('usuario:1', 'Ana')

# Leerlo
valor = client.get('usuario:1')
print(valor)

# Borrarlo
client.delete('usuario:1')
