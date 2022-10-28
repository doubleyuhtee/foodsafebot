# FoodSafeBot

Reminding everyone that 3d printing is not food safe, but can be, but isn't.

## Summon

`!FoodSafe` and I'll let everyone know the score

## Delete

If I respond incorrectly, there's nothing you can do yet. Feature coming.

## Setup

`git update-index --skip-worktree secrets`

## Included text

I have been summoned!

The United States Food and Drug administration doesn't actually have a definition for "Food Safe". The classification is Generally Regarded as Safe (GRAS). While [PLA](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=184.1061), and many forms of [Polyethylene (PET)](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=177.1630) including [Polyethylene glycol (PETG)](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=172.820) have these classifications, they are for the raw materials, not pigments or additives that are used to make it "silky" or have other properties.

The classification for PLA was granted "with no limitation other than current good manufacturing practice", which at the time did not include 3d printing. The method of deposition leaves pockets where bacteria can grow. Additionally, it is possible (though unlikely) that heavy metals can leach from the hot end into the plastics. Most resins are toxic in their liquid form and prolonged contact can deposit trace chemicals. For these reasons, it's recommended you use a food safe epoxy sealer or glaze.

CPE HT gets around this somewhat by being dishwasher safe and resistant to chemicals like bleach.

Beyond issues the the plastics themselves, new nozzles can come with a coating (often PTFE) to prevent blobs from sticking. The abrasives in the filament can wear this coating down and while it is safe for food to contact like on a frying pan, [the worn down products are not](https://pubmed.ncbi.nlm.nih.gov/28913736/).. It also wears the nozzle and metal particles can end up in the print. While copper and zinc (the ingredients for brass) are necessary in trace amounts, in larger amounts it can cause illness.

Or don't. I'm a bot, not a cop.

[Here is a video from Prusa](https://www.youtube.com/watch?v=D-SKMdlegdU) on some techniques that may work, [here is a relevant formlabs article](https://formlabs.com/blog/guide-to-food-safe-3d-printing/) and a [2010 material study](https://ift.onlinelibrary.wiley.com/doi/full/10.1111/j.1541-4337.2010.00126.x)

TL;DR: Use a sealer
