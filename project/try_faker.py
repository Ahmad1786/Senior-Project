# Did not end up using faker for now

# create fake data
from faker import Faker
fake = Faker()
Faker.seed(36746347)

PASSWORD = 'adminadmin'
first_names = []
last_names = []
emails = []

def create_email(f, l):
    return f.lower() + l.lower() + '@random.com'

for _ in range(10):
    first_names.append(fake.first_name())
    last_names.append(fake.last_name())

for f, l in zip(first_names, last_names):
    emails.append(create_email(f, l))

print(first_names)
print(last_names)
print(emails)


print(fake.text(20*200)) # takes a minimum words count?
print(fake.random_int(min=0, max=100, step=1))
for _ in range(10):
    print(fake.random_int(min=0, max=1, step=1), end=' ')
print()

