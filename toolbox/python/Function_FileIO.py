import os


class FncFileHandling:

    def create_file(self):
        if not os.path.exists(self):
            f = open(self, "w")
            f.close()
            return "createSuccess"
        else:
            return "fileExists"

    def delete_file(self):
        if os.path.exists(self):
            os.remove(self)
            return "deleteSuccess"
        else:
            return "fileNotFound"

    def read_line(self):
        try:
            with open(self, "r") as f:              #auto file close when block exits
                lines = [x.rstrip() for x in f]
            return lines.__len__()
        except:
            return "openFailed"

    def read_string(self, char):
        try:
            f = open(self, "r")
            if char > 0:
                return f.read(char)
            else:
                return f.read()
        except:
            return "openFailed"
        finally:
            if "f" in locals():
                f.close()

    def append_line(self, value):
        try:
            f = open(self, "a")
            f.write(value)
            f.close()
            with open(self, "r") as f:
                lines = [x.rstrip() for x in f]
            return lines.__len__()
        except:
            return "openFailed"
        finally:
            if "f" in locals():
                f.close()

    def remove_line(self, value):
        try:
            f = open(self, "r+")
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != value and i != "\n":
                    f.write(i)
            f.truncate()
        except:
            return "openFailed"
        finally:
            if "f" in locals():
                f.close()
