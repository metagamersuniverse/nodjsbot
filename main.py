const { Telegraf } = require('telegraf');
const Web3 = require('web3');
const ethers = require('ethers');

const provider = new ethers.providers.InfuraProvider('mainnet', 'your-infura-project-id');
const web3 = new Web3('https://mainnet.infura.io/v3/your-infura-project-id');

const contractAddress1 = '0x123456789abcdef'; // Replace with the address of your smart contract1
const contractAbi1 = [...]; // Replace with the ABI of your smart contract1
const contract1 = new web3.eth.Contract(contractAbi1, contractAddress1);

const contractAddress2 = '0xd9e41dd9efc314ed265aa3b1df4a752e16cb4896'; // Replace with the address of your smart contract2
const contractAbi2 = [...]; // Replace with the ABI of your smart contract2
const contract2 = new ethers.Contract(contractAddress2, contractAbi2, provider);

const bot = new Telegraf('YOUR_TELEGRAM_BOT_TOKEN');

// Command to get the latest winner information
bot.command('latest_winner_info', async (ctx) => {
  try {
    const latestRound = await contract1.methods._lotteryRound().call();
    const winnerInfo = await contract1.methods.lotteryWinnerInfo(latestRound).call();
    const prizeAmount = (winnerInfo.prizeAmount / 1e18).toFixed(5);
    const message = `Latest Winner: ${winnerInfo.wallet}\nPrize Amount: ${prizeAmount} ETH`;
    ctx.reply(message);
  } catch (error) {
    console.error('Error getting latest winner info:', error);
    ctx.reply('Error getting latest winner info');
  }
});

// Command to get the wallet balance
bot.command('wallet_balance', async (ctx) => {
  const walletAddress = '0xD9E41dD9EFc314eD265aA3b1Df4A752e16Cb4896'; // Replace with your desired wallet address
  try {
    const balance = await web3.eth.getBalance(walletAddress);
    const formattedBalance = web3.utils.fromWei(balance);
    const message = `Wallet Address: ${walletAddress}\nBalance: ${formattedBalance} ETH`;
    ctx.reply(message);
  } catch (error) {
    console.error('Error getting wallet balance:', error);
    ctx.reply('Error getting wallet balance');
  }
});

// Command to get the lottery participants amount
bot.command('lottery_participants_amount', async (ctx) => {
  try {
    const participantsAmount = await contract1.methods.lotteryParticipantsAmount().call();
    const message = `Total Lottery Participants: ${participantsAmount}`;
    ctx.reply(message);
  } catch (error) {
    console.error('Error getting participants amount:', error);
    ctx.reply('Error getting participants amount');
  }
});

// Command to get the total rewards given by owner
bot.command('total_rewards_given', async (ctx) => {
  try {
    const totalRewardsGiven = await contract2.methods.totalRewardsGiven().call();
    const message = `Total Rewards Given: ${totalRewardsGiven}`;
    ctx.reply(message);
  } catch (error) {
    console.error('Error getting total rewards given:', error);
    ctx.reply('Error getting total rewards given');
  }
});

// Command to get the lottery round
bot.command('lottery_round', async (ctx) => {
  try {
    const lotteryRound = await contract1.methods._lotteryRound().call();
    const message
 = `Lottery Round: ${lotteryRound.toString()}`;
    ctx.reply(message);
  } catch (error) {
    console.error('Error getting lottery round:', error);
    ctx.reply('Error getting lottery round');
  }
});

// Command to get the winner details for a specific round
bot.command('winner_details', async (ctx) => {
  try {
    const roundNumber = ctx.message.text.split(' ')[1];
    if (!roundNumber) {
      ctx.reply('Please provide a round number');
      return;
    }
    const winnerInfo = await contract1.methods.lotteryWinnerInfo(roundNumber).call();
    const prizeAmount = (winnerInfo.prizeAmount / 1e18).toFixed(5);
    const message = `Winner: ${winnerInfo.wallet}\nPrize Amount: ${prizeAmount} ETH`;
    ctx.reply(message);
  } catch (error) {
    console.error('Error getting winner details:', error);
    ctx.reply('Error getting winner details');
  }
});

bot.launch();
