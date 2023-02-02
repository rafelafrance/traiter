# Legacy spaCy pipelines [Deprecated]

I've learned a bit about what does and does not work for our rule-based trait parsing needs.
- Entity rulers don't really work for our particular case because we are trapping matches and calling functions to fill trait data as the traits are being built (I.e. we need the on match callback). Using rulers for this purpose winds up forcing us to add more pipes to the pipeline, one pipe to form the entity/trait and another to add trait data. This both slows and complicates pipelines needlessly.
- Some pipes in this directory were combined into a single pipe.
- Other pipes weren't needed at all.

This directory is only here so support older traiter projects.

Look at the [pipes](../pipes) directory for the newer shiny trait pipes.
