# imports
from newinsta import NewInsta

# login credentials
insta_username = 'charliefoxx9'
insta_password = 'pzvL~juqs4C_[X_<'

insta_session = NewInsta(insta_username, insta_password, headless=False)

insta_session.login(insta_username, insta_password)

# insta_session.sendMessage(user='le.nae', message='Hoe bitch')

# insta_session.sendGroupMessage(
    # users=['le.nae', 'jcrns'], message='Lenae smells like two trash bins in Mexico')

insta_session.checkUp()
# insta_session.automatic(hitUpChance=100, checkUp=1000)
