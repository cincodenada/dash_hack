Dash Button Listener
====================

Intro
----

Okay, so you wanna have your Dash buttons do something other than order stuff from Amazon?  You're in the right place!

Currently, it can fire an IFTTT trigger, but it's built to be easily extensible to other outputs as well
(check out the IFTTTOutput directory).


This is heavily cribbed from Ted Benson's excellent article [How I Hacked Amazon’s $5 WiFi Button to track Baby Data][1],
and uses the same basic premise.  This code is forked from zippocage via davidgruhin, but refactored and organized and 
feature-fied to my satisfaction, because I'm never happy with anything.

How to use the thing
-------------------------

1. Get your Dash Button into a state where it's connected to your network.  I'll just quote Benson from the above article here:

 >Step 1: Prevent the Dash Button from actually ordering anything (Sorry Amazon)

 >The first thing you need to do is configure your buttons to send messages when you push them but not actually order anything. When you get a Dash button, Amazon gives you a list of setup instructions to get going. Just follow this list of instructions, but don’t complete the final step — don’t select the particular product you want ordered.

 >The last step for the Huggies button, for example, is to select which of several Huggies products you want. Just don’t answer this question and you won’t have to worry about actually buying anything.
 
 In short: install the Amazon app on your phone and go to Menu->Your Account->Dash Devices->Set up a new device

2. Get a Maker API key: go to https://ifttt.com/maker and follow the directions there to
connect the Maker channel and get a key.  Take note of the key, you'll need it for the next step.

3. Set up the config for your Dash listener.  Copy `config.basic.yaml` as `config.yaml` and fill in your Maker API key
where it says "YOUR MAKER API KEY HERE".  You'll fill in the other lines in a moment.

4. Find the MAC address of your button.  To get this, run `python dash-listen.py`,
and press the button.  It should say "Unknown dash button" and list the MAC.  If it doesn't, try adding `show_all_devices: true` on a new line in config.yaml and run it again.  When you have the MAC, copy it, and replace `1234deadbeef` in the config with the MAC address, and `your_ifttt_action_key` with whatever you want to call your action.

5. Set up the IFTTT action.  I have a [template ready to go][2], or you can just make your own.  Fill in the action name, pick your beeminder goal, and save it.

That's it! Now when you press your button with the script running, it should fire the IFTTT recipe and update Beeminder!  Hurrah!

I have the script running on a Raspberry Pi, but long as it's running on a computer connected to the same wifi as the button, it should pick it up.


[1]: https://medium.com/@edwardbenson/how-i-hacked-amazon-s-5-wifi-button-to-track-baby-data-794214b0bdd8#.9w4xdon1a
[2]: https://ifttt.com/recipes/451668-send-custom-dash-button-event-to-beeminder
