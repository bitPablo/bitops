import yaml
import os
import subprocess
import envbash

# Load plugin config yml
bitops_dir=os.environ['BITOPS_DIR']
with open(bitops_dir+'/plugin.config.yml', 'r') as stream:
    try:
        plugins_yml = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)

# Loop through plugins and invoke each
plugins_dir = bitops_dir + '/scripts/plugins/'
operations_dir = os.environ['ENVROOT']
for plugin in plugins_yml.get('plugins'):
    plugin_name = plugin['name']

    # Set ENV vars
    plugin_dir = plugins_dir + plugin_name
    os.environ['PLUGIN_DIR'] = plugin_dir
    environment_dir = operations_dir + '/' + plugin_name
    os.environ['ENVIRONMENT_DIR'] = environment_dir

    # Load BitOps config using existing shell scripts
    print('Loading BitOps Config for ' + plugin_name)
    os.environ['ENV_FILE'] = plugin_dir + '/' + 'ENV_FILE'
    bitops_schema = plugin_dir + '/' + 'bitops.schema.yaml'
    bitops_config = environment_dir + '/' + 'bitops.config.yaml'
    old_debug = os.environ['DEBUG'] 
    os.environ['DEBUG'] = ''
    subprocess.run(['bash',os.environ['SCRIPTS_DIR']+'/bitops-config/convert-schema.sh', bitops_schema, bitops_config])
    os.environ['DEBUG'] = old_debug

    # Source envfile
    envbash.load_envbash(os.environ['ENV_FILE'])

    # Invoke Plugin
    result = subprocess.run(['bash', bitops_dir + '/deploy/before-deploy.sh', environment_dir], 
        universal_newlines = True,
        capture_output=True)
    print(result.stdout)

    print('Calling ' + plugin_dir + '/deploy.sh')
    result = subprocess.run(['bash', plugin_dir + '/deploy.sh'], 
        universal_newlines = True,
        capture_output=True)
    print(result.stdout)

    result = subprocess.run(['bash', bitops_dir + '/deploy/after-deploy.sh', environment_dir], 
        universal_newlines = True,
        capture_output=True)
    print(result.stdout)



