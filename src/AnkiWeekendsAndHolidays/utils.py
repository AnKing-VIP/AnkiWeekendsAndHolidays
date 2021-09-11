

def add_compat_alias(namespace, new_name, old_name):
    if new_name not in list(namespace.__dict__.keys()):
        setattr(namespace, new_name, getattr(namespace, old_name))
        return True
    
    return False