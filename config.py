# Bot Token
TOKEN = "CHANGE_ME"

# Server ID
GUILD_ID = 1234567890123456789 # Example

# Embed Colors
EMBED_COLOR = int("58bed5", 16) # Change inside "", dont touch 16

# Welcome
# Preferred welcome channel
WELCOME_CHANNEL_ID = 1234567890123456789 # Example
WELCOME_IMAGE_URL = "https://example.com/approved.png"

# Verify Feature
# Role to give when verified
VERIFIED_ROLE_ID = 1234567890123456789 # Example
VERIFY_PUBLIC_LOG_CHANNEL = 1234567890123456789 # Example
VERIFY_LOG_CHANNEL_ID = 1234567890123456789 # Example
APPROVED_IMAGE_URL = "https://example.com/approved.png"
DENIED_IMAGE_URL = "https://example.com/denied.png"

# Blacklist of user IDs who cannot verify
BLACKLIST = [
    1234567890123456789, # example
]

# Qbox Player Info (FiveM)
# Database for Qbox
DB_HOST = "" # IP/Address
DB_USER = "" # DB Username
DB_PASS = "" # DB Password
DB_NAME = "" # DB Name

# Polls
# Can everyone do polls or only admins/mods?
POLLONLYADMIN = True

# Tickets
# All done within discord (/help)
TICKET_LOG_CHANNEL_ID = 1234567890123456789

# Feature Toggles
FEATURES = {
    "welcome": True,
    "verify": True,
    "admin": True,
    "stickynote": True,
    "tickets": True,
    "playerlookup": True,
    "purge": True,
    "serverinfo": True,
    "giveaways": True,
    "polls": True,
    "help": True,
}