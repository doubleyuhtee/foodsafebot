from textmatcher.textmatch import *

shpiel_keywords = Trigger(
    And(
        Not(Or("seal", "sealer", "ceramic", "formlabs.com/blog/")),
        Or("cookie cutter", "foodsafe", "foodsafety", And("food", Or("safe", "safety")))
    ))

summon_keywords = Trigger(
    And(
        Or("/u/foodsafeprintbot",
           "!foodsafe",
           "!foodsafebot",
           "!foodsafeprint",
           "!foodsafeprintbot",
           "foodsafeprintbot"),
        Not(Or("vote", "voting", "botrank"))
    )
)
