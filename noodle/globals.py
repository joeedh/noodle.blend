from . import utils

#NOTE: this module never has imp.reload() called on it,
#it represents permanent global state

module_registrar = utils.Registrar([])
