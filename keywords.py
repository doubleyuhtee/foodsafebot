from textmatcher.textmatch import *

shpiel_keywords = Trigger(
    And(
        Not(Or("seal", "sealer", "ceramic", "formlabs.com/blog/")),
        Or("cookie cutter", "cookiecutters", "cookiecutter", "cookie cutters",
           "foodsafe", "foodsafety", And("food", Or("safe", "safety")))
    ))

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
