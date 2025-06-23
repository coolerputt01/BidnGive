<template>
    <main style="background-color: #ebebd3ff;">
        <section style="margin-bottom: 12%;">
            <div style="display: flex;justify-content: space-between;align-items: center;padding: 24px;">
                <div style="line-height: 8px;">
                    <h2 style="font-size: 1.2em;font-weight: 600;">Hello, Coolerputt!</h2>
                    <p style="font-size: 0.9em;">Welcome back</p>
                </div>
                <div>
                    <img src="/icons/notification-on.svg" alt="Notifications Icon" style="width: 1.8em;height: 1.8em;">
                </div>
            </div>
            <section style="display: flex;justify-content: center;align-items: center;flex-direction: column;">
                <div style="text-align: center;display: flex;justify-content: center;align-items: center;border-radius: 3px;">
                    <span style="color: #004f28;background-color: #e0ffe0;font-size: 0.9em;padding: 4px;font-weight: 600;border-radius: 6px;">⏰ Next auction starts in 0h :01m :0s</span>
                </div>
                <div style="margin-top: 4%;border-radius: 3px;background-color: #95190C;padding: 12px;width: 80%;">
                    <div>
                        <div style="display: flex;justify-content: space-between;align-items: center;width: 100%;color: #fff;"><p style="font-size: 1.3em;color: #fff;display: flex;justify-content: flex-start;align-items: center;gap: 3%;">Market Status</p> <span style="background-color: #191919;border-radius: 50px;color: #fff;padding: 5px;font-size: 0.9em;padding-left: 10px;padding-right: 10px;">Market Closed</span></div>
                        <div style="display: flex;justify-content: space-between;align-items: center;width: 100%;color: #fff;"><p>🕐 Next Auction: 08:30PM</p><p>02:02:18</p></div>
                        <div style="display: flex;justify-content: center;align-items: center;width: 100%;">
                            <button style="width: 60vw;padding: 10px;background-color: #fff;font-weight: 550;text-align: center;border-radius: 50px;outline: none;border: none;">Auction</button>
                        </div>
                    </div>
                </div>
                <!-- Wallet Balance Card -->
                <div style="margin-top: 4%; border-radius: 12px; background-color: #17a35e; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <p style="font-size: 1.2em; color: #fff; font-weight: 600; margin-bottom: 10px;">💰 Wallet Balance</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #fff; font-size: 1.6em; font-weight: bold;">₦50,000</span>
                    <button style="padding: 10px 20px; background-color: #fff; color: #17a35e; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;">
                    Withdraw
                    </button>
                </div>
                </div>

                <!-- Ongoing Bids Card -->
                <div style="margin-top: 4%; border-radius: 12px; background-color: #191919; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <p style="font-size: 1.2em; color: #fff; font-weight: 600; margin-bottom: 10px;">
                    <img src="/icons/moneybag.svg" alt="Bid Icon" style="width: 1.3em; height: 1.3em; margin-right: 6px;" />
                    Ongoing Bids
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #fff; font-size: 1.5em; font-weight: bold;">1</span>
                    <button style="padding: 10px 20px; background-color: #fff; color: #191919; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;">
                    View Bid
                    </button>
                </div>
                </div>
                <!-- Combined Referral Overview -->
<div style="margin-top: 4%; border-radius: 12px; background-color: #e0ffe0; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <p style="font-size: 1.2em; color: #004f28; font-weight: 600; margin-bottom: 16px;">🎁 Referral Overview</p>
  
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
    
    <!-- Referral Balance -->
    <div style="flex: 1; min-width: 120px;">
      <p style="color: #004f28; font-size: 0.9em; margin-bottom: 4px;">Referral Balance</p>
      <span style="font-size: 1.5em; font-weight: bold; color: #004f28;">₦2,000</span>
    </div>

    <!-- Referral Count -->
    <div style="flex: 1; min-width: 120px;">
      <p style="color: #004f28; font-size: 0.9em; margin-bottom: 4px;">Total Referrals</p>
      <span style="font-size: 1.5em; font-weight: bold; color: #004f28;">4 Users</span>
    </div>

    <!-- Withdraw Button -->
    <div style="flex: 1 1 100%; text-align: right;">
      <button style="padding: 10px 20px; background-color: #17a35e; color: #fff; font-weight: 600; border-radius: 50px; border: none; cursor: pointer;">
        Withdraw
      </button>
    </div>
  </div>
