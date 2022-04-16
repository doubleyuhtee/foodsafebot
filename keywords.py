from textmatcher.textmatch import *

shpiel_keywords = Trigger(
    And(
        Not(Or("seal", "sealer", "ceramic", "formlabs.com/blog/", "http://", "plastic wrap")),
        Or("cookie cutter", "cookiecutters", "cookiecutter", "cookie cutters")
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
