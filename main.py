import re
import tweepy
import logging
import time
import csv
from iota_wallet import IotaWallet, StrongholdSecretManager
import os
from dotenv import load_dotenv
from twitter_bot import run_twitter_bot

load_dotenv()
# Load information from .env file
stronghold_password = os.getenv("STRONGHOLD_PASSWORD")
shimmer_mnemonic = os.getenv("SHIMMER_MNEMONIC")
shimmer_native_token_id = os.getenv("SHIMMER_NATIVE_TOKEN_ID")
shimmer_native_token_amount = os.getenv("SHIMMER_NATIVE_TOKEN_AMOUNT")
twitter_user_id_to_monitor = os.getenv("TWITTER_USER_ID_TO_MONITOR")
twitter_status_id_to_monitor = os.getenv("TWITTER_STATUS_ID_TO_MONITOR")
twitter_last_tweet_reply = os.getenv("LAST_TWEET_REPLY_ID")
config_done = os.getenv("CONFIG_DONE")
tweet_keyword = os.getenv("TWEET_KEYWORD_TO_SEARCH")
shimmer_address_pattern = os.getenv("SHIMMER_ADDRESS_PATTERN")
shimmer_receiver_address = None

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


#####################################
# TWITTER SECTION
#####################################

# Twitter Configuration
def ConfigureTwitterBot():
    global config_done

    if config_done == "1":
        print("Configuration was already done. Use Option 3 to run the bot or Option 7 to RESET the configuration.")
        input("Press Enter to continue...")
        os.system('clear')
        return
    elif config_done == "0":
        print("Configuration start")
        print("What you will need:")
        print(" - Native Token ID to send")
        print("   (example: 0x08967b40894f97a226630ea16a752bd44697154e5c514da0f5fa76076eaaf4cf5a0100000000)")
        print(" - Token amount to send to every single address")
        print(" - Your Twitter Account name")
        print(" - The Twitter tweet number you want to monitor")
        
        def InsertShimmerNativeTokenId():
            while(True):
                try:
                    # compiling the pattern for alphanumeric string
                    pat = re.compile(r"[0]+[x]+[A-Za-z0-9]{76}")
                
                    # Prompts the user for input string
                    test = input("Enter Shimmer Native Token ID: ")
                    
                    # Checks whether the whole string matches the re.pattern or not
                    if re.fullmatch(pat, test):
                        print(f"Native Token ID entered = '{test}'")
                        shimmer_native_token_id = test
                        return shimmer_native_token_id
                    else:
                        print(f"'{test}' is NOT a native token ID!")
                except:
                    print("Try again")
                continue

        def InsertShimmerNativeTokenAmount():
            while(True):
                try:
                    # compiling the pattern for alphanumeric string
                    pat = re.compile(r"[0]+[x]+[A-Za-z0-9]{76}")
                
                    # Prompts the user for input string
                    test = input("Enter Shimmer Native Token ID: ")
                    
                    # Checks whether the whole string matches the re.pattern or not
                    if re.fullmatch(pat, test):
                        print(f"Native Token ID entered = '{test}'")
                        shimmer_native_token_id = test
                        return shimmer_native_token_id
                    else:
                        print(f"'{test}' is NOT a native token ID!")
                except:
                    print("Try again")
                continue

        def InsertShimmerNativeTokenAmount():
            while(True):
                try:
                    # compiling the pattern for alphanumeric string
                    pat = re.compile(r"[0-9]+")
                
                    # Prompts the user for input string
                    test = input("Enter Shimmer Native Token Amount to send: ")
                    
                    # Checks whether the whole string matches the re.pattern or not
                    if re.fullmatch(pat, test):
                        print(f"Native Token Amount to send entered = '{test}'")
                        shimmer_native_token_amount = test
                        return shimmer_native_token_amount
                    else:
                        print(f"'{test}' is NOT a correct token amount!")
                except:
                    print("Try again")
                continue

        def InsertTwitterUserIdToMonitor():
            while(True):
                try:
                    # Prompts the user for input string
                    test = input("Enter Your Twitter User ID: ")
                    
                    # Checks whether the whole string matches the re.pattern or not
                    print(f"Twitter User ID entered = '{test}'")
                    twitter_user_id = test
                    return twitter_user_id
                except:
                    print("Try again")
                continue

        def InsertTwitterStatusIdToMonitor():
            while(True):
                try:
                    # compiling the pattern for alphanumeric string
                    pat = re.compile(r"[0-9]+")
                
                    # Prompts the user for input string
                    test = input("Enter Twitter Status ID to watch for replies: ")
                    
                    # Checks whether the whole string matches the re.pattern or not
                    if re.fullmatch(pat, test):
                        print(f"Twitter Status ID entered = '{test}'")
                        twitter_status_id = test
                        return twitter_status_id
                    else:
                        print(f"'{test}' is NOT a correct Twitter Status ID!")
                except:
                    print("Try again")
                continue

        def WriteToEnv():
            with open('.env','r',encoding='utf-8') as file:
                data = file.readlines()
            data[6] = "TWITTER_USER_ID_TO_MONITOR="+ str(twitter_user_id_to_monitor +"\n")
            data[7] = "TWITTER_STATUS_ID_TO_MONITOR="+ str(twitter_status_id_to_monitor +"\n")
            data[13] = "SHIMMER_NATIVE_TOKEN_ID="+ str(shimmer_native_token_id +"\n")
            data[14] = "SHIMMER_NATIVE_TOKEN_AMOUNT="+ str(shimmer_native_token_amount +"\n")
            data[18] = "CONFIG_DONE=1"
            with open('.env', 'w', encoding='utf-8') as file:
                file.writelines(data)

        shimmer_native_token_id = InsertShimmerNativeTokenId()
        shimmer_native_token_amount = InsertShimmerNativeTokenAmount()
        twitter_user_id_to_monitor = InsertTwitterUserIdToMonitor()
        twitter_status_id_to_monitor = InsertTwitterStatusIdToMonitor()

        WriteToEnv()
        config_done = "1"
        input("Press Enter to continue...")
        os.system('clear')

