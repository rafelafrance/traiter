# Pipes for building traits

**Remember that traits are just annotated spaCy entities.**
That is, we're treating traits (aka attributes) as if they were entities.

You can see what that trait data is by looking at the `add_extensions` function
in the [pipe_util](extensions.py) file.

Pipes:
- [add_traits](add.py): Is the workhorse pipe. Use this when you want to add custom data to a trait. It creates an entity from a matched span and fills in some standard data, but you'll need a registered function to fill in the custom data.
- [term_pipe](term.py) Adds terms from a set of vocabularies as entities.
- [delete_traits](delete.py): Is used to get rid of partially built traits.
- [sentence](sentence.py): Breaks text into sentences using custom rules that work well on technical documents -- so far.
- [debug_tokens & debug_entities](debug.py): Pipes that print the current state of token or entity data within the pipeline. There are convenience functions (`token` & `ent`) for adding debug pipelines that handle renaming pipes when you need to add multiple debug pipes.
