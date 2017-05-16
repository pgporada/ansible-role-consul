'''
Made possible thanks to http://www.danielhall.me/2014/09/creating-rr-records-in-route53-with-ansible/

In Ansible lots of things take lists (or comma seperated
strings), however lots of things return dicts. One
example of this is the hostvars and groups variable.

'groups' returns a list of machines in a group, and
'hostvars' is a dict containing all the hosts. So if you
need a list of ip addresses of those hosts for the
route53 module you cant.
'''

def fetchlistfromdict(d, l):
    result = []
    for i in l:
        result.append(d[i])
    return result

class FilterModule(object):
    def filters(self):
        return {
                'fetchlistfromdict': fetchlistfromdict,
        }
