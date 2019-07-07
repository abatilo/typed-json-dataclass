import json
import plac
import toml

def main(package_json_path: 'path to the package.json file', pyproject_toml_path: ('path'
         ' to the pyproject.toml file to sync version string to')):
  package_json = json.load(open(package_json_path, 'r'))
  pyproject_toml = toml.load(open(pyproject_toml_path, 'r'))
  package_json_version = package_json['version']
  pyproject_toml_version = pyproject_toml['tool']['poetry']['version']
  pyproject_toml['tool']['poetry']['version'] = package_json_version
  toml.dump(pyproject_toml, open(pyproject_toml_path, 'w'))

  print(f'{pyproject_toml_version} -> {package_json_version}')

def entrypoint():
  plac.call(main)

if __name__ == '__main__':
  entrypoint()
