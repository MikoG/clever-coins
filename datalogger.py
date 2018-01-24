class DataLogger:

    __NEWLINE = '\r\n'
    
    def __init__(self, data, filename):
        self.__filename = filename
        header = self.__generate_line(data, 0)
        self.f = open(self.__filename, 'a+')
        size = self.f.tell()
        if size == 0:
            self.f.write(header + self.__NEWLINE)
            self.f.flush()
        else:
            self.f.seek(0, 0)
            file_header = self.f.readline()[:-1]
            assert file_header == header, 'the header in the log file does not match the data being provided'
            pos = self.f.seek(0, 2)

    def add_line(self, data):
        data = self.__generate_line(data, 1)
        self.f.write(data + self.__NEWLINE)
        self.f.flush()

    ## line_type 0 = header line
    #  line_type 1 = data line
    def __generate_line(self, data, line_type = 0):
        header = ''
        first = True
        for field in sorted(data):
            if line_type == 0:
                text = str(field)
            else:
                text = str(data[field])
            
            if not first:
                text = ', ' + text
            
            header += text
            first = False

        return header
