

def add_compat_alias(namespace, new_name, old_name):
    if new_name not in dir(namespace):
        setattr(namespace, new_name, getattr(namespace, old_name))
        return True
    
    return False