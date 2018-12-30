import os.path, imp, importlib, sys

#little re to detect if path starts with directory slashes (with or without dots) or not
#import re
#tests = ["\.\/", "\.\.\/", "\/", r"\.\\", r"\\", r"\.\.\\", r"[a-zA-Z]\:\\"]
#test = "(" + ")|(".join(tests) + ")"
#test += ".*"
#print(test)
#test = re.compile(test)
#print(test.match(r"c:\bleh"))

def find_parentpath():
    path = __file__

    path = os.path.split(path)[0].strip()
    while path.endswith(os.path.sep) or path.endswith("/"):
        path = path[:-1].strip()
        
    path += os.path.sep + ".." + os.path.sep
    path = os.path.normpath(os.path.abspath(path))

    path = path.strip()
    while path.endswith(os.path.sep) or path.endswith("/"):
        path = path[:-1].strip()
    
    return path

#accepts both module names and paths
def load_parentmodule(name, report_error=False, raise_error=False):
    global parentpath
    
    if name.strip().lower().endswith(".py"):
        name = os.path.split(name.strip())[-1].remove(".py")
    
    if name in sys.modules:
        #print("returning cached module")
        return sys.modules[name]
        
    try:
        mod = imp.find_module(name, [parentpath])
    except ImportError:
        if report_error:
            sys.stderr.write("Failed to load %s!\n", name)
        if raise_error:
            raise ImportError("Failed to load %s!\n", name)
            
        return None
    
    #print("NAME", name)
    
    mod = imp.load_module(name, mod[0], mod[1], mod[2])
    sys.modules[name] = mod
    
    return mod
    
parentpath = os.path.normpath(find_parentpath())
