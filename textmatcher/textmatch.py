import logging
import re

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


class Trigger:
    def __init__(self, match_method=None, match_phrases=None, event=None, full_text=None, full_text_ratio=0.7):
        self.matchMethod = match_method
        self.matchPhrases = match_phrases
        self.event = event
        self.fullText = full_text
        self.fullTextRatio = full_text_ratio

    @staticmethod
    def normalize_test_string(s: str):
        return s.replace("0", "o") \
            .replace("3", "e") \
            .replace("4", "a") \
            .replace("5", "s") \
            .replace("7", "t") \
            .lower()

    def check(self, test_text: str):
        test_text_lower = self.normalize_test_string(test_text)
        log.debug("Checking " + str(test_text_lower))
        chunks = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", test_text_lower)
        return any(self.matchMethod.check(x) for x in chunks)


class And:
    def __init__(self, *args):
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message) -> bool:
        log.debug("Checking And " + str(len(self.triggers)))
        res = True
        for t in self.triggers:
            if type(t) is str:
                res &= bool(re.search(f"\\b{t}\\b", message))
            else:
                res &= t.check(message)
                if not res:
                    break
        return res


class Or:
    def __init__(self, *args):
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message) -> bool:
        log.debug("Checking Or " + str(len(self.triggers)))
        res = False
        for t in self.triggers:
            if type(t) is str:
                res |= bool(re.search(f"\\b{t}\\b", message))
            else:
                res |= t.check(message)
            if res:
                break
        return res


class Not:
    def __init__(self, *args):
        if len([*args]) != 1:
            log.error("Misconfigured Not, it's going to get weird")
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message) -> bool:
        log.debug("Checking Not " + str(len(self.triggers)))
        if type(self.triggers[0]) is str:
            res = not re.search(f"\\b{self.triggers[0]}\\b", message)
        else:
            res = not self.triggers[0].check(message)

        return res


class StartsWith:
    def __init__(self, *args):
        if len([*args]) != 1:
            log.error("Misconfigured Startswith, it's going to get weird")
        self.triggers = list(map(lambda x: x.lower() if type(x) == str else x, [*args]))

    def check(self, message: str) -> bool:
        log.debug("Checking StartsWith " + str(len(self.triggers)))
        if type(self.triggers[0]) is str:
            return message.startswith(self.triggers[0])

        return False
