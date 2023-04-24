class AppException(Exception):
    def __init__(self):
        super()
    
class InputException(AppException):
    def __init__(self, args='f'):
        """
            @params: 
                default args='f' 
                f: format
                e: empty
        """
        self.msg = {
            "f": "Please enter the correct format!",
            "e": "Empty input!",
        }
        self.value = self.msg[args]

    def __str__(self):
        return self.value
    
class DataException(AppException):
    def __init__(self, args='nm'):
        """
            @params: 
                default args='nm' 
                nm: no match
        """
        self.msg = {
            'nm': "No matching data!",
        }
        self.value = self.msg[args]

    def __str__(self):
        return self.value

if __name__ == "__main__":
    try:
        raise DataException("nm")
    except DataException as e:
        print(e)