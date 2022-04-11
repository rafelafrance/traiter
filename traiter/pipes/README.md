# Pipes for building traits

Pipes:
- [simple_traits](./simple_trait.py) creates traits from spacy entities by adding standard trait data to an entity.
- [add_traits](./add_traits.py) is the workhorse pipe. Use this when you want to add custom data to a trait. It creates an entity from a matched span and fills in some standard data, but you'll need a registered function to fill in custom data.
- [forget_traits](./forget_traits.py) is used to get rid of partially build traits.
