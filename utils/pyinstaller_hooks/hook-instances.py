from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('hybrid_cc.game.elements.instances')
datas = collect_data_files('hybrid_cc.game.elements.instances',
                           include_py_files=True)
