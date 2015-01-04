from zipfile import ZipFile
import shutil
import os.path

from file_handling import fetch_url, mkdir


class Mod_File(dict):
    attribs = sorted(('name',
                      'description',
                      'required_on_server',
                      'required_on_client',
                      'download_url_primary',
                      'download_url_secondary',
                      'download_md5',
                      'install_method',
                      'install_path',
                      'install_filename',
                      'special_actions',
                      'comments'))

    def __init__(self, **kwargs):
        super(Mod_File, self).__init__(**kwargs)
        for a in self.attribs:
            self[a] = None

    def download(self):
        self.validate_attributes()
        print ("Downloading {f} from {u}".format(f=self['install_filename'], u=self['download_url_primary']))
        fetch_url(self['download_url_primary'], self['install_filename'], self['download_md5'])

    def install(self, mod_pack):
        self.validate_attributes()
        inst_path = os.path.join(mod_pack['install_folder'], self['install_path'])
        src_path = os.path.join(mod_pack['download_cache_folder'], self['install_filename'])
        mkdir(inst_path)
        if self['install_method'] == 'copy':
            print ("Installing {f} by copying to {d}".format(f=src_path, d=inst_path))
            shutil.copy(src_path, inst_path)
        elif self['install_method'] == 'unzip':
            with ZipFile(src_path, 'r') as z:
                print ("Installing {f} by unzipping to {d}".format(f=src_path, d=inst_path))
                z.extractall(inst_path)

    def validate_attributes(self):
        assert sorted(self.keys()) == self.attribs  # Check no extra attributes added
        assert self['name'] is not None
        assert self['download_url_primary'] is not None
        assert self['required_on_server'] in (True, False)
        assert self['required_on_client'] in (True, False)
        assert self['install_method'] in ('copy', 'unzip')
        assert self['install_path'] is not None
        assert self['install_filename'] is not None
        assert self['special_actions'] in (None, 'create_run_sh')
        