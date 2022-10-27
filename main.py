# TODO
# CREATE twitter_user_id_filename if not existing
# CREATE shimmer_address_sent_to_filename if not existing

import re
import tweepy
import logging
import time
import csv
from iota_wallet import IotaWallet, StrongholdSecretManager
import os
from dotenv import load_dotenv
import random

load_dotenv()
# Load information from .env file
stronghold_password = os.getenv("STRONGHOLD_PASSWORD")
shimmer_mnemonic = os.getenv("SHIMMER_MNEMONIC")
shimmer_native_token_id = os.getenv("SHIMMER_NATIVE_TOKEN_ID")
shimmer_native_token_amount = os.getenv("SHIMMER_NATIVE_TOKEN_AMOUNT")
shimmer_address_pattern = os.getenv("SHIMMER_ADDRESS_PATTERN")
twitter_user_id_to_monitor = os.getenv("TWITTER_USER_ID_TO_MONITOR")
twitter_status_id_to_monitor = os.getenv("TWITTER_STATUS_ID_TO_MONITOR")
tweet_address_hrp_to_search = os.getenv("TWEET_ADDRESS_HRP_TO_SEARCH")
tweet_hashtag_to_search = os.getenv("TWEET_HASHTAG_TO_SEARCH")
print(tweet_hashtag_to_search)
config_done = os.getenv("CONFIG_DONE")

# Read/Write files
twitter_user_id_filename = os.getenv("TWITTER_USER_ID_FILENAME")
shimmer_address_sent_to_filename = os.getenv("SHIMMER_ADDRESS_SENT_TO_FILENAME")
twitter_tweet_id_replied_to_no_follow_filename = os.getenv("TWITTER_TWEET_ID_REPLIED_TO_NO_FOLLOW_FILENAME")
twitter_tweet_id_replied_to_no_hashtag_filename = os.getenv("TWITTER_TWEET_ID_REPLIED_TO_NO_HASHTAG_FILENAME")

follower_ids = []
replies_ids = []
shimmer_receiver_address = None
twitter_receiver_twitter_id = None

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


#####################################
# TWITTER SECTION
#####################################

# Twitter Configuration
def ConfigureTwitterBot():
    global config_done
    if IsConfigDone() == True:
        print("Configuration was already done. Use Option 3 to run the bot or Option 7 to RESET the configuration.")
        input("Press Enter to continue...")
        os.system('clear')
        return
    else:
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
                    test = input("Enter Your Twitter Username: ")
                    
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
                data[6] = "TWITTER_USER_ID_TO_MONITOR="+ str(twitter_user_id_to_monitor + "\n")
                data[7] = "TWITTER_STATUS_ID_TO_MONITOR="+ str(twitter_status_id_to_monitor + "\n")
                data[13] = "SHIMMER_NATIVE_TOKEN_ID="+ str(shimmer_native_token_id + "\n")
                data[14] = "SHIMMER_NATIVE_TOKEN_AMOUNT="+ str(shimmer_native_token_amount + "\n")
                data[18] = "CONFIG_DONE=1\n"
                with open('.env', 'w', encoding='utf-8') as file:
                    file.writelines(data)

        shimmer_native_token_id = InsertShimmerNativeTokenId()
        shimmer_native_token_amount = InsertShimmerNativeTokenAmount()
        twitter_user_id_to_monitor = InsertTwitterUserIdToMonitor()
        twitter_status_id_to_monitor = InsertTwitterStatusIdToMonitor()
        # Verifying if all necessary file exist or write them
        CheckFileExist(twitter_user_id_filename)
        CheckFileExist(shimmer_address_sent_to_filename)
        CheckFileExist(twitter_tweet_id_replied_to_no_follow_filename)

        WriteToEnv()
        config_done = "1"

        input("Press Enter to continue...")
        os.system('clear')