def ResetTwitterBotConfiguration():
    global config_done
    def WriteToEnv():    
        with open('.env','r',encoding='utf-8') as file:
            data = file.readlines()
        data[6] = "TWITTER_USER_ID_TO_MONITOR=\n"
        data[7] = "TWITTER_STATUS_ID_TO_MONITOR=\n"
        data[13] = "SHIMMER_NATIVE_TOKEN_ID=\n"
        data[14] = "SHIMMER_NATIVE_TOKEN_AMOUNT=\n"
        data[18] = "CONFIG_DONE=0"
        data[20] = "LAST_SMR_ADDRESS_SENT_TO=\n"
        data[21] = "LAST_TWEET_REPLY_ID=\n"
        with open('.env', 'w', encoding='utf-8') as file:
            file.writelines(data)
    WriteToEnv()
    config_done = "0"
    input("Press Enter to continue...")
    os.system('clear')

def ShowConfigurationTwitterBot():
    with open('.env','r',encoding='utf-8') as file:
        data = file.readlines()
        print("Actual configuration")
        print(data[6])
        print(data[7])
        print(data[13])
        print(data[14])
        print(data[13])
        print(data[19])
        print(data[20])
        print(data[21])
        print(data[22])
        input("Press Enter to continue...")
        os.system('clear')

# Twitter Bot
def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def check_mentions(api, keywords, user_name, monitor_id, since_id):
    global shimmer_address_pattern
    global shimmer_receiver_address
    logger.info("Retrieving replies")
    tweet_id = monitor_id
    name = user_name
    while(True):
        sleep(30)
        for tweet in tweepy.Cursor(api.search_tweets,q='to:'+name).items(1000):
            try:
                #print(tweet.text)
                #for each status, overwrite that status by the same status, but from a different endpoint.
                status = api.get_status(tweet.id, tweet_mode='extended')
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                
                    if tweet.in_reply_to_status_id_str == tweet_id:
                        logger.info("There is a reply")
                        print("Since ID " + str(since_id))
                        if int(tweet.id) >= int(since_id):
                        
                            if tweet.user.following == True:
                                logger.info("Is Following")
                                
                                if any(keyword in tweet.text.lower() for keyword in keywords):
                                    shimmer_reply_address = re.findall(shimmer_address_pattern, tweet.text, flags=re.IGNORECASE)
                                    logger.info("Looking for address")
                                    for shimmer_receiver_address in shimmer_reply_address:
                                        logger.info("Address found")
                                        with open('.env','r',encoding='utf-8') as file:
                                            data = file.readlines()
                                        data[20] = "LAST_SMR_ADDRESS_SENT_TO="+ str(shimmer_receiver_address +"\n")
                                        with open('.env', 'w', encoding='utf-8') as file:
                                            file.writelines(data)
                                        logger.info(tweet.favorited)

                                        if status.favorited == False:
                                            try:
                                                logger.info("Is not Liked")
                                                with open('.env','r',encoding='utf-8') as file:
                                                    data = file.readlines()
                                                data[21] = "LAST_TWEET_REPLY_ID="+ str(tweet.id) +"\n"
                                                with open('.env', 'w', encoding='utf-8') as file:
                                                    file.writelines(data)
                                                tweet.favorite()
                                                since_id = tweet.id
                                                logger.info("Tweet is now liked")
                                                SendNativeToken()
                                                #continue
                                            except tweepy.TweepyException as e:
                                                print('Error: ' + str(e))
                                                #continue
                                        elif status.favorited == True:
                                            logger.info("Is liked no need to send tokens")
                                            #continue                                                 
            except tweepy.TweepyException as e:
                print('Error: ' + str(e))
                #continue
