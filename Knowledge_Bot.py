import requests
from bs4 import BeautifulSoup
import json

urls = [
    "https://theadityakashyap.github.io/PortsideIndiaTraders/",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/about.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/products.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/contact.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/WebbingSlings.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/RoundSlings2.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/LoweringBelts.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/SinglePartSlings.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/MultipleLegSlings.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/GrommetSlings.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/FlemishEyeSlings.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/WireLockKits.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/VitaLife.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/CrossbyClipsAndSockets.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/CrossbyOpenAndClosedSpelterSockets.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/CrossbyOpenAndClosedSwageSockets.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/Thimbles.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/Hooks-hardware.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/Masterlinkes.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/MetricSwivelAndAlloyChain.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ForgedMasterLinks.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/MasterLinkAssembly.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ConnectingLinks.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/WebSlingConnectors.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ClevisChainSlingHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ClevisSelfLockingHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/EyeSelfLockingHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/SwivelSelfLockingHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/EyeHoistHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/EyeFoundryHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/EyeGrabHook.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ClevisGrabHooks.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/DShackles_AnchorBowShackles.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/WireRopeClamps.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/Turnbuckles_StrainingScrews.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/BeamLiftingClamps.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/VerticalLiftingClamps.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/HorizontalLiftingClamps.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ChainPulleyBlock.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/RatchetLeverHoist_PullPushTrolley_GearedTrolley.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/RatchetLeverHoist_PullPushTrolley_GearedTrolley.html#ratchet-content",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/RatchetLeverHoist_PullPushTrolley_GearedTrolley.html#pull-push-content",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/RatchetLeverHoist_PullPushTrolley_GearedTrolley.html#geared-content",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/BabyChainPulleyHoist.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/HeavyDutyWireropeHoist.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/SnatchBlockWithShackle.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ManualWinches.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/ElectricWinches.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/Anchors.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/StudLinkAnchorChain.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/LashingChainsAndLoadBinders.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/GarfilMooringRopes.html",
    "https://theadityakashyap.github.io/PortsideIndiaTraders/GarfilIndustrialRopes.html"

]

content = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(soup.stripped_strings)
    content.append({
        "url": url,
        "text": text
    })

with open('website_content.json', 'w') as f:
    json.dump(content, f)