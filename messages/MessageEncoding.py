import json


class MessageDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            inst = class_(**args)
        else:
            inst = d
        return inst


class MessageEncoder(json.JSONEncoder):
    def default(self, o):
        d = {'__class__':   o.__class__.__name__,
             '__module__':  o.__module__}
        d.update(o.__dict__)
        return d
