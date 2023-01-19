import ldap

# connect to the server
l = ldap.initialize("ldap://localhost")

# bind to the server
l.bind_s("cn=admin,dc=messaging,dc=com", "12345")

# search for a user
result = l.search_s("dc=messaging,dc=com", ldap.SCOPE_SUBTREE, "(cn=Amine Gharbi)")
# print the result
print(result)

# unbind from the server
l.unbind_s()
