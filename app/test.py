test = 'abc122$  jkdl90() '
result =''
for i in test:
    if i.isalnum():
        print(i.isalnum())
        result = result +i
print(result)