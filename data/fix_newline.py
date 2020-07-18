

lines = []
counter = 0
train_to = "train.to"
train_from = "train.from"

# Code to remove not needed chars

# f = open(train_from)
# lines = [line.replace('newlinechar', '') if 'newlinechar' in line else line for line in f]
# print('done')

# new_file = open("train.from", "w")
# for line in lines:
#     counter += 1
#     new_file.write(line)

#     if (counter % 1000) == 0:
#         print('counter')
#         print(counter)

train_from = open(train_from, "r").readlines()
train_to = open(train_to, "r").readlines()
new_train_file = open("train.txt", "w")

# Format trainings
print('Formatting training files into one')

counter = 0
for line in train_from:
    statement = train_from[counter]
    response = train_to[counter]
    new_train_file.write(statement)
    new_train_file.write(response)
    if (counter % 1000) == 0:
        print('counter')
        print(counter)
    counter += 1