from kiwipiepy import Kiwi

kiwi = Kiwi(model_type='knlm')

class KiwiTokenizer:
    def kiwi_tokenize(self, text):
        result = kiwi.tokenize(text)

        tokens = []
        for token in result:
            if token.tag in ['NNG', 'NNP', 'VA', 'VV', 'MAG', 'XR', 'SL']:
                tokens.append(token.form)
        return tokens
