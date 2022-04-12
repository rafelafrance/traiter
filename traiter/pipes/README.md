# Pipes for building traits

Pipes:
- [simple_traits](./simple_traits.py) creates traits from spacy entities by adding standard trait data to an entity.
- [add_traits](./add_traits.py) is the workhorse pipe. Use this when you want to add custom data to a trait. It creates an entity from a matched span and fills in some standard data, but you'll need a registered function to fill in custom data.
- [delete_traits](./delete_traits.py) is used to get rid of partially build traits.
- [sentence](./sentence.py) breaks text into sentences using custom rules that work well on PDF files -- so far.
- [debug_tokens & debug_entities](./debug_traits.py) are pipes that print the current state of token or entity data.
