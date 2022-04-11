# Legacy spaCy pipelines [Deprecated]

I've learned a bit about what does and does not work for our rule-based trait parsing needs.
- Entity rulers don't really work for out particular case because we are trapping matches and calling functions to fill trait data as the traits are being built (I.e. we need the on match callback). Using rulers for this purpose winds up forcing us to add more pipes to the pipeline, one pipe to form the entity/trait and another to add trait data. This not only slows the pipeline it also complicates the pipelines needlessly.
- Some pipes in this directory can be combined.
- Other pipes aren't needed at all.

Look at the [trait_pipes](../pipes) directory for the newer shiny trait pipes.
