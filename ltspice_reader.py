#__author__ = 'NicholasYF'

import re


class InvalidRawFileError(Exception):

    def __init__(self, message):

        super(InvalidRawFileError, self).__init__(message)


class LtspicePlotVariable(object):

    def __init__(self, index, name, varType):

        self.index = index
        self.name = name
        self.type = varType


class RawFileReader(object):

    TAGS = {
        "TITLE": "title",
        "DATE": "date",
        "PLOTNAME": "plotname",
        "FLAGS": "flags",
        "NVARS": "no. variables",
        "NPTS": "no. points",
        "OFFSET": "offset",
        "COMMAND": "command",
        "BACKANNO": "backannotation",
        "VARS": "variables",
        "BINARY": "binary",
        "VALUES": "values",
    }

    def __init__(self, filename):
        self.filename = filename
        self.title = ""
        self.date = ""
        self.plotname = ""
        self.flags = []
        self.nvars = 0
        self.npts = 0
        self.offset = 0
        self.command = ""
        self.vars = []
        self.datapos = 0

        self.readHeader()

    def validate(self):
        return True

    def readHeader(self):
        tagsRegexStr = "^({}):.*".format("|".join([x if "." not in x
                                                   else "\.".join(x.split("."))
                                                   for x in RawFileReader.TAGS.values()]))
        varsRegexStr = r"^\s*\d+\s+[\w\(\):,]+\s+\w+"
        tagsRegex = re.compile(tagsRegexStr)
        varsRegex = re.compile(varsRegexStr)
        with open(self.filename, "rb") as fi:
            for line in fi:
                if tagsRegex.match(line.lower()):
                    tag = line.split(":", 1)[0].strip().lower()
                    contents = line.split(":", 1)[1].strip()
                    if tag.startswith(RawFileReader.TAGS["TITLE"]):
                        self.title = contents
                    elif tag.startswith(RawFileReader.TAGS["DATE"]):
                        self.date = contents
                    elif tag.startswith(RawFileReader.TAGS["PLOTNAME"]):
                        self.plotname = contents
                    elif tag.startswith(RawFileReader.TAGS["FLAGS"]):
                        self.flags = [x.strip().lower() for x in contents.split()]
                    elif tag.startswith(RawFileReader.TAGS["NVARS"]):
                        try:
                            self.nvars = int(contents)
                        except ValueError as e:
                            raise InvalidRawFileError("Invalid number of variables: {}".format(e))
                    elif tag.startswith(RawFileReader.TAGS["NPTS"]):
                        try:
                            self.npts = int(contents)
                        except ValueError as e:
                            raise InvalidRawFileError("Invalid number of points: {}".format(e))
                    elif line.lower().startswith(RawFileReader.TAGS["OFFSET"]):
                        try:
                            self.offset = float(contents)
                        except ValueError as e:
                            raise InvalidRawFileError("Invalid offset: {}".format(e))
                    elif line.lower().startswith(RawFileReader.TAGS["COMMAND"]):
                        self.command = contents
                    elif line.lower().startswith(RawFileReader.TAGS["BACKANNO"]):
                        pass
                    elif line.lower().startswith(RawFileReader.TAGS["VARS"]):
                        pass
                    elif line.lower().startswith(RawFileReader.TAGS["VALUES"]):
                        self.datatype = "values"
                        self.datapos = fi.tell()
                        break
                    elif line.lower().startswith(RawFileReader.TAGS["BINARY"]):
                        self.datatype = "binary"
                        self.datapos = fi.tell()
                        break
                elif varsRegex.match(line):
                    contents = line.split()
                    try:
                        variableIndex = contents[0]
                        variableName = contents[1]
                        variableType = contents[2]
                    except IndexError as e:
                        raise InvalidRawFileError("Invalid variable line: {}".format(line))
                    var = LtspicePlotVariable(variableIndex, variableName, variableType)
                    self.vars.append(var)
                else:
                    raise InvalidRawFileError("Unknown line: {}".format(line))






class BinaryReader(object):

    def __init__(self, filename):
        self.filename = filename


class ValuesReader(object):

    def __init__(self, filename):
        self.filename = filename


def main():
    filename = r"C:\Apps\LTC\LTspiceIV\Draft14.raw"
    rf = RawFileReader(filename)
    print rf.title
    print rf.date
    print rf.plotname

    print rf.datapos
    for v in rf.vars:
        print "{0}{1}{2}\n".format(v.index, v.name, v.type)


if __name__ == "__main__":
    main()