def ResetTwitterBotConfiguration():
    global config_done
    if IsConfigDone() == True:
        answer = input("Continue configuration reset? yes or no: ") 
        if answer == "yes": 
            def WriteToEnv():    
                with open('.env','r',encoding='utf-8') as file:
                    data = file.readlines()
                data[6] = "TWITTER_USER_ID_TO_MONITOR=\n"
                data[7] = "TWITTER_STATUS_ID_TO_MONITOR=\n"
                data[13] = "SHIMMER_NATIVE_TOKEN_ID=\n"
                data[14] = "SHIMMER_NATIVE_TOKEN_AMOUNT=\n"
                data[18] = "CONFIG_DONE=0\n"
                with open('.env', 'w', encoding='utf-8') as file:
                    file.writelines(data)
            DeleteExistingFile(twitter_user_id_filename)
            DeleteExistingFile(shimmer_address_sent_to_filename)
            DeleteExistingFile(twitter_tweet_id_replied_to_no_follow_filename)
            WriteToEnv()
            config_done = "0"
            logger.info("Configuration reset")
            input("Press Enter to continue...")
            os.system('clear')
        elif answer == "no": 
            return 

def ShowConfigurationTwitterBot():
    with open('.env','r',encoding='utf-8') as file:
        data = file.readlines()
        print("Actual configuration")
        print(data[6])
        print(data[7])
        print(data[13])
        print(data[14])
        print(data[18])
        print(data[19])
        print(data[20])
        print(data[21])
        print(data[22])
        print(data[23])
        input("Press Enter to continue...")
        os.system('clear')

# Twitter Bot
def CreateApi():
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

def GetFollowers(api):
    logger.info("Retrieving IDs of followers, this might take some time.")

    for user in tweepy.Cursor(api.get_follower_ids, screen_name=twitter_user_id_to_monitor).items():
        follower_ids.append(user)

