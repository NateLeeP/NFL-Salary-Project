class QB:
    def __init__(self, name, fb_url=None, sp_url=None): # optional arguments       
        if fb_url is not None: # meaning you passed a value into the constructor
            self.pro_fb_url = fb_url
        else:
             self.pro_fb_url = self.pro_fb_url.format(self.name.split()[1][0], self.pro_football_url_name(self.name))
                  
        if sp_url is not None:
            self.spotrac_url = sp_url
        else:
            self.spotrac_url = self.spotrac_url.format(self.team_name.lower().replace(' ','-'), self.name.lower().replace(' ','-'))

        ...


def main():

    # using a dict to get url for the guy
    hot_fixes = {
        'joe flacco': ('the-fb-url-for-this-fuck', 'the-other-sp-url-for-this-cunt'),
        'daniel jones': ('https://spankbang.cum', 'second-source-url')
    }

    for name in qbs:
        if name in hot_fixes.keys():
            # will set self.pro_fb_url and self.spotrac_url to the urls you pass here from the hot_fixes dict
            qb_object = QB(name, fb_url=hot_fixes[name][0], sp_url=hot_fixes[name][1])
        else:
            qb_object = QB(name) # works exactly as you already have it
