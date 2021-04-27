import sys, re
from collections.abc import MutableMapping, MutableSequence

class Utilities:
    def simple(self, struct):
        return(type(struct) == str or type(struct) == int or type(struct) == float)

class DmarkBase(Utilities):
    def __init__(self, meta, path, init):
        if (type(meta) == list):
            self.meta = meta

        else:
            sys.exit("Err: meta required to build DmarkBase")

        if (type(path) == tuple):
            self.meta[1][id(self)] = path

        else:
            sys.exit("Err: path required to build DmarkBase")

        self.init = init

    def path(self):
        return(self.meta[1][id(self)])

    def meta_set(self, key, struct):
        if (not self.init):
            return(struct)

        key_path = (*self.path(), key)

        if (key_path in self.meta[0]):
            key_linenum = self.meta[0][key_path][0]
            old_len = len(self.meta[0])

            self.meta_del_children(key_path)
            diff = old_len - len(self.meta[0])
            self.meta_shift_below_by(key_linenum, -diff)

        else:
            key_location = self.meta_new_child_location(self.path())
            key_linenum = key_location[0]

            self.meta_shift_below_by(key_linenum - 1, 1)
            self.meta[0][key_path] = key_location

        if (type(struct) == DmarkDict or type(struct) == DmarkList):
            struct = struct.raw_value()

        if (type(struct) == dict):
            dmd = DmarkDict(self.meta, key_path, True)
            dmd.update(struct)
            return(dmd)

        elif (type(struct) == list):
            dml = DmarkList(self.meta, key_path, True)
            dml.extend(struct)
            return(dml)

        elif (self.simple(struct)):
            return(struct)

    # def meta_sort

    def meta_del_children(self, path):
        self.meta[0] = {
            k: v for (k, v) in self.meta[0].items()
            if not self.is_child(path, k)
        }

        self.meta[1] = {
            k: v for (k, v) in self.meta[1].items()
            if not self.is_child(path, v)
        }

    def meta_del_children_or_eq(self, path):
        self.meta[0] = {
            k: v for (k, v) in self.meta[0].items()
            if not self.is_child_or_eq(path, k)
        }

        self.meta[1] = {
            k: v for (k, v) in self.meta[1].items()
            if not self.is_child(path, v)
        }

    def meta_shift_below_by(self, linenum, diff):
        self.meta[0].update({
            k: (v[0] + diff, v[1]) for (k, v) in self.meta[0].items()
            if v[0] > linenum
        })

    def meta_shift_paths_after_or_at_by(self, path, diff):
        part = len(path) - 1
        reverse_meta = {v: k for (k, v) in self.meta[0].items()}
        reverse_meta.update({
            k: (*v[:part], v[part] + diff, *v[part+1:]) for (k, v) in reverse_meta.items()
            if self.is_after_or_at(path, v)
        })
        
        self.meta[0] = {v: k for (k, v) in reverse_meta.items()}

        self.meta[1].update({
            k: (*v[:part], v[part] + diff, *v[part+1:]) for (k, v) in self.meta[1].items()
            if self.is_after_or_at(path, v)
        })

    def meta_new_child_location(self, path):
        return((
            max([
                v[0] for (k, v) in self.meta[0].items()
                if self.is_child_or_eq(path, k)
            ]) + 1,
            self.meta[0][path][1] + 1
        ))

    @staticmethod
    def is_child(parent_path, candidate_path):
        return(
            parent_path == candidate_path[:len(parent_path)]
            and len(parent_path) != len(candidate_path)
        )

    @staticmethod
    def is_child_or_eq(parent_path, candidate_path):
        return(parent_path == candidate_path[:len(parent_path)])

    @staticmethod
    def is_after_or_at(prior_path, candidate_path):
        return(
            len(candidate_path) >= len(prior_path)
            and prior_path[:len(prior_path)-1] == candidate_path[:len(prior_path)-1]
            and candidate_path[len(prior_path)-1] >= prior_path[len(prior_path)-1]
        )


