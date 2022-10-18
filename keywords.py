from textmatcher.textmatch import *

shpiel_keywords = Trigger(And("lkjsdffhlkasdfhlhlkasfdhlsfd"))

summon_keywords = Trigger(
    And(
        Or("/u/foodsafeprintbot",
           "u/foodsafeprintbot"
           "!foodsafe",
           "!foodsafebot",
           "!foodsafeprint",
           "!foodsafeprintbot",
           "foodsafeprintbot"),
        Not(Or("vote", "voting", "botrank"))
    )
)