def CheckMentions(api, keywords, user_name, monitor_id):
    if IsConfigDone() == True:
        global shimmer_address_pattern
        global shimmer_receiver_address
        global twitter_receiver_twitter_id
        global tweet_hashtag_to_search
        hashtag_found = None
        GetFollowers(api)
        logger.info(str(len(follower_ids)) + " followers found.")
        logger.info("Retrieving replies")
        extra_time = random.randint(1, 8)
        count = 0

        while count < 100:
            logger.info("Round: " + str(count))
            
            for tweet in tweepy.Cursor(api.search_tweets, q='to:'+user_name, result_type='recent', count=100).items(1000):

                try:
                    # for each status, overwrite that status by the same status, but from a different endpoint.
                    status = api.get_status(tweet.id, tweet_mode='extended')
                    logger.info("Getting extra sleep")
                    time.sleep(1 + extra_time)

                    # Verify if user's tweet is a reply
                    if hasattr(tweet, 'in_reply_to_status_id_str'):
                
                        # Verify if user's tweet is a reply to the tweet we monitor
                        if tweet.in_reply_to_status_id_str == monitor_id:
                            print(tweet.id)
                            logger.info("There is a reply to our giveaway")

                            # Verify if we already replied
                            CheckFileExist(twitter_tweet_id_replied_to_no_follow_filename)
                            with open(twitter_tweet_id_replied_to_no_follow_filename, mode ='r', encoding='UTF8') as file:
                                logger.info("Opening " + str(twitter_tweet_id_replied_to_no_follow_filename) + " file.")
                                if (str(tweet.id)) in file.read():                        
                                        logger.info("We already replied for no follow")
                                        break
                                else:
                                    logger.info("We did not reply for no follow. Continue.")
                                
                                    # Verify if user is following the account we tweeted from
                                    if tweet.user.id in follower_ids:
                                        logger.info("Is Following") 
                                        
                                        CheckFileExist(twitter_tweet_id_replied_to_no_hashtag_filename)
                                        with open(twitter_tweet_id_replied_to_no_hashtag_filename, mode ='r', encoding='UTF8') as file:
                                            logger.info("Opening " + str(twitter_tweet_id_replied_to_no_hashtag_filename) + " file.")
                                            if (str(tweet.id)) in file.read():                        
                                                logger.info("We already replied for no hashtag")
                                            else:
                                                logger.info("We did not reply for no hashtag. Continue.")
                                                
                                                # Verify if the hashtag is in the message
                                                hashtag_in_message = re.findall(r"\b %s\b" %tweet_hashtag_to_search,  tweet.text, flags=re.IGNORECASE)

                                                for tweet_hashtag_to_search in hashtag_in_message:
                                                    hashtag_found = True
                                                    print(hashtag_found)
                                                    logger.info("Hashtag found")

                                                if hashtag_found == None:
                                                    logger.info("Hashtag is missing")
                                                    reply_to_user = tweet.user.screen_name
                                                    message_to_reply = "@%s Sorry, you need to add the %s hashtag to get an airdrop! Write a new reply with your %s address and the %s hashtag!" %(reply_to_user, tweet_hashtag_to_search, keywords, tweet_hashtag_to_search)
                                                    api.update_status(message_to_reply, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata=True)
                                                    # Add tweet id to file
                                                    WriteToFile(tweet.id, twitter_tweet_id_replied_to_no_hashtag_filename)
                                                    tweet.favorite()
                                                    logger.info("Tweet is now liked")
                                                else:
                                                    # Verify if Twitter userID already got the tokens, or is on blocklist
                                                    CheckFileExist(twitter_user_id_filename)
                                                    with open(twitter_user_id_filename, mode ='r', encoding='UTF8') as file:
                                                        logger.info("Opening " + str(twitter_user_id_filename) + " file.")
                                                        if (str(tweet.user.id)) in file.read():
                                                            logger.info("User ID " + str(tweet.user.id) + " found in the list. Skipping.")
                                                            break
                                                        else:
                                                            logger.info("This is a new user. We continue")
                                                            
                                                            # Verify if the Tweet text contains the keyword
                                                            if any(keyword in tweet.text.lower() for keyword in keywords):
                                                                # Verify tweet has Shimmer address
                                                                shimmer_reply_address = re.findall(shimmer_address_pattern, tweet.text, flags=re.IGNORECASE)
                                                                logger.info("Looking for address in " + str(tweet.id))
                                                            
                                                                for shimmer_receiver_address in shimmer_reply_address:
                                                                    logger.info("Address found")

                                                                    if status.favorited == False:
                                                                        try:
                                                                            logger.info("Is not Liked")
                                                                            # Verify if Shimmer address already got the tokens, or is on blocklist
                                                                            CheckFileExist(shimmer_address_sent_to_filename)
                                                                            with open(shimmer_address_sent_to_filename, mode ='r', encoding='UTF8') as file:
                                                                                if (str(shimmer_reply_address)) in file.read():
                                                                                    logger.info("Address " + str(shimmer_reply_address) + " found in file. Skipping.")
                                                                                    break                   
                                                                                else:
                                                                                    logger.info("This is a new address")
                                                                                    # Now we send the tokens
                                                                                    SendNativeToken()
                                                                                    # Write the address to the file
                                                                                    WriteToFile(shimmer_receiver_address, shimmer_address_sent_to_filename)
                                                                                    #Write the Twitter user.ID to the file
                                                                                    WriteToFile(tweet.user.id, twitter_user_id_filename)
                                                                                    # We like (favorite) the Tweet to mark it as complete, this tweet will no longer be taken in consideration
                                                                                    tweet.favorite()
                                                                                    logger.info("Tweet is now liked")
                                                                        except tweepy.TweepyException as e:
                                                                            print('Error: ' + str(e))
                                                                            continue

                                                                    else:
                                                                        logger.info("Is liked no need to send tokens") 
                                                                else:
                                                                    logger.info("No address in the reply")
                                                            else:
                                                                logger.info("No keyword in the reply")
                                
                                    elif tweet.user.id not in follower_ids:
                                        logger.info("Not following, replying message.")
                                        reply_to_user = tweet.user.screen_name
                                        message_to_reply = "@%s Sorry, you need to follow @%s to get an airdrop!" %(reply_to_user, twitter_user_id_to_monitor)
                                        api.update_status(message_to_reply, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata=True)
                                        # Add tweet id to file
                                        WriteToFile(tweet.id, twitter_tweet_id_replied_to_no_follow_filename)
                                    else:
                                        logger.info("Not following, already replied")
                                        count = count + 1

                        else:
                            logger.info("This is not a reply to our giveaway tweet.")
                            count = count + 1
                            break

                    else:
                        logger.info("Is not a reply")
                        count = count + 1

                except tweepy.TweepyException as e:
                    print('Error: ' + str(e))

            else:
                logger.info("There is an issue with searching tweets.")
                count = count + 1
        else:
            CheckMentions(api, keywords, user_name, monitor_id)
    else:
        logger.info("Please finish the configuration")
        count = count + 1
    