class DmarkList(DmarkBase, MutableSequence):
    def __init__(self, meta, path, init=False):
        super().__init__(meta, path, init)
        self.value = list()

    def _to_dict(self):
        dmd = DmarkDict(self.meta, self.path(), self.init)
        dmd.update({k: v for k, v in enumerate(self.value)})
        del self.meta[1][id(self)]
        return(dmd)

    def __getitem__(self, index):
        return(self.value[index])

    def __setitem__(self, index, value):
        self.value[index] = self.meta_set(index, value)

    def __delitem__(self, index):
        self.meta_del(index)
        del self.value[index]

    def __len__(self):
        return(len(self.value))

    def insert(self, index, value):
        self.value.insert(index, self.meta_insert(index, value))

    def __repr__(self):
        return(repr(self.value))

    def __str__(self):
        return(str(self.value))

    def meta_insert(self, index, struct):
        if (not self.init):
            return(struct)

        index_path = (*self.path(), index)

        if (index_path in self.meta[0]):
            index_location = self.meta[0][index_path]

            self.meta_shift_paths_after_or_at_by(index_path, 1)

        else:
            index_location = self.meta_new_child_location(self.path())

        index_linenum = index_location[0]

        self.meta_shift_below_by(index_linenum - 1, 1)
        self.meta[0][index_path] = index_location

        if (type(struct) == DmarkDict or type(struct) == DmarkList):
            struct = struct.raw_value()

        if (type(struct) == dict):
            dmd = DmarkDict(self.meta, index_path, True)
            dmd.update(struct)
            return(dmd)

        elif (type(struct) == list):
            dml = DmarkList(self.meta, index_path, True)
            dml.extend(struct)
            return(dml)

        elif (self.simple(struct)):
            return(struct)

    def meta_del(self, index):
        if (not self.init):
            return

        index_path = (*self.path(), index)
        index_linenum = self.meta[0][index_path][0]
        old_len = len(self.meta[0])

        self.meta_del_children_or_eq(index_path)
        self.meta_shift_paths_after_or_at_by(index_path, -1)

        diff = old_len - len(self.meta[0])
        self.meta_shift_below_by(index_linenum, -diff)


class DmarkDict(DmarkBase, MutableMapping):
    def __init__(self, meta, path, init=False):
        super().__init__(meta, path, init)
        self.value = dict()

    def __getitem__(self, key):
        return(self.value[key])

    def __setitem__(self, key, value):
        self.value[key] = self.meta_set(key, value)

    def __delitem__(self, key):
        self.meta_del(key)
        del self.value[key]

    def __iter__(self):
        return(iter(self.value))

    def __len__(self):
        return(len(self.value))

    def __repr__(self):
        return(repr(self.value))

    def __str__(self):
        return(str(self.value))

    def meta_del(self, key):
        if (not self.init):
            return

        key_path = (*self.path(), key)
        key_linenum = self.meta[0][key_path][0]
        old_len = len(self.meta[0])

        self.meta_del_children_or_eq(key_path)

        diff = old_len - len(self.meta[0])
        self.meta_shift_below_by(key_linenum, -diff)


