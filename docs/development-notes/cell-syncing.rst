Syncing Instances Across Cells
==============================

If an ipyniivue.Niivue instance has already been displayed and then is
displayed again in a different cell, the older display(s) become
non-interactive.

The reason for the current implementation are: 1) any callbacks and
states for the NiiVue instance will be saved (i.e. transferred to each
new NiivueView) 2) previous views of the NiivueModel will be saved
(frozen/non-interactive). This allows for viewing progress over cells.
