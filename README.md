# twitter-shimmer-dropper
Drop Shimmer Native Tokens to replies (on the Shimmer Testnet)

## TODO
[ ] Make hashtag search configurable  
[ ] Review and rewrite by a professional developer XD

# Setup

- clone the repo
- clone submodule `git submodule update --init --recursive`
- set up your Python environment and Shimmer library following the [Shimmer wiki](https://wiki.iota.org/shimmer/wallet.rs/getting_started/python)
- set up the .env file `cp .env.example .env`
- Add `Twitter Auth keys` and Shimmer parameters to the .env file
- Create Shimmer Profile
- Send Shimmer testnet tokens and native tokens to the bot's address visible in the menu
- Configure the bot using the menu
  - Token ID  
  ![image](https://user-images.githubusercontent.com/7383572/196972799-3b02a697-f4f7-4b1a-9560-141d9bc242ab.png)
  - Twitter User ID  
  ![image](https://user-images.githubusercontent.com/7383572/196972648-427baf23-cb99-4032-b5cb-663e2d1399a6.png)
  - Twitter Status ID of the tweet you want to monitor for replies  
  ![image](https://user-images.githubusercontent.com/7383572/196972482-ed04e58e-ace4-4b20-a629-3ec48520ee99.png)

- Start the bot using the menu

![image](https://user-images.githubusercontent.com/7383572/196917542-9dfc9956-d1d2-48db-82d8-a1adfb4019aa.png)

- Logic

![image](https://user-images.githubusercontent.com/7383572/198233769-dce113f6-2e88-405b-a7b7-3f47eef2b03e.png)