def RunTwitterBot():
    api = CreateApi()
    keywords = tweet_address_hrp_to_search
    user_name = twitter_user_id_to_monitor
    monitor_id = twitter_status_id_to_monitor
    CheckMentions(api, keywords, user_name, monitor_id)

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
        try:
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
        except:
            logger.info("Add your 24 words mnemonic to the .env file") 
    
def GetShimmerAddresses():
    # This shows all addresses in an account
    wallet = IotaWallet('./twitter-database')
    account = wallet.get_account('Twitter')
    address = account.addresses()
    print(f'Address: {address}')
    input("Press Enter to continue...")
    os.system('clear')

def SendNativeToken():
    if IsConfigDone() == True:
        # Send native tokens
        logger.info("I am in Send native tokens")
        wallet = IotaWallet('./twitter-database')
        account = wallet.get_account('Twitter')

        # Sync account with the node
        response = account.sync_account()
        logger.info("Account syncronized")
        logger.info("Sending to " + str(shimmer_receiver_address))
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

        logger.info("Transaction sent")
        logger.info("Sleeping 25s to make sure transaction is out")
        time.sleep(25)

def SendToList():
    global shimmer_receiver_address
    if IsConfigDone() == True:
        if os.path.isfile('wallet.stronghold') == False:
            logger.info("Profile does not exists. Please create a profile first.")
            input("Press Enter to continue...")
            os.system('clear')
        else:
         ReadAddressesFromFile()

def ReadAddressesFromFile():
    global shimmer_receiver_address
    global shimmer_address_sent_to_filename
    if IsConfigDone() == True:
        with open('addresses_to_send.txt', mode ='r', encoding='UTF8') as file:
            for line in file.readlines():
                shimmer_reply_address = re.findall(shimmer_address_pattern, line, flags=re.IGNORECASE)
                for shimmer_receiver_address in shimmer_reply_address:
                    if line.startswith(shimmer_receiver_address):
                        logger.info("Address found " + str(shimmer_receiver_address))
                        SendNativeToken()
                        shimmer_receiver_address
                        WriteToFile(shimmer_receiver_address, shimmer_address_sent_to_filename)
                    else:
                        logger.info("This is not an address")

#####################################
# Configurations functions
#####################################

def WriteToFile(ins_data, ins_filename):
    with open(ins_filename, mode ='a+', encoding='UTF8') as file:
        file.writelines(str(ins_data) + "\n")
        for line in file:
            logger.info("Writing " + str(line) + " to file.")
            file.close()

def IsConfigDone():
    if config_done == "0":
        logger.info("Configuration was not done.")
        input("Press Enter to continue...")
        os.system('clear')
        return False
    else:
        logger.debug("Configuration is OK.")
        return True

def DeleteExistingFile(ins_filename):
    f_p = ins_filename
    # check if file is available in the file system
    if os.path.exists(f_p):
        os.remove(f_p)
        logger.info("The " + str(ins_filename) +  " file has been removed succesfully")
    else:
        logger.info("The " + str(ins_filename) +  " cannot be removed, or does not exist")

def CheckFileExist(ins_filename):
    f_p = ins_filename
    # check if file is available in the file system
    if not os.path.isfile(f_p):
        with open(f_p, "a") as f:
            logger.info('Empty text file was just created at {}.'.format(f_p))
    else:
        logger.info('File exists: {}.'.format(f_p))

# Menu Options
menu_options = {
    1: 'Create Profile',
    2: 'Get Shimmer Address',
    3: 'Run bot',
    4: 'Configure',
    5: 'Show configuration',
    7: '⚠️  RESET ⚠️',
    12: 'Send to list',
    99: 'Exit',
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
    CreateShimmerProfile()

def option2():
    GetShimmerAddresses()

def option3():
    RunTwitterBot()

def option4():
    ConfigureTwitterBot()

def option5():
    ShowConfigurationTwitterBot()

def option7():
    ResetTwitterBotConfiguration()

def option12():
    SendToList()

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
        elif option == 12:
            option12()                        
        elif option == 99:
            print('Thanks for using this bot')
            exit()
        else:
            print('Invalid option. Please enter the correct number.')
