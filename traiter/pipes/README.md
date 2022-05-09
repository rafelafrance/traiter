# Pipes for building traits

**Remember that traits are just annotated spaCy entities.** That is we're treating traits (aka attributes) as if they were entities themselves.

You can see what that trait data is by looking at the `add_extensions` function in the [pipe_util](./pipe_util.py) file.

Pipes:
- [simple_traits](simple_traits_pipe.py): Creates traits from spacy entities by adding standard trait data to an entity.
- [add_traits](./add_traits_pipe.py): Is the workhorse pipe. Use this when you want to add custom data to a trait. It creates an entity from a matched span and fills in some standard data, but you'll need a registered function to fill in the custom data.
- [term_pipe](./term_pipe.py) Adds terms from a set of vocabularies as entities.
- [delete_traits](./delete_traits_pipe.py): Is used to get rid of partially build traits.
- [dependency.py](../old_pipes/dependency_pipe.py): Is a wrapper around a dependency matcher pipe which is used to link traits. For instance, does a color trait refer to a leaf color or a flower color.
- [sentence](./sentence_pipe.py): Breaks text into sentences using custom rules that work well on PDF files -- so far.
- [debug_tokens & debug_entities](./debug_pipes.py): Pipes that print the current state of token or entity data within the pipeline. There are convenience functions (`token` & `ent`) for adding debug pipelines that handle renaming pipes when you need to add multiple debug pipes.
