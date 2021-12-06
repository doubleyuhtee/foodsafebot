from textmatch import *

shpiel_keywords = Trigger(
    And(
        Not(Or("seal", "sealer")),
        Or("foodsafe", "foodsafety", And("food", Or("safe", "safety")))
    ))
