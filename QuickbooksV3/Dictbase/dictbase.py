import pickle

class AutoSaveDict:
    def __init__(self, filename):
        self.filename = filename
        self._dictionary = self.load_dict_from_file()

    def __getitem__(self, key):
        return self._dictionary[key]

    def __setitem__(self, key, value):
        self._dictionary[key] = value
        self.save_dict_to_file()

    def __delitem__(self, key):
        del self._dictionary[key]
        self.save_dict_to_file()

    def __iter__(self):
        return iter(self._dictionary)

    def __len__(self):
        return len(self._dictionary)

    def items(self):
        return self._dictionary.items()

    def save_dict_to_file(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self._dictionary, f)

    def load_dict_from_file(self):
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def __repr__(self):
        return repr(self._dictionary)
    
    def __str__(self):
        return str(self._dictionary)

db = AutoSaveDict('dictbase.pickle')