</div>


                <!-- Referral Info Card -->
                <div style="margin-top: 4%; border-radius: 12px; background-color: #fff; padding: 20px; width: 80%; max-width: 600px; margin-inline: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <p style="font-size: 1.2em; color: #17a35e; font-weight: 600; margin-bottom: 10px;">📢 Invite & Earn</p>
                <p style="color: #444; font-size: 0.95em; margin-bottom: 10px;">
                    Share your referral link and earn ₦500 for every user that joins and makes a bid.
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <input type="text" readonly value="https://yourapp.com/ref/coolerputt" style="flex: 1; min-width: 200px; padding: 10px; border-radius: 6px; border: 1px solid #ccc;" />
                    <button style="padding: 10px 16px; background-color: #17a35e; color: #fff; font-weight: 600; border: none; border-radius: 6px; cursor: pointer;">
                    Copy Link
                    </button>
                </div>
                </div>
            </section>
            <section style="margin-top: 2%;padding: 13px;">
                <section style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 20px; margin-top: 1%; overflow-x: hidden; padding: 10px;">
                    <span class="contact" style="width: auto; height: auto; padding: 20px; border-radius: 50%; background-color: #191919;position: fixed;right: 4%;bottom: 23%;display: flex; align-items: center; justify-content: center;box-shadow: 9px 4px 5px 0px rgba(0,0,0,0.3);">
                        <img src="/icons/whatsapp.svg" alt="Bid icon" style="width: 2em;height: 2em;">
                    </span>
                </section>
            </section>
            <section style="margin-top: 2%;padding: 23px;background-color: #fff;border-radius: 20px;">
                <div style="display: flex;justify-content: space-between;align-items: center;">
                    <div>
                        <span style="color: #191919ff;font-size: 1.3em;font-weight: 600;padding: 5px;">Recent Transactions</span>
                    </div>
                    <div>
                        <span style="color: #191919ff;font-size: 0.9em;font-weight: 600;padding: 5px;color: #172A3A;">View all</span>
                    </div>
                </div>
                <section style="display: flex;justify-content: flex-start;align-items: center;flex-direction: column;margin-top:3%;overflow-x: hidden;">
                    <div style="display: flex;justify-content: space-between;align-items: center;flex-direction: row;border-bottom: 1.2px solid #191919ff;padding: 18px;gap: 5%;">
                        <img src="/icons/credit.svg" alt="Credit alert" style="width: 1.8em;height: 1.8em;background-color: lightgrey;border-radius: 50%;padding: 12px;">
                        <span style="line-height: 6px;width: 60vw;">
                            <span style="font-size: 1.3em;font-weight: 600;width: 100%;">Mr Adeniyi Samuel</span>
                            <p style="font-size: 1em;font-weight: normal;width: 100%;color: grey">Recommitment</p>
                        </span>
                        <span style="font-size: 1.3em;font-weight: 600;">
                            &#8358;5,000
                        </span>
                    </div>
                    <div style="display: flex;justify-content: space-between;align-items: center;flex-direction: row;border-bottom: 1.2px solid #191919ff;padding: 18px;gap: 5%;">
                        <img src="/icons/credit.svg" alt="Credit alert" style="width: 1.8em;height: 1.8em;background-color: lightgrey;border-radius: 50%;padding: 12px;">
                        <span style="line-height: 6px;width: 60vw;">
                            <span style="font-size: 1.3em;font-weight: 600;width: 100%;">Mr Adeniyi Samuel</span>
                            <p style="font-size: 1em;font-weight: normal;width: 100%;color: grey">Recommitment</p>
                        </span>
                        <span style="font-size: 1.3em;font-weight: 600;">
                            &#8358;5,000
                        </span>
                    </div>
                </section>
            </section>
        </section>
        <NavBar />
    </main>
</template>