class Dmark(Utilities):
    def __init__(self, file_name):
        self.load_file(file_name)

    def load_file(self, file_name):
        self.file_name = file_name
        self.value, self.meta = self.parse_file(file_name)
        self.old_meta = self.meta[0].copy()

    def raw_value(self):
        def raw_value_recur(value):
            if (type(value) == DmarkDict):
                return({k: raw_value_recur(v) for (k, v) in value.items()})

            elif (type(value) == DmarkList):
                return([raw_value_recur(v) for v in value])

            elif (self.simple(value)):
                return(value)

        return(raw_value_recur(self.value))

    def write(self):
        f = open(self.file_name, "r")
        lines = f.readlines()
        f.close()

        offset = 1
        for (linenum, _) in sorted(self.old_meta.values(), key=(lambda t: t[0])):
            if (linenum > 0):
                del lines[linenum - offset]
                offset += 1

        def write_line(content, path):
            (linenum, indent) = self.meta[0][path]

            if (type(content) == tuple):
                line = str(content[0]) + ": " + str(content[1])

            elif (type(content) == list):
                line = " " + str(content[0])

            elif (self.simple(content)):
                line = str(content)

            elif (not content):
                line = ""

            line = "\t" * indent + "@" + line + "\n"
            lines.insert(linenum - 1, line)

        def write_recur(value, path=()):
            if (type(value) == DmarkDict):
                for (k, v) in value.items():
                    key_path = (*path, k)

                    if (type(v) == DmarkDict or type(v) == DmarkList):
                        write_line(k if type(k) != int else None, key_path)
                        write_recur(v, key_path)

                    elif (type(v) == str or type(v) == int):
                        write_line((k, v) if type(k) != int else [v], key_path)

            elif (type(value) == DmarkList):
                i = 0
                for element in value:
                    element_path = (*path, i)

                    if (type(element) == DmarkDict or type(element) == DmarkList):
                        write_line(None, element_path)
                        write_recur(element, element_path)

                    elif (self.simple(element)):
                        write_line([element], element_path)

                    i +=1

        write_recur(self.value)

        f = open(self.file_name, "w")
        f.writelines(lines)
        f.close()

        self.old_meta = self.meta[0].copy()

    @staticmethod
    def parse_file(file_name):
        def strip_line(line, count=0):
            head = line[0]
            if (head == "\t"):
                return strip_line(line[1:], count+1)
        
            else:
                return (line, count)

        lines = []
        with open(file_name, "r") as f:
            line = f.readline()

            linenum = 1
            while (line):
                content, indent = strip_line(line)

                if (content[0] == "@"):
                    content = content.strip()

                    if (re.fullmatch(r"@.*: .*", content)):
                        content = content.split(": ")

                        key = content[0][1:]
                        val = content[1]

                        try:
                            val = float(val)

                            if (int(val) == val):
                                val = int(val)

                        except Exception:
                            pass

                        ret = (key, val)

                    elif (re.fullmatch(r"@ ..*", content)):
                        val = content[2:]

                        try:
                            val = float(val)

                            if (int(val) == val):
                                val = int(val)

                        except Exception:
                            pass

                        ret = [val]

                    elif (re.fullmatch(r"@..*", content)):
                        ret = content[1:]

                    elif (re.fullmatch(r"@", content)):
                        ret = None

                    lines.append((ret, (linenum, indent)))

                line = f.readline()
                linenum += 1

        def value_gen(lines, meta, depth=0, parent_path=()):
            value = DmarkList(meta, parent_path)

            while (len(lines) > 0):
                content, location = lines[0]
                indent = location[1]

                if (indent == depth):
                    del lines[0]

                    # List (str or int)
                    if (type(content) == list):
                        if (type(value) == DmarkDict):
                            sys.exit("Err: no keyless values in dict")

                        index = len(value)
                        new_path = (*parent_path, index)

                        new_value = content[0]
                        value.append(new_value)

                    # Dict (str or int)
                    elif (type(content) == tuple):
                        if (type(value) == DmarkList and len(value) == 0):
                            value = value._to_dict()

                        elif (type(value) == DmarkList and len(value) > 0):
                            sys.exit("Err: no keyed values in list")

                        key = content[0]
                        new_path = (*parent_path, key)

                        new_value = content[1]
                        value[key] = new_value

                    # Dict (dict or list)
                    elif (type(content) == str):
                        if (type(value) == DmarkList):
                            value = value._to_dict()

                        key = content
                        new_path = (*parent_path, key)

                        new_value = value_gen(lines, meta, depth+1, new_path)
                        value[key] = new_value

                    # List (dict or list)
                    elif (not content):
                        if (type(value) == DmarkDict):
                            sys.exit("Err: no keyless values in dict")

                        index = len(value)
                        new_path = (*parent_path, index)

                        new_value = value_gen(lines, meta, depth+1, new_path)
                        value.append(new_value)

                    meta[0][new_path] = location
                    meta[1][id(new_value)] = new_path

                elif (indent > depth):
                    sys.exit("Err: badly indented line")

                else:
                    return(value)

            return(value)

        def init(value):
            if (type(value) == DmarkDict):
                value.init = True

                for (_, val) in value.items():
                    init(val)

            elif (type(value) == DmarkList):
                value.init = True
                
                for val in value:
                    init(val)

        meta = [{():(-1, -1)}, {-1: ()}]
        value = value_gen(lines, meta)
        init(value)

        return(value, meta)




