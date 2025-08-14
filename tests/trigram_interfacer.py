from unidecode import unidecode
class Trigram:
    data: str
    trigrams: set
    verbose: bool
    
    
    def __init__(self, data, verbose = False):
        self.verbose = verbose
        self.data = unidecode(data)
        self.trigrams = set()
        self._get_trigrams()
        self._log(self.data)
        
    def _log(self, *args):
        if self.verbose:
            print(*args)
            
    def _get_trigrams(self):
        for i in range(len(self.data) // 3):
            self.trigrams.add(self.data[i:i+3].lower())
            self._log(i, " ", self.data[i:i+3].lower())
            
    def __call__(self) -> set[str]:
        return self.trigrams
if __name__ == "__main__":
    tg = Trigram(data="The quick brown fox jumped over the lazy dog. Pablo has 15 Piñatas.", verbose=True)