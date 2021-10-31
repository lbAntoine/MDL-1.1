
import re


class outils:
    def clean(self, txt_):
        str_txt = str(txt_)
        clean_txt = ''
        regex = r"[\w -]+"

        matches = re.finditer(regex, str_txt, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            #print(match.group())
            clean_txt += match.group()
        return clean_txt

    def coucou(self, name):
        print(f'Coucou {name}!')