#        except StopIteration:
#            break

def RunTwitterBot():
    api = create_api()
    monitor_id = twitter_status_id_to_monitor
    since_id = twitter_last_tweet_reply
    user_name = twitter_user_id_to_monitor
    keywords = tweet_keyword
    since_id = check_mentions(api, keywords, user_name, monitor_id, since_id)


#####################################
# SHIMMER SECTION
#####################################
# Option one create a Shimmer profile
def CreateShimmerProfile():
    # Check if wallet.stronghold exists and exit if present
    if os.path.isfile('wallet.stronghold') == True:
        print("Profile already exists. Choose a different option.")
        input("Press Enter to continue...")
        os.system('clear')

    else:
        print("Creating new profile")
        # This creates a new database and account

        client_options = {
            'nodes': ['https://api.testnet.shimmer.network'],
        }

        # Shimmer coin type
        coin_type = 4219

        secret_manager = StrongholdSecretManager("wallet.stronghold", stronghold_password)

        wallet = IotaWallet('./twitter-database', client_options, coin_type, secret_manager)

        # Store the mnemonic in the Stronghold snapshot, this only needs to be done once
        account = wallet.store_mnemonic(shimmer_mnemonic)

        account = wallet.create_account('Twitter')
        print(account)
        input("Press Enter to continue...")
        os.system('clear')
    
def GetShimmerAddresses():
    # This shows all addresses in an account
    wallet = IotaWallet('./twitter-database')
    account = wallet.get_account('Twitter')
    address = account.addresses()
    print(f'Address: {address}')
    input("Press Enter to continue...")
    os.system('clear')

def SendNativeToken():
    # Send native tokens
    logger.info("I am in Send native tokens")
    wallet = IotaWallet('./twitter-database')
    account = wallet.get_account('Twitter')

    # Sync account with the node
    response = account.sync_account()
    print(f'Synced: {response}')
    logger.info("Sending to " + shimmer_receiver_address)
    wallet.set_stronghold_password(stronghold_password)
    
    outputs = [{
        "address": shimmer_receiver_address,
        "nativeTokens": [(
            shimmer_native_token_id,
            # hex converted
            hex(int(shimmer_native_token_amount))
        )],
    }];

    transaction = account.send_native_tokens(outputs, None)

    print(f'Sent transaction: {transaction}')

# Menu Options
menu_options = {
    1: 'Create Profile',
    2: 'Get Shimmer Address',
    3: 'Run bot',
    4: 'Configure',
    5: 'Show configuration',
    7: '⚠️  RESET ⚠️',
    9: 'Exit',
}

# MENU OPTION TEMPLATE
# def option#():
#     # Option  selected
#     print('Handle option \'Option #\'')

def print_menu():
    os.system('clear')
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
    # Option 1 selected run the CreateShimmerProfile function
    CreateShimmerProfile()

def option2():
    # Option 2 selected run the GetShimmerAddresses function
    GetShimmerAddresses()

def option3():
    # Option 3 selected run the RunTheTwitterBot function
    RunTwitterBot()
    

def option4():
    # Option 4 selected go through configuration
    ConfigureTwitterBot()

def option5():
    # Option 4 selected go through configuration
    ShowConfigurationTwitterBot()

def option7():
    ResetTwitterBotConfiguration()

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 7:
            option7()    
        elif option == 9:
            print('Thanks for using this bot')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 9.')
