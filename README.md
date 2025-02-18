# legacy_samsungtv
Home Assistant Integration for legacy Samsung TV with enhanced source selection.

The legacy samsungtv platform allows you to control a legacy Samsung Smart TV. In my case a Series F (2013) TV.
This integration extensively used the Home Assistant (2025.2.0) core integration samsungtv maintained by @chemelli74 and @epenet. Many thanks. I do not have extensive knowledge of Home Assistant or python so my revisions may not be the most eloguent, but they work for me.

What I changed for this integration is that I enabled the custom selection of the TV sources; ie. HDMI 1, HDMI 2 or whatever sources you want to access on your TV. This is done by editing the SOURCES dictionary in the file media_player.py. For my TV you can not access HDMI 2 directly but must submit a key sequence to change the TV source with KEY_TV as the starting point. This capabilty also required a change to the samsungctl python utility by increasing the time lapse between key submissions, inorder for the TV to complete the instruction sent. The revised samsungctl utility (samsungTVlegacy) is included with the requirements in the manifest.json file.

Setup

Download the files and directories under legacy_samsungtv (less the CODEOWNERS file) into a directory named legacy_samsungtv under your Home Assistant custom_components directory.
The installation depends on your TV being ON and SSDP discovery being enabled. The configuration only uses SSDP and there is no need for adding anything to the configuration YAML file. Wait for the notification and confirm the detected device.

If your TV is first connected, you will need to accept Home Assistant on the TV to allow communication.

NOTE: Samsung Legacy TV's do not have the ability to be TURNED ON with an integration.

As always, use this at your own risk; I am not responsible for how you use it.
