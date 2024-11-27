import argparse

class SorchaArgparse(argparse.ArgumentParser):
    
    
    def __init__(self, *argv, **kwargs):
        super().__init__( **kwargs)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
 
    def print_usage(self,file=None):
        super().print_usage(file)
        print(f"For more detailed help try: {self.prog} -h ",file=file)