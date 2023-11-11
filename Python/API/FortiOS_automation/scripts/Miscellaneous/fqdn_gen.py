

fqdn_list = '''
api.stripe.com
checkout.stripe.com
dashboard.stripe.com
files.stripe.com
js.stripe.com
m.stripe.com
m.stripe.network
q.stripe.com
verify.stripe.com
stripe.com
'''


temp = '''
config firewall address
    edit <FQDN>
        set type fqdn
        set fqdn <FQDN>
    next
end
'''

for item in fqdn_list.split():
    print(temp.replace('<FQDN>', item